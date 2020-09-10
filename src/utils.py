SCRAPER_INFO_FILE_NAME = "apps"
SCRAPER_LOG_FILE_NAME = "logs"
CLASSIFIER_DATA_BUILDER_INFO_DIR = "info"


def get_app_icon_name(app_id: str) -> str:
    """Builds the corresponding app icon name from app id."""
    return f"icon_{app_id}"
