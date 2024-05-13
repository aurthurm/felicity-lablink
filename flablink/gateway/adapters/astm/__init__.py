# -*- coding: utf-8 -*-
from flablink.gateway.adapters.astm.abbott import AbbotM2000ASTMAdapter
from flablink.gateway.adapters.astm.panther import PantherASTMAdapter
from flablink.gateway.adapters.astm.roche import RocheASTMPlusAdapter

astm_adapters = [AbbotM2000ASTMAdapter,
                 PantherASTMAdapter, RocheASTMPlusAdapter]
