# -*- coding: utf-8 -*-

import argparse

from flablink.gateway.logger import Logger
logger = Logger(__name__, __file__)

def main():

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-s",
        "--server",
        action="store_true",
        help="Start the serial server tool"
    )

    parser.add_argument(
        "-p",
        "--port",
        type=str,
        default="/dev/ttys002",
        help="COM Port to connect"
    )

    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List available ports"
    )

    parser.add_argument(
        "-f",
        "--forward",
        action="store_true",
        help="Foward Results to LIMS"
    )

    parser.add_argument(
        "-d",
        "--dashboard",
        action="store_true",
        help="Start Admin Dashboard"
    )

    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Start All"
    )

    parser.add_argument(
        "-fm",
        "--fixmessages",
        action="store_true",
        help="Fix messages imported earlier"
    )

    parser.add_argument(
        "-r",
        "--replay",
        action="store_true",
        help="Repley messages import"
    )

    args = parser.parse_args()


    # fix messages imported earlier
    if args.fixmessages:
        from flablink.gateway.services.transformer import Transformer
        from flablink.gateway.models import RawData
        raw_data = RawData.all()
        for _raw in raw_data:
            Transformer().update_fix(_raw)

    # replay reimport results for raw_data
    if args.replay:
        from flablink.gateway.services.transformer import Transformer
        from flablink.gateway.models import RawData, Order
        for _order in Order().all():
            _order.delete()

        raw_data = RawData.all()
        for _raw in raw_data:
            Transformer().handle_replay(_raw)