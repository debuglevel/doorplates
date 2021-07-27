from functools import lru_cache
import logging.config

from pydantic import BaseSettings


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@lru_cache()
def get_configuration():
    logger.debug("Getting configuration...")
    return Configuration()


class Configuration(BaseSettings):
    inkscape_url: str

    class Config:
        env_file = "configuration.env"
