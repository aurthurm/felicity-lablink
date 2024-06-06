from flablink.gateway.models import (
    ResultExclusions,
    ResultTranslation,
    KeywordMapping
)
from flablink.gateway.logger import Logger
from flablink.gateway.services.base import BaseService


logger = Logger(__name__, __file__)


class ResultExclusionsService(BaseService[ResultExclusions]):
    def __init__(self):
        super().__init__(ResultExclusions)


class ResultTranslationService(BaseService[ResultTranslation]):
    def __init__(self):
        super().__init__(ResultTranslation)


class KeywordMappingService(BaseService[KeywordMapping]):
    def __init__(self):
        super().__init__(KeywordMapping)
