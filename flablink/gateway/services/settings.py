from flablink.gateway.models import LinkSettings, LimsSettings
from flablink.gateway.logger import Logger
from flablink.gateway.services.base import BaseService

logger = Logger(__name__, __file__)


class LinkSettingsService(BaseService[LinkSettings]):
    def __init__(self):
        super().__init__(LinkSettings)


class LimsSettingsService(BaseService[LimsSettings]):
    def __init__(self):
        super().__init__(LimsSettings)