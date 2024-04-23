import json
from pathlib import Path
from typing import Any, Dict, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentParameter(BaseSettings):
    version: str = 'develop'
    stage: str = 'local'


default_environment_parameter = EnvironmentParameter()


class EnvironmentSettings(BaseSettings):
    class Config:
        env_file = f'config.{default_environment_parameter.stage}.env'
        extra = "allow"


def json_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    """
    A simple settings source that loads variables from a JSON file
    at the project's root.

    Here we happen to choose to use the `env_file_encoding` from Config
    when reading `.json`
    """
    encoding = settings.__config__.env_file_encoding
    file_path = settings.__config__.env_file
    return json.loads(Path(file_path).read_text(encoding))


class JsonSettings(BaseSettings):
    class Config:
        env_file = f'config.{default_environment_parameter.stage}.json'
        env_nested_delimiter = '__'

        @classmethod
        def customise_sources(
                cls,
                init_settings,
                env_settings,
                file_secret_settings,
        ):
            """When env_settings.env_file has a value, the json file will be parsed by env format"""
            if env_settings.env_file:
                cls.env_file = env_settings.env_file
                env_settings.env_file = None
            return (
                init_settings,
                env_settings,
                json_config_settings_source,
                file_secret_settings,
            )
