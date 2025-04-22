from pydantic_settings import BaseSettings, SettingsConfigDict


class Configis(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    DATABASE_URL: str
