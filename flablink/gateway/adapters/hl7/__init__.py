# -*- coding: utf-8 -*-
from flablink.gateway.adapters.hl7.roche import RocheCOBAS68008800Hl7Adapter
from flablink.gateway.adapters.hl7.generic import GenericHl7Adapter

hl7_adapters = [RocheCOBAS68008800Hl7Adapter, GenericHl7Adapter]
