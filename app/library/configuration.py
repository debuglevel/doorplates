import logging.config
from functools import lru_cache

from pydantic import BaseSettings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# TODO: it might be nice to incorporate dependency injection to override settings in testing:
#  https://fastapi.tiangolo.com/advanced/settings/#settings-and-testing
#  but that might also be possible without dependency injection.


@lru_cache()
def get_configuration():
    logger.debug("Getting configuration...")
    return Configuration()


class Configuration(BaseSettings):
    inkscape_url: str
    templates_directory: str = "data/templates/"
    doorplates_directory: str = "data/doorplates/"

    class Config:
        env_file = "configuration.env"
