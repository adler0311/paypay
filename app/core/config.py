import secrets
from typing import Optional

from pydantic import PostgresDsn, model_validator, MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    MYSQL_SERVER: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str
    MYSQL_TEST_DB: str | None = None
    MYSQL_PORT: str
    MYSQL_DATABASE_URI: str | None = None
    MYSQL_TEST_DATABASE_URI: str | None = None

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    @model_validator(mode='after')
    def assemble_db_connection(self):
        self.MYSQL_DATABASE_URI = f'mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_SERVER}:{self.MYSQL_PORT}/{self.MYSQL_DB}'
        self.MYSQL_TEST_DATABASE_URI = f'mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_SERVER}:{self.MYSQL_PORT}/{self.MYSQL_TEST_DB}'
        return self


settings = Settings()
