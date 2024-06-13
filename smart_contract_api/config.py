from functools import lru_cache
from smart_contract_api.lib.setting import EnvironmentSettings


class Settings(EnvironmentSettings):
    database_host: str
    database_user: str
    database_password: str
    database_name: str
    port: int
    public_key: str
    private_key: str
    web3_provider: str
    contract_address: str
    address_private_key: str
    from_address: str


@lru_cache()
def get_settings():
    return Settings()
