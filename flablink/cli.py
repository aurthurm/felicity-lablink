# -*- coding: utf-8 -*-
import typer
import uvicorn

from flablink.gateway.models import RawData, Order
from flablink.gateway.logger import Logger

logger = Logger(__name__, __file__)
app = typer.Typer()


@app.command()
def seed():
    from flablink.gateway.seeder import seed_all
    seed_all()

@app.command()
def replay_orders():
    """Fix messages imported earlier"""
    from flablink.gateway.services.transformer import Transformer
    orders = Order.all()
    for _order in orders:
        Transformer().replay_order(_order)

@app.command()
def replay_rawdata():
    """Replay results reimport from raw_data"""
    from flablink.gateway.services.transformer import Transformer
    for _order in Order().all():
        _order.delete()

    raw_data = RawData.all()
    for _raw in raw_data:
        Transformer().replay_raw(_raw)

@app.command()
def transform(message: str):
    """Test a message and see how it gets transformed"""
    from flablink.gateway.services.transformer import Transformer
    msg = Transformer().adapter.process(message)
    logger.log("info", f"{msg}")

@app.command()
def serial(uid: int, name: str, code: str, path: str = "/dev/tty/USB0", baud: int = 9600, protocol: str = "astm"):
    """Serial Interface connection"""
    from flablink.gateway.link import SerialLink
    from flablink.gateway.link.schema import InstrumentConfig
    # TODO add this instrumet to db if not exist
    cfg = InstrumentConfig(uid=uid,code=code,name=name,path=path,baud_rate=baud, protocol_type=protocol)
    link = SerialLink(instrument_config=cfg, emit_events=False)
    link.start_server()

@app.command()
def tcpip(uid: int, name: str, code: str, address: str, port: int, socket: str, protocol: str = "hl7"):
    """TCPIP Interface conection"""
    from flablink.gateway.link import SocketLink
    from flablink.gateway.link.schema import InstrumentConfig
    # TODO add this instrumet to db if not exist
    cfg = InstrumentConfig(uid=1010,code=code,name=name,address=address,port=port,socket_type=socket, protocol_type=protocol)
    link = SocketLink(instrument_config=cfg, emit_events=False)
    link.start_server()

@app.command()
def serve(host:str="127.0.0.1", port:int=80):
    uvicorn.run("flablink.main:app", host=host, port=port, reload=False)


def main(): app()

if __name__ == "__main__": app()
