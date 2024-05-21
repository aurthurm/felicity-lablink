# -*- coding: utf-8 -*-
import typer

from flablink.gateway.services.transformer import Transformer
from flablink.gateway.link import SerialLink, SocketLink
from flablink.gateway.link.schema import InstrumentConfig
from flablink.gateway.models import RawData, Order
from flablink.gateway.logger import Logger

logger = Logger(__name__, __file__)
app = typer.Typer()

@app.command
def fix():
    """Fix messages imported earlier"""
    raw_data = RawData.all()
    for _raw in raw_data:
        Transformer().update_fix(_raw)

@app.command
def replay():
    """Replay results reimport from raw_data"""
    for _order in Order().all():
        _order.delete()

    raw_data = RawData.all()
    for _raw in raw_data:
        Transformer().handle_replay(_raw)

@app.command
def transform(message: str):
    """Test a message and see how it gets transformed"""
    msg = Transformer().adapter.process(message)
    logger.log("info", f"{msg}")

@app.command
def serial(uid: int, name: str, code: str, path: str = "/dev/tty/USB0", baud: int = 9600, protocol: str = "astm"):
    """Serial Interface connection"""
    # TODO add this instrumet to db if not exist
    cfg = InstrumentConfig(uid=uid,code=code,name=name,path=path,baud_rate=baud, protocol_type=protocol)
    link = SerialLink(instrument_config=cfg, emit_events=False)
    link.start_server()

@app.command
def tcpip(uid: int, name: str, code: str, address: str, port: int, socket: str, protocol: str = "hl7"):
    """TCPIP Interface conection"""
    # TODO add this instrumet to db if not exist
    cfg = InstrumentConfig(uid=1010,code=code,name=name,address=address,port=port,socket_type=socket, protocol_type=protocol)
    link = SocketLink(instrument_config=cfg, emit_events=False)
    link.start_server()


if __name__ == "__main__":
    app()
