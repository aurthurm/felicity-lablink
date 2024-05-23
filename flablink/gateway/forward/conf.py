from functools import lru_cache
from enum import IntEnum

from flablink.gateway.services.settings import LimsSettings, LimsSettingsService
from flablink.gateway.services.settings import LinkSettings, LinkSettingsService
from flablink.gateway.services.order.other import ResultTranslationService
from flablink.gateway.services.order.other import KeywordMappingService
from flablink.gateway.services.order.other import ResultExclusionsService


class SyncStatus(IntEnum):
    PENDING = 0
    SYNCED = 1
    SKIPPED = 2


# @lru_cache
def get_lims_settings() -> LimsSettings:
    lss = LimsSettingsService().first()
    if not lss:
        raise Exception("LIMS Settings are required")
    return lss
LIMS_SETTINGS = get_lims_settings()


# @lru_cache
def get_link_settings() -> LinkSettings:
    lss = LinkSettingsService().first()
    if not lss:
        raise Exception("LINK Settings are required")
    return lss
LINK_SETTINGS = get_link_settings()


# @lru_cache
def get_translations():
    translation_service = ResultTranslationService()
    translations = translation_service.find_all()
    INTEPRETATIONS = {}
    for _item in translations:
        INTEPRETATIONS[_item.original] = _item.translated
    return INTEPRETATIONS
INTEPRETATIONS = get_translations()


# @lru_cache
def get_keyword_mappings():
    re_service = KeywordMappingService()
    mappings = re_service.find_all()
    KEYWORDS_MAPPING = {}
    for _item in mappings:
        KEYWORDS_MAPPING[_item.keyword] = ','.join(_item.mappings)
    return KEYWORDS_MAPPING
KEYWORDS_MAPPING = get_keyword_mappings()


# @lru_cache
def get_exclusions():
    re_service = ResultExclusionsService()
    exclusions = re_service.find_all()
    return list(map(lambda x: x.result, exclusions))
EXCLUDE_RESULTS = get_exclusions()