from functools import lru_cache

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.paths import ENV_PATH

settings_config_dict = SettingsConfigDict(
    env_file=ENV_PATH,
    env_file_encoding='utf-8',
    validate_default=False,
    extra="ignore",
)


class SettingsModel(BaseSettings):
    model_config = settings_config_dict

class PostgresSettings(SettingsModel):
    driver: str = "postgresql+asyncpg"
    username: str = Field(default=None, validation_alias="POSTGRES_USER")
    password: str = Field(default=None, validation_alias="POSTGRES_PASSWORD")
    host: str = Field(default=None, validation_alias="POSTGRES_HOST")
    port: int = Field(default=None, validation_alias="POSTGRES_PORT")
    database: str = Field(default=None, validation_alias="POSTGRES_DB")

class Settings(BaseModel):
    postgres: PostgresSettings = PostgresSettings()

    @property
    def postgres_dsn(self) -> str:
        return PostgresDsn.build(
            scheme=self.postgres.driver,
            username=self.postgres.username,
            password=self.postgres.password,
            host=self.postgres.host,
            port=self.postgres.port,
            path=self.postgres.database,
        ).unicode_string()
    
@lru_cache(maxsize=4)
def get_app_settings() -> Settings:
    return Settings()



