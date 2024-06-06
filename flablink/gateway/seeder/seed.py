from flablink.gateway.models.order import (
    ResultExclusions,
    ResultTranslation,
    KeywordMapping
)
from flablink.gateway.models.settings import (
    LinkSettings,
    LimsSettings
)
from flablink.gateway.models.performance import Forwarder



def seed_link_settings():
    if not LinkSettings().all():
        LinkSettings(
            verify_results=False,
            resolve_hologic_eid=False,
            submission_limit=250,
            sleep_seconds=5,
            sleep_submission_count=10,
            clear_data_over_days=30,
            poll_db_every=10,
        ).save()

def seed_lims_settings():
    if not LimsSettings().all():
        LimsSettings(
            address="http://localhost:8080",
            api_url="/senaite/@@API/senaite/v1",
            username="username",
            password="password",
            max_attempts=10,
            attempt_interval=30,
            is_active=True
        ).save()


def seed_keyword_mappings():
    KEYWORDS_MAPPING = {
        # Abbott
        "HIV1mlDBS": ["Abbott", "HIV06ml", "VLDBS", "VLPLASMA", ],
        "HIV1.0mlDBS": ["Abbott", "HIV06ml", "VLDBS", "VLPLASMA", ],
        "HIV06ml": ["Abbott", "HIV06ml", "VLDBS", "VLPLASMA", ],
        "HIV0.2ml": ["Abbott", "HIV06ml", "VLDBS", "VLPLASMA", ],
        # Roche Cobas
        "HI2DIL96": ["HI2CAP96", "VLDBS", "VLPLASMA", ],
        "HI2DIL48": ["HI2CAP96", "VLDBS", "VLPLASMA", ],
        "HI2CAP48": ["HI2CAP96", "VLDBS", "VLPLASMA", ],
        "HI2CAP96": ["HI2CAP96", "VLDBS", "VLPLASMA", ],
        # Roche 6800/8800
        # "HIVVL": ["VLPLASMA", "EID", ], 
        "HIV": ["VLPLASMA", ],
        # "HIV-1-2-DBS": ["EID", ],
        # Hologic Panther/Alinity
        "qHIV-1": ["ViralLoad", "VLDBS", "VLPLASMA", ],
        "HIV-1": ["ViralLoad", "VLDBS", "VLPLASMA", ],
        "HIV-DBS": ["ViralLoad", "VLDBS", "VLPLASMA", ],
        "HPV": ["HPV", "HPV01", ]
    }

    for kw, mp in KEYWORDS_MAPPING.items():
        kewyword = KeywordMapping().get(keyword=kw)
        if not kewyword:
            kewyword = KeywordMapping(keyword=kw).save()
        kewyword.update(mappings=', '.join(mp), is_active=True)

def seed_result_exclusions():
    EXCLUDE_RESULTS = ["ValueNotSet"]
    for _er in EXCLUDE_RESULTS:
        if not ResultExclusions().get(result=_er):
            ResultExclusions(result=_er).save()

def seed_result_translations():
    INTEPRETATIONS = {
        "< Titer min": "< 20",
        "< Titer Min": "< 20",
        "> Titer max": "> 10000000",
        "> Titer Max": "> 10000000",
        "Reactive": "Strong Positive",
        "Non-Reactive": "Negative",
        "Not Detected": "Target Not Detected",
    }
    for _i in INTEPRETATIONS.keys():
        if not ResultTranslation().get(original=_i):
            ResultTranslation(original=_i, translated=INTEPRETATIONS[_i]).save()

def seed_performance_tracker():
    if not Forwarder().all():
        Forwarder(
            connection="disconnected",
            activity="",
            message=""
        ).save()