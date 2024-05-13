import socket

from hl7apy.parser import parse_message
from hl7apy.core import Message  as HL7Message

from flablink.gateway.link.base import AbstractLink
from flablink.gateway.extensions.event.base import EventType
from flablink.gateway.extensions.event.event import post_event
from flablink.gateway.link.schema import InstrumentConfig
from flablink.gateway.link.config import ProtocolType, SocketType
from flablink.gateway.link.config import NotConnectedException
from flablink.gateway.logger import Logger

logger = Logger(__name__, __file__)

ENQ = b"\x05"  # <ENQ>, enquiry
SB = b"\x0b"  # <SB>, vertical tab - start block
EB = b"\x1c"  # <EB>, file separator - end block
CR = b"\x0d"  # <CR>, \r - carriage return
FF = b"\x0c"  # <FF>, new page form feed
ACK = chr(0x06)  # ACK
NAK = chr(0x15)  # NAK
F_MIN = chr(0x20)   # content of LLP frame must be >= 0x20

RECV_BUFFER = 4096


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
        # Socket 
        self.socket = None
        self.is_connected = False
        self.encoding = "utf-8"
        #  buffer and messages
        self._buffer = b''
        self._messages = []
        # ACK
        self.expect_ack = False

    def start_server(self):
        while True:
            if not self.is_connected:
                self._connect()
                sckt = None
                if self.socket_type.lower() == SocketType.SERVER:
                    sckt, _ = self.socket.accept()
                else:
                    sckt = self.socket

            try:
                # read a frame
                data = sckt.recv(RECV_BUFFER)
                if data == b'':
                    logger.info("Connection closed")
                    self._disconnect()

                # Is this a new session?
                if not self.is_open():
                    self.open()

                self.process(data)

                # Does the receiver has to send something back?
                response = self.get_response()
                if response:
                    if isinstance(response, str):
                        # convert to bytes
                        response = response.encode()
                    self.send_message(response)

            except Exception as e:
                logger.error(f"Error reading data: {e}")
                self._disconnect()
       
    def _connect(self):
        match self.connection_type.lower():
            case SocketType.CLIENT:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
                self.is_connected = True
            case SocketType.SERVER:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.bind((self.host, self.port))
                self.socket.listen(1)
                self.is_connected = True
            case _:
                raise ValueError("Connection type must be either 'client' or 'server'")
            
        post_event(EventType.ACTIVITY_STREAM, {
            'id': self.uid,
            'message': 'connected',
            'connecting': False,
            'connected': True,
        })

    def _disconnect(self):
        if self.is_connected:
            self.socket.close()
            self.is_connected = False

            post_event(EventType.ACTIVITY_STREAM, {
                'id': self.uid,
                'message': 'disconnected',
                'connecting': False,
                'connected': False,
            })

    def is_open(self):
        return self._buffer is not None

    def is_busy(self):
        return self.response is not None

    def open(self):
        logger.log("info", "Opening session")
        self._buffer = b''
        self.response = None
        self.establishment = False

    def close(self):
        logger.log("info", "Closing session: neutral state")
        self.messages = None
        self.establishment = False

    def send_message(self, message: bytes | str | HL7Message):
        """Wraps a byte string, unicode string, or :py:class:`HL7Message`
        in a MLLP container and send the message to the server

        If message is a byte string, we assume it is already encoded properly.
        If message is unicode or  :py:class:`HL7Message`, it will be encoded
        according to  :py:attr:`hl7.client.MLLPClient.encoding`

        """
        if not self.is_connected:
            raise NotConnectedException
        
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

        if data == ENQ:
            self.handle_enq()
            return
        
        if self.establishment:
            # Establishment phase has been initiated already and we are now in
            # Transfer phase
            if data == SB:
                self._buffer = b''
                self._messages = []
                return 

            elif data == EB:
                # Received an End Of Transmission. Resume and enter to neutral
                self.handle_eot(self._messages)
                self._buffer = b''
                self._messages = []
                return 
            
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
                    # verify the message is valid
                    for c in m:
                        if not (c >= F_MIN or c == CR):
                            logger.log("error", "Invalid character in message")
                            self.response = NAK
                            break
                    if self.response == NAK:
                        break
                    
                    self._messages.append(m)

            if self.response != NAK:
                self.response = ACK
            # if self._messages:
            #     self.ack(data, 'AA')
            # else:
            #     self.ack(data, 'AE')

    def handle_enq(self):
        logger.log("debug", "Initiating Establishment Phase ...")
        if self.is_busy():
            """
            A receiver that cannot immediately receive information, replies with
            the <NAK> transmission control character. Upon receiving <NAK>, the 
            sender must wait at least 10 s before transmitting another <ENQ>
            """
            logger.log("info", " Receiver is busy")
            self.response = NAK
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
            self.response = ACK

    def handle_eot(self, messages):
        """Handles an End Of Transmission message
        """
        logger.log("info", "Transfer phase completed")
        super(SocketLink, self).handle_eot(messages)

        # Go to neutral state
        self.response = None
        self.close()

    def ack(self, raw, status , error=''):
        """Creates AA,AE or AR ACK message and returns it to sender"""
        ACK = ""
            
        # Get the field separator from MSH-1
        fld = raw[3:4]
        com = raw[4:5]

        # Finding the newline or return character
        if "\n" in raw:
            ret = "\n"
        else:
            ret = "\r"

        # Splitting segments
        segments = raw.split(ret)
        # Splitting MSH fields
        fields = segments[0].split(fld)
        i = 0
        MSH = ""
        while i < 12:
            if i == 8:
                # Changing MSH-9-1
                coms = fields[i].split(com)
                coms[0] = 'ACK'
                fields[i] = com.join(coms) 
            MSH += fields[i] + fld
            i += 1
        MSH = MSH[0:len(MSH) - 1]# Trimming last field character
        # Combining MSH segment with MSA segment
        # MSA|AA or AE or AR|MSH-10 value
        ACK = MSH + ret + "MSA" + fld + status + fld + fields[9] + fld + str(error) + ret

        self.write(ACK)
        # Returning ACK to use if they do it directly
        return ACK
    
    def get_response(self):
        if self.response:
            logger.log("debug", "<- {}".format(self.response))
        resp = self.response
        self.response = None
        return resp
    

# byte by byte reading

# def analyze_read_data(self, data):
# 	# Initialize empty lists to store HL7 messages and lines
# 	hl7_message = []
# 	hl7_line = b''

# 	# Iterate over each byte in the data sequence
# 	for datum in data:
# 		# Convert the byte to a character and encode it
# 		char = chr(datum).encode()

# 		# Check if the character indicates the start of an HL7 message
# 		if char == SB:
# 			# Reset the HL7 message and line lists
# 			hl7_message = []
# 			hl7_line = b''
# 			continue

# 		# Check if the character indicates the end of a line in the HL7 message
# 		if char == FF:
# 			# Append the current line to the HL7 message list and reset the line
# 			hl7_message.append(hl7_line)
# 			hl7_line = b''
# 			continue

# 		# Check if the character indicates the end of the HL7 message
# 		if char == self.EB:
# 			# Append the current line to the HL7 message list, process the complete message, and reset the lists
# 			hl7_message.append(hl7_line)
# 			self.process_hl7_message(hl7_message)
# 			hl7_message = []
# 			hl7_line = b''
# 			continue

# 		# If the character is none of the above, append it to the current line
# 		hl7_line += char




# JS TO PYTHON


# import asyncio
# import socket
# import serial
# from datetime import datetime
# from cryptography import random

# class InstrumentHandlerService:
#     def __init__(self, instrument_connection_service, parsers, result_order_service):
#         self.data = {}
#         self.ACK = b'\x06'
#         self.ENQ = b'\x05'
#         self.SOH = b'\x01'
#         self.STX = b'\x02'
#         self.ETX = b'\x03'
#         self.EOT = b'\x04'
#         (link unavailable) = b'\x13'
#         self.FS = b'\x25'
#         self.LF = b'\x10'
#         self.NAK = b'\x21'

#         self.instrument_connection_service = instrument_connection_service
#         self.parsers = parsers
#         self.result_order_service = result_order_service

#     def hex2ascii(self, hexx):
#         hex_str = hexx.decode('hex')
#         return ''.join([chr(int(hex_str[i:i+2], 16)) for i in range(0, len(hex_str), 2)])

#     def hl7ACK(self, messageID):
#         if not messageID or messageID == '':
#             messageID = random.getrandbits(64)
#         date = datetime.now().strftime('%Y%m%d%H%M%S')
#         ack = '\x0bMSH|^~\\&|FELICITY|FELICITY|FELICITY|FELICITY|' + date + '||ACK^R22^ACK|' + str(random.getrandbits(64)) + '|P|2.5.1||||||UNICODE UTF-8\x0d'
#         ack += 'MSA|AA|' + str(messageID) + '\x0d\x1c\x0d'
#         return ack

#     async def socketReader(self, data, instrument, clientSocket):
#         instance = None
#         if instrument.isClient:
#             instance = self.instrument_connection_service.getClientSession((link unavailable))
#         else:
#             instance = self.instrument_connection_service.getServerSession((link unavailable))

#         strData = instance['statements']

#         if instrument.protocol == 'hl7':
#             hl7Text = self.hex2ascii(data.hex())
#             strData += hl7Text
#             if '\x1c' in strData:
#                 strData = strData.replace('\x0b\x1c', '').strip().replace('\r\n\x0B\x0C\u0085\u2028\u2029', '\r')
#                 msgID = strData.split('\r')[0].split('|')[9]
#                 clientSocket.write(self.hl7ACK(msgID))
#                 final = self.parsers.parse(strData, instrument)
#                 if final:
#                     self.result_order_service.createAll(final)
#                 strData = ''
#         elif instrument.protocol == 'astm':
#             d = data.hex()
#             if d == '04':
#                 clientSocket.write(self.ACK)
#                 final = self.parsers.parse(strData, instrument)
#                 if final:
#                     self.result_order_service.createAll(final)
#                 strData = ''
#             elif d == '21':
#                 clientSocket.write(self.ACK)
#             else:
#                 text = self.hex2ascii(d)
#                 if text.startswith('\d*H'):
#                     text = '##START##' + text
#                 strData += text
#                 clientSocket.write(self.ACK)
#         self.instrument_connection_service.updateSerialSession((link unavailable), {'...instance': strData})

#     async def serialReader(self, data, instrument, sPort):
#         instance = self.instrument_connection_service.getSerialSession((link unavailable))
#         ACK_BUFFER = b'\x06'
#         ENQ = b'\x05'
#         STX = b'\x02'
#         ETX = b'\x03'
#         LF = b'\x10'
#         CR = b'\x13'
#         EOT = b'\x04'

#         strData = data.decode('ascii')
#         if strData == '':
#             return
#         if strData[0] == ENQ:
#             sPort.write(ACK_BUFFER)
#         elif strData[0] == EOT:
#             stringData = self.summarizeTransmission(instance)
#             final = self.parsers.parse(stringData, instrument)
#             if final:
#                 self.result_order_service.createAll(final)
#             instance['transmission'] = []
#             self.instrument_connection_service.updateSerialSession((link unavailable), {'...instance': instance})
#         else:
#             transmission = instance['transmission']
#             statement = instance['statement']
#             for char in strData:
#                 if char == STX:
#                     statement = {'hasStarted': True, 'hasEnded': False, 'dataMessage': '', 'checksum': ''}
#                 elif char == ETX:
#                     if not statement['hasStarted']:
#                         print('statement ended before it was started.')
#                         return
#                     statement['hasEnded'] = True
#                 elif char == LF:
#                     if