from pydantic_settings import BaseSettings
from sentinelhub import SHConfig


class Settings(BaseSettings):
    app_name: str = "Fastapi config"
    debug: bool = False
    copernicus_client_id: str = "test"
    copernicus_secret: str = "test"

    class Config:
        env_file = ".env"

    def prepare_sh_config(self) -> SHConfig:
        config = SHConfig()
        config.sh_client_id = self.copernicus_client_id
        config.sh_client_secret = self.copernicus_secret
        config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
        config.sh_base_url = "https://sh.dataspace.copernicus.eu"
        config.save("cdse")

        return config
