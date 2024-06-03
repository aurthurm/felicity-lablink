import ssl
import json
import time
from time import sleep
from datetime import datetime
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth

from flablink.config import SEND_TO_QUEUE
from flablink.gateway.extensions.event.base import EventType
from flablink.gateway.extensions.event.event import post_event
from flablink.gateway.services.order.order import OrderService
from flablink.gateway.forward.conf import (
    EXCLUDE_RESULTS, KEYWORDS_MAPPING, LIMS_SETTINGS, LINK_SETTINGS, SyncStatus
)
from flablink.gateway.forward.result_parser import (
    ResultParser, HologicEIDInterpreter
)
from flablink.gateway.helpers import has_special_char
from flablink.gateway.db.session import test_db_connection
from flablink.gateway.logger import Logger

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logger = Logger(__name__, __file__)


class FowardOrderHandler:
    def __init__(self):
        self.order_service = OrderService()

    @staticmethod
    def sanitise(incoming):
        """Sanitise incoming data by removing special characters."""
        return [item.replace(';', ' ').strip() if isinstance(item, str) else item for item in incoming]

    def fetch_astm_results(self): 
        return self.order_service.find_all(
            filters={"synced__exact": 0}, 
            limit=LINK_SETTINGS.submission_limit
        )
    
    @staticmethod
    def _to_csv(data_frame): data_frame.to_csv("result_orders.csv", index=False)

    def update_result(self, order_id: int, lims_sync_status: int, sync_comment: str = ""):
        logger.log(
            "info",
            f"FowardOrderHandler: Updating astm result orders with uid: {order_id} with synced: {lims_sync_status} ..."
        )
        self.order_service.update(
            uid=order_id,
            synced=lims_sync_status,
            sync_comment=sync_comment,
            sync_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        logger.log(
            "info",
            f"FowardOrderHandler: Updated astm result orders with uid: {order_id} with synced: {lims_sync_status}..."
        )


class SenaiteHandler:
    username = LIMS_SETTINGS.username
    password = LIMS_SETTINGS.password
    api_url = f"{LIMS_SETTINGS.address}{LIMS_SETTINGS.api_url}"
    also_verify = LINK_SETTINGS.verify_results
    timeout = 10

    def _auth_session(self):
        """ start a fresh requests session """
        self.session = requests.session()
        self.session.verify = ssl.CERT_NONE
        self.session.auth = HTTPBasicAuth(self.username, self.password)
        self.session.timeout = self.timeout

    def test_senaite_connection(self) -> bool:
        """Test connection to Senaite."""
        self._auth_session()
        url = f"{self.api_url}/"
        logger.log("info", f"SenaiteHandler: intiating connection to: {url}")
        try:
            response = self.session.post(url)
            if response.status_code == 200:
                logger.log(
                    "info", f"SenaiteHandler: connection established")
                return True
            else:
                logger.log(
                    "error", f"SenaiteHandler: connection failed")
                self.error_handler(url, response, None)
                return False
        except Exception as e:
            logger.log(
                "error", f"SenaiteHandler: connection failed with error: {e}")
            return False

    @staticmethod
    def error_handler(url=None, res=None, request_id=None):
        """Log errors encountered during requests."""
        logger.log("info", f"SenaiteHandler: Error Status Codel::{request_id}:: {res.status_code} Reason: {res.reason}")
        logger.log("info", f"SenaiteHandler: Error Detail::{request_id}:: {res.text}")

    @staticmethod
    def decode_response(response):
        return json.loads(response)

    def search_analyses_by_request_id(self, request_id: str, order_uid: int):
        """Searches senaite's Analysis portal for results
        @param request_id: Sample ID e.g BP-XXXXX
        @return dict
        """
        success = True
        data = None
        
        # searching using an ID.
        search_url = f"{self.api_url}/search?getRequestID={request_id.upper()}&catalog=bika_analysis_catalog"
        logger.log("info", f"SenaiteHandler: Searching ... {search_url}")

        post_event(EventType.FORWARD_STREAM, id=order_uid, search_started=datetime.now(), connection="connected", activity="searching", message=request_id)
        response = self.session.get(search_url)
        if response.status_code == 200:
            success = True
            data = self.decode_response(response.text)
        else:
            success = False
            data = None
            self.error_handler(search_url, response, request_id)

        post_event(EventType.FORWARD_STREAM, id=order_uid, search_ended=datetime.now(), connection="connected", activity="idle", message="")
        return success, data

    def update_resource(self, uid, payload, request_id: str, order_uid: int):
        """ create a new resource in senaite: single or bundled """
        url = f"{self.api_url}/update/{uid}"
        logger.log("info", f"SenaiteHandler: Updating resource: {url} for {request_id} with {payload}")
        success = True
        response = None

        post_event(EventType.FORWARD_STREAM, id=order_uid, update_started=datetime.now(), connection="connected", activity="submitting", message=request_id)
        response = self.session.post(url, json=payload)
        if response.status_code == 200:
            success = True
            data = self.decode_response(response.text)
        else:
            success = False
            self.error_handler(url, response, request_id)
            data = self.decode_response(response.text)
        post_event(EventType.FORWARD_STREAM, id=order_uid, update_ended=datetime.now(), connection="connected", activity="idle", message="")
        return success, data

    @staticmethod
    def _one_for_keyword(values, keyword, is_eid):
        if len(values) == 1:
            logger.log("info", f"SenaiteHandler: Analysis with keyword {keyword} successfully resolved ...")
            return True, values[0], is_eid

        if len(values) > 1:
            logger.log("info", f"SenaiteHandler: More than 1 anlysis found for keyword: {keyword}")
            return False, values, is_eid

        return False, None, is_eid

    def resolve_by_keywords(self, keyword, results):
        original = results
        if len(results) == 0:
            return False, None, False

        logger.log("info", f"SenaiteHandler: Resolving analysis containing keyword {keyword} ...")

        mappings = KEYWORDS_MAPPING.get(keyword, [keyword])
        mappings.append(keyword)
        mappings = list(set(mappings))

        states = ["unassigned", "assigned"]
        results = list(filter(lambda r: r["review_state"] in states and r["getKeyword"] in mappings, results))

        found, payload, is_eid = self._one_for_keyword(results, keyword, False)
        if found:
            return found, payload, is_eid

        if LINK_SETTINGS.resolve_hologic_eid:
            eids = list(filter(lambda r: r["review_state"] in states and r["getKeyword"] in ["EID"], original))
            return self._one_for_keyword(eids, keyword, True)

        obtained = list(map(lambda r: (r["getKeyword"], r["review_state"]), original))

        logger.log("info", f"SenaiteHandler: No anlysis found for keyword: {keyword} with state in {states}. \
         Obtained: {obtained}")
        return False, None, False

    def do_work_for_order(self, order_uid, request_id, result, keyword=None):
        self._auth_session()
        
        if has_special_char(request_id):
            FowardOrderHandler().update_result(order_uid, SyncStatus.SKIPPED, "Has special characters")
            return False

        searched, search_payload = self.search_analyses_by_request_id(request_id, order_uid)
        if not searched:
            return False

        search_items = search_payload.get("items", [])

        found, search_data, is_eid = self.resolve_by_keywords(keyword, search_items)
        if not found:
            logger.log(
                "info", 
                f"SenaiteHandler: search for {request_id}, {keyword} did not find any matches"
            )
            FowardOrderHandler().update_result(order_uid, SyncStatus.SKIPPED, f"No pending results matching keyword: {keyword}")
            return False

        if is_eid:
            result = HologicEIDInterpreter(result).output
            if not result:
                return False

        submitted = False
        submit_payload = {
            "transition": "submit",
            "Result": result,
            "InterimFields": []
        }

        logger.log("info", f"SenaiteHandler:  ---submitting result--- ")
        submitted, submission = self.update_resource(
            search_data.get("uid"), submit_payload, request_id, order_uid
        )

        if not submitted:
            logger.log("info", f"SenaiteHandler: Submission Response for checking : {submission}")

        if self.also_verify:
            if not submitted:
                return False

            verified = False
            verify_payload = {"transition": "verify"}

            submission_items = submission.get("items")
            if not len(submission_items) > 0:
                return False

            submission_data = submission_items[0]
            # assert submission_data.get("uid") == search_data.get("uid")

            logger.log("info", f"SenaiteHandler:  ---verifying result---")
            verified, verification = self.update_resource(
                submission_data.get("uid"), verify_payload, request_id, order_uid
            )

            # DateVerified is not None, 'VerifiedBy': 'system_daemon'
        return True


class SenaiteQueuer:

    def __init__(self):
        self.base_url = LIMS_SETTINGS.address
        self.api_url = f"{LIMS_SETTINGS.address}{LIMS_SETTINGS.api_url}"
        self.session = None
        self.start_session(LIMS_SETTINGS.username, LIMS_SETTINGS.password)

    def start_session(self, username, password):
        logger.log("info", "Starting session with SENAITE ...")
        self.session = requests.Session()
        self.session.auth = (username, password)

        # try to get the version of the remote JSON API
        version = self.get_version()
        if not version or not version.get('version'):
            logger.log(
                "error", f"senaite.jsonapi not found on at {self.api_url}")
            return False

        # try to get the current logged in user
        user = self.get_authenticated_user()
        if not user or user.get("authenticated") is False:
            logger.log("error", "Wrong username/password")
            return False

        logger.log(
            "info", f"Session established ('{username}') with '{self.base_url}'")
        return True

    def send_message(self, message):
        if message:
            logger.log(
                "info", f"Sending message to SENAITE: {message[:50]} ...")

        if not self.session:
            logger.log("info", "Session not started yet")
            return False

        url_import = f"{self.base_url}/serial_push"
        response = self.session.post(url_import,
                                     data={"message": message},
                                     timeout=30)
        if response.text == "ACK":
            logger.log("info", "Message accepted")
            return True
        logger.log("info", F"Message not accepted: {response.__dict__}")
        return False

    def get_version(self):
        """Return the remote JSON API version
        """
        return self.get_json("version")

    def get_authenticated_user(self):
        """Return the current logged in remote user
        """
        return self.get_first_item("users/current")

    def get_first_item(self, endpoint, **kw):
        """Fetch the first item of the 'items' list from a std. JSON API reponse
        """
        items = self.get_items_with_retry(
            endpoint=endpoint, **kw)
        if not items:
            return None
        return items[0]

    def get_items_with_retry(self, max_attempts=LIMS_SETTINGS.max_attempts,
                             interval=LIMS_SETTINGS.attempt_interval, **kwargs):
        """
        Retries to retrieve items if HTTP response fails.
        :param max_attempts: maximum number of attempts to try
        :param interval: time delay between attempts in seconds
        :param kwargs: query and parameters pass to get_items
        :return:
        """
        items = None
        for i in range(max_attempts):
            items = self.get_items(kwargs.get("endpoint", None))
            if items:
                break
            sleep(interval)
        return items

    def get_items(self, endpoint):
        """
        Return the 'items' list from a std. JSON API response
        """
        data = self.get_json(endpoint)
        if not isinstance(data, dict):
            return []
        return data.get("items", [])

    def get_json(self, endpoint):
        """Fetch the given url or endpoint and return a parsed JSON object
        """
        api_url = self.get_api_url(endpoint)
        try:
            response = self.session.get(api_url)
        except Exception as e:
            message = f"Could not connect to {api_url} Please check"
            logger.log("error", message)
            logger.log("error", e)
            return {}
        status = response.status_code
        if status != 200:
            message = f"GET for {endpoint} ({api_url}) returned Status Code {status}. Please check."
            logger.log("error", message)
            return {}
        return response.json()

    def get_api_url(self, endpoint):
        """Create an API URL from an endpoint"""
        return "/".join([
            self.api_url,
            "/".join(endpoint.split("/"))
        ])


class ResultFowarder(FowardOrderHandler, SenaiteHandler):
    def run(self):
        # reset connection
        post_event(EventType.FORWARD_STREAM, id=None, connection="connecting", activity="idle", message="")

        if not test_db_connection():
            logger.log("info", "ResultInterface: Failed to connect to db, backing off a little ...")
            post_event(EventType.FORWARD_STREAM, id=None, connection="error", activity="test-database-connection", message="Failed to connect to the db")
            return

        if not self.test_senaite_connection():
            post_event(EventType.FORWARD_STREAM, id=None, connection="error", activity="test-senaite-connection", message="Failed to connect to senaite")
            logger.log("info", "ResultInterface: Failed to connectto Senaite, backing off a little ...")
            return
        
        # connections established
        post_event(EventType.FORWARD_STREAM, id=None, connection="connected", activity="fetch-orders", message="")

        logger.log("info", "ResultInterface: All connections were successfully estabished :)")

        to_exclude = [x.strip().lower() for x in EXCLUDE_RESULTS]

        orders = self.fetch_astm_results()
        total = len(orders)
        if total <= 0:
            logger.log("info", "ResultInterface: No orders at the moment :)")

        logger.log("info", f"ResultInterface: {total} order are pending syncing ...")

        for index, order in enumerate(orders):

            if index > 0 and index % LINK_SETTINGS.sleep_submission_count == 0:
                logger.log("info", "ResultInterface:  ---sleeping---")
                time.sleep(LINK_SETTINGS.sleep_seconds)
                logger.log("info", "ResultInterface:  ---waking---")

            logger.log("info", f"ResultInterface: Processing {index} of {total} ...")

            senaite_updated = False
            if SEND_TO_QUEUE:
                senaite_updated = SenaiteQueuer(
                ).send_message(order['raw_message'])
            else:
                # Parse the result object before sending to LIMS
                result_parser = ResultParser(order.result, order.unit)
                result = str(result_parser.output)

                if isinstance(result, str):
                    if result.strip().lower() in to_exclude:
                        # also update astm db for excluded to avoid unecessary trips
                        senaite_updated = True
                    else:
                        senaite_updated = self.do_work_for_order(
                            order.uid,
                            order.order_id,
                            result,
                            order.keyword
                        )
                else:
                    senaite_updated = self.do_work_for_order(
                        order.uid,
                        order.order_id,
                        result,
                        order.keyword
                    )
            #
            if senaite_updated:
                self.update_result(order.uid, SyncStatus.SYNCED)

        post_event(EventType.FORWARD_STREAM, id=None, connection="disconnected", activity="", message="")