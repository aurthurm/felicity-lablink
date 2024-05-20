import socket
import time 
from datetime import datetime

from hl7apy.parser import parse_message
from hl7apy.core import Message  as HL7Message

from flablink.gateway.link.base import AbstractLink
from flablink.gateway.extensions.event.base import EventType
from flablink.gateway.extensions.event.event import post_event
from flablink.gateway.link.schema import InstrumentConfig
from flablink.gateway.link.config import ProtocolType, SocketType
from flablink.gateway.logger import Logger

logger = Logger(__name__, __file__)

SB = b"\x0b"  # <SB>, vertical tab - start block
EB = b"\x1c"  # <EB>, file separator - end block
CR = b"\x0d"  # <CR>, \r - carriage return
FF = b"\x0c"  # <FF>, new page form feed

NAK = chr(0x15)  # NAK

RECV_BUFFER = 1024 # 4096


class SocketLink(AbstractLink): 
    def __init__(self, instrument_config: InstrumentConfig):
        # Instrument configuration
        self.uid = instrument_config.uid
        self.name = instrument_config.name
        self.host = instrument_config.host
        self.port = instrument_config.port
        self.socket_type: SocketType = instrument_config.socket_type
        self.protocol_type: ProtocolType = instrument_config.protocol_type
        self.auto_reconnect: bool = instrument_config.auto_reconnect
        self.encoding = "utf-8"
        # socket
        self.socket = None
        # self.is_connected = False
        # base
        self._received_messages = list()
        self.establishment = False
        self.response = None
        self._buffer = b''
        # ACK | NACK
        self.msg_id = None
        self.expect_ack = False

    def start_server(self, trials=1):
        """Start serial server"""
        logger.log("info", "Starting socket server ...")

        post_event(EventType.ACTIVITY_STREAM, **{
            'id': self.uid,
            'connection': "connecting",
            'trasmission': "",
        })

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                sckt = s
                if self.socket_type == SocketType.CLIENT:
                    sckt.connect((self.host, self.port))

                if self.socket_type == SocketType.SERVER:
                    s.bind((self.host, self.port))
                    s.listen(1)
                    sckt, _ = s.accept()
                
                self.socket = sckt
                
                post_event(EventType.ACTIVITY_STREAM, **{
                    'id': self.uid,
                    'connection': "connected",
                    'trasmission': "",
                })
                
                while True:
                    data = self._read_data(sckt)
                    if data == b'':
                        raise Exception("Connection closed")

                    # Is this a new session ?
                    if not self.is_open():
                        self.open()

                    self.process(data)

                    # Does the receiver has to send something back?
                    response = self.get_response()
                    if response == "ACK":
                        self.ack()
                    if response == "NACK":
                        self.nack()
            
        except OSError as e:
            logger.log("info", f"OS error: {e}")
        except Exception as e:
            logger.log("info", f"An unexpected error occured: {e}")
        finally:     
            self.socket = None
            
            post_event(EventType.ACTIVITY_STREAM, **{
                'id': self.uid,
                'connection': "disconnected",
                'trasmission': "",
            })

            if self.auto_reconnect and trials <= 5:
                logger.log("info", f"Reconnecting ... trial: {trials}")
                trials += 1
                time.sleep(5)
                self.start_server(trials)

    def _read_data(self, sckt): 
        try:
            # read a frame
            return sckt.recv(RECV_BUFFER)
        except socket.timeout as e:
            logger.log("error", f"Socket timeout: {e}")
        except socket.error as e:
            logger.log("error", f"Socket error: {e}")
        except Exception as e:
            logger.log("error", f"Error reading data: {e}")

    def is_open(self):
        return self._buffer is not None

    def is_busy(self):
        return self.response is not None

    def open(self):
        logger.log("info", "Opening session")
        self._buffer = b''
        self.response = None
        self.establishment = False
          
        post_event(EventType.ACTIVITY_STREAM, **{
            'id': self.uid,
            'connection': "connected",
            'trasmission': "started",
        })
        
    def close(self):
        logger.log("info", "Closing session: neutral state")
        self._buffer = None
        self.establishment = False
        self._received_messages = list()
          
        post_event(EventType.ACTIVITY_STREAM, **{
            'id': self.uid,
            'connection': "connected",
            'trasmission': "ended",
        })

    def send_message(self, message: bytes | str | HL7Message):
        """Wraps a byte string, unicode string, or :py:class:`HL7Message`
        in a MLLP container and send the message to the server

        If message is a byte string, we assume it is already encoded properly.
        If message is unicode or  :py:class:`HL7Message`, it will be encoded
        according to  :py:attr:`hl7.client.MLLPClient.encoding`

        """
        
        if isinstance(message, bytes):
            # Assume we have the correct encoding
            binary = message
        else:
            # Encode the unicode message into a bytestring
            if isinstance(message, HL7Message):
                message = str(message)
            binary = message.encode(self.encoding)

        # wrap in MLLP message container
        data = SB + binary + EB + CR

        # convert to bytes
        # data = bytes(data, "utf-8")
        return self._send(data)

    def _send(self, data):
        """Low-level, direct access to the socket.send (data must be already
        wrapped in an MLLP container).  Blocks until the server returns.
        """
        # upload the data
        self.socket.send(data)

        # wait for the ACK/NACK
        if self.expect_ack:
            ACK = self.socket.recv(RECV_BUFFER)
            ACK = ACK.replace(SB, b"")
            ACK = ACK.replace(EB, b"")
            ACK = ACK.decode()

            # Returning ACK string
            return ACK

    def process(self, data: bytes) -> None:
        if data is None:
            return

        logger.log("info", f"Incoming data: {data}")
        if SB in data:
            self.handle_enq()
            self._buffer = b''
            self._get_message_id(data.strip(SB).decode(self.encoding))
        
        if self.establishment:
            # Establishment phase has been initiated already and we are now in Transfer phase
            
            # try to find a complete message(s) in the combined the buffer and data
            # usually should be broken up by EB, but I have seen FF separating messages: 
            # EB or EB if FF not in data else FF
            messages = (self._buffer + data).split(EB if FF not in data else FF)
            # whatever is in the last chunk is an uncompleted message, so put back
            # into the buffer
            self._buffer = messages.pop(-1)  

            for m in messages:
                # strip the rest of the MLLP shell from the HL7 message
                m = m.strip(SB) # SB or SB + CR

                # only handle messages with data
                if len(m) > 0:
                    self._received_messages.append(m)

            if EB in data:
                # Received an End Of Transmission. Resume and enter to neutral
                self.handle_eot()
                # logger.log("info", F"EOT {self._received_messages}")

            self.response = "ACK"
            return
        else:
            logger.log("info", "Establishment phase not initiated")
        
        self.response = "NACK"
        return

    def handle_enq(self):
        logger.log("debug", "Initiating Establishment Phase ...")
        if self.is_busy():
            """
            A receiver that cannot immediately receive information, replies with
            the <NAK> transmission control character. Upon receiving <NAK>, the 
            sender must wait at least 10 s before transmitting another <ENQ>
            """
            logger.log("info", " Receiver is busy")
            self.response = "NAK"
        else:
            """
            The system with information available initiates the establishment 
            phase. After the sender determines the data link is in a neutral 
            state, it transmits the <ENQ> transmission control character to the 
            intended receiver. Sender will ignore all responses other than 
            <ACK>, <NAK>, or <ENQ>.
            """
            logger.log("info", "Ready for Transfer Phase ...")
            self.establishment = True
            self.response = "ACK"

    def handle_eot(self):
        """Handles an End Of Transmission message
        """
        logger.log("info", "Transfer phase completed: handle_eot")
        msgs = []
        for m in self._received_messages:
            if isinstance(m, bytes):
                msgs.append(m.decode(self.encoding))
            else:
                msgs.append(m)
        
        self.show_message(msgs)
        self.eot_offload(self.uid, msgs)

        # Go to neutral state
        self.response = None
        self.close()

    def nack(self):
        logger.log("info", f"<- NACK : {self.msg_id}")
        nak = self._nack_msg(self.msg_id)
        self.send_message(nak)

    def ack(self):
        logger.log("info", f"<- ACK : {self.msg_id}")
        ack = self._ack_msg(self.msg_id)
        self.send_message(ack)

    def _get_message_id(self, message):
        # Split the HL7 message into segments
        segments = message.split('\r')

        # Find the MSH segment
        msh_segment = None
        for segment in segments:
            if segment.startswith('MSH'):
                msh_segment = segment
                break

        if msh_segment:
            # Split the MSH segment into fields
            fields = msh_segment.split('|')

            # Return the 10th field (Message Control ID)
            self.msg_id = fields[9] if len(fields) > 9 else None
        else:
            self.msg_id = None
        
    def _ack_msg(original_control_id, ack_code='AA', text_message='', error_code=''):
        ack = [
            f"MSH|^~\&|VLSM|VLSM|VLSM|VLSM|{datetime.now().strftime('%Y%m%d%H%M%S')}||ACK|{original_control_id}||2.7",
            f"MSA|{ack_code}|{original_control_id}|{text_message}|{error_code}"
        ]
        return '\r'.join(ack)

    def _nack_msg(original_control_id, text_message='', error_code=''):
        nack = [
            f"MSH|^~\&|VLSM|VLSM|VLSM|VLSM|{datetime.now().strftime('%Y%m%d%H%M%S')}||NACK|{original_control_id}||2.7",
            f"MSA|AR|{original_control_id}|{text_message}|{error_code}"
        ]
        return '\r'.join(nack)

    def get_response(self):
        if self.response:
            logger.log("debug", "<- {}".format(self.response))
        resp = self.response
        self.response = None
        return resp
    