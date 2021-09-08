import logging.config
import os
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


def ensure_directory_exists(path: str):
    logger.debug(f"Ensure configured directory {path} exists...")

    if not os.path.isdir(path):
        logger.warning(f"Configured directory '{path}' does not exist, creating directory...")
        os.makedirs(path, exist_ok=True)


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
        else:
            doorplates_directory = self.doorplates_directory
            logger.debug(f"Doorplates directory specified: {doorplates_directory}")

        ensure_directory_exists(doorplates_directory)
        return doorplates_directory

    def get_templates_directory(self):
        if self.templates_directory is None:
            templates_directory = f"{self.data_directory}/templates/"
            logger.debug(f"Templates directory not specified. Using data directory: {templates_directory}")
        else:
            templates_directory = self.templates_directory
            logger.debug(f"Templates directory specified: {self.templates_directory}")

        ensure_directory_exists(templates_directory)
        return templates_directory

    class Config:
        env_file = "configuration.env"
