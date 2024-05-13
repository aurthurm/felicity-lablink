from .seed import (
    seed_link_settings,
    seed_lims_settings,
    seed_keyword_mappings,
    seed_result_exclusions,
    seed_result_translations
)


def seed_all():
    seed_link_settings()
    seed_lims_settings()
    seed_keyword_mappings()
    seed_result_exclusions()
    seed_result_translations()
