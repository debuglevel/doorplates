import logging.config
from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# TODO: it might be nice to incorporate dependency injection to override settings in testing:
#  https://fastapi.tiangolo.com/advanced/settings/#settings-and-testing
#  but that might also be possible without dependency injection.


@lru_cache()
def get_configuration():
    logger.debug("Getting configuration...")
    configuration = Configuration()
    logger.debug(f"Got configuration: {configuration}")
    return configuration


class Configuration(BaseSettings):
    inkscape_url: str
    data_directory: str = "data/"
    doorplates_directory: Optional[str]
    templates_directory: Optional[str]
    rendering_backend: str = "inkscape-microservice"
    # rendering_backend: str = "inkscape"
    # rendering_backend: str = "cairosvg"
    # rendering_backend: str = "svglib"

    def get_doorplates_directory(self):
        if self.doorplates_directory is None:
            doorplates_directory = f"{self.data_directory}/doorplates/"
            logger.debug(f"Doorplates directory not specified. Using data directory: {doorplates_directory}")
            return doorplates_directory
        else:
            logger.debug(f"Doorplates directory specified: {self.doorplates_directory}")
            return self.doorplates_directory

    def get_templates_directory(self):
        if self.templates_directory is None:
            templates_directory = f"{self.data_directory}/templates/"
            logger.debug(f"Templates directory not specified. Using data directory: {templates_directory}")
            return templates_directory
        else:
            logger.debug(f"Templates directory specified: {self.templates_directory}")
            return self.templates_directory

    class Config:
        env_file = "configuration.env"
