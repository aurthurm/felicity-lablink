from flablink.gateway.logger import Logger

logger = Logger(__name__, __file__)

from .seed import (
    seed_link_settings,
    seed_lims_settings,
    seed_keyword_mappings,
    seed_result_exclusions,
    seed_result_translations
)


def seed_all():
    logger.log("info", "Seeding all...")
    seed_link_settings()
    seed_lims_settings()
    seed_keyword_mappings()
    seed_result_exclusions()
    seed_result_translations()
    logger.log("info", "Done Seeding all...")
