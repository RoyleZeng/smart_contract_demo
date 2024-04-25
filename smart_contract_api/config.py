from functools import lru_cache
from smart_contract_api.lib.setting import EnvironmentSettings


class Settings(EnvironmentSettings):
    database_host: str
    database_user: str
    database_password: str
    database_name: str
    port: int
    jwt_public_key: str
    jwt_private_key: str


@lru_cache()
def get_settings():
    return Settings()
