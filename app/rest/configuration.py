from pydantic import BaseSettings


class Configuration(BaseSettings):
    some_string: str  # must be overridden by environment variable or startup fails
    some_string_with_default: str = "Nyan Cat"
    some_integer_with_default: int = 1138

    class Config:
        env_file = "configuration.env"
