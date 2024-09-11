from functools import lru_cache
from logging.config import dictConfig
from typing import Optional
import logging
import os

from fastapi_mail import ConnectionConfig
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils.enums import AppEnv, AppEnvPath, StorageType

MODE = os.getenv('MODE', AppEnv.DEV)


class Base(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f'{os.getcwd()}/{AppEnvPath[MODE]}',
        extra='ignore',
    )


class MailSettings(Base):
    username: str = Field(alias='MAIL_USERNAME', description='帳號')
    password: str = Field(alias='MAIL_PASSWORD', description='密碼')
    from_name: str = Field(alias='MAIL_FROM_NAME', description='信件標題')


class PostgresSQL(Base):
    username: str = Field(alias='POSTGRESQL_USERNAME', description='帳號')
    password: str = Field(alias='POSTGRESQL_PASSWORD', description='密碼')
    host: str = Field(alias='POSTGRESQL_HOST', description='位置')
    port: str = Field(alias='POSTGRESQL_PORT', description='埠')
    db: str = Field(alias='POSTGRESQL_DB', description='DB名稱')

    @property
    def url(self) -> str:
        return f'postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.db}'


class Redis(Base):
    host: str = Field(alias='REDIS_HOST', description='位置')
    port: str = Field(alias='REDIS_PORT', description='埠')

    @property
    def url(self) -> str:
        return f'redis://{self.host}:{self.port}/'


class Domain(Base):
    host: str = Field(alias='DOMAIN_HOST', description='位置')
    port: int = Field(alias='DOMAIN_PORT', description='埠')
    ssl: str = Field(alias='DOMAIN_SSL')

    @property
    def url(self) -> str:
        return f'{self.ssl}://{self.host}:{self.port}'


class OAuth(Base):
    google_id: Optional[str] = Field(alias='GOOGLE_OAUTH_CLIENT_ID')
    google_secret: Optional[str] = Field(alias='GOOGLE_OAUTH_CLIENT_SECRET')
    github_id: Optional[str] = Field(alias='GITHUB_OAUTH_CLIENT_ID')
    github_secret: Optional[str] = Field(alias='GITHUB_OAUTH_CLIENT_SECRET')
    github_associate_id: Optional[str] = Field(
        alias='GITHUB_OAUTH_ASSOCIATE_CLIENT_ID',
    )
    github_associate_secret: Optional[str] = Field(
        alias='GITHUB_OAUTH_ASSOCIATE_CLIENT_SECRET',
    )
    microsoft_id: Optional[str] = Field(alias='MICROSOFT_OAUTH_CLIENT_ID')
    microsoft_secret: Optional[str] = Field(
        alias='MICROSOFT_OAUTH_CLIENT_SECRET'
    )

    @property
    def google(self) -> tuple[str, str]:
        return self.google_id, self.google_secret

    @property
    def github(self) -> tuple[str, str]:
        return self.github_id, self.github_secret

    @property
    def github_associate(self) -> tuple[str, str]:
        return self.github_associate_id, self.github_associate_secret

    @property
    def microsoft(self) -> tuple[str, str]:
        return self.microsoft_id, self.microsoft_secret


class LogConfig(Base):
    LOG_NAME: str = 'app.main:app'
    LOG_FORMAT: str = '%(levelprefix)s | %(asctime)s | %(message)s'
    LOG_LEVEL: str = Field(default='DEBUG', alias='LOG_LEVEL')
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    }
    handlers: dict = {
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },
    }

    def get_dict_config(self) -> dict:
        config = self.dict()
        config['loggers'] = {
            self.LOG_NAME: {
                'handlers': ['default'],
                'level': self.LOG_LEVEL,
            },
        }
        return config


class GCStorage(Base):
    cert: str = Field(alias='GC_STORGE_CERT')
    BUCKET_NAME: str = Field(alias='GC_STORAGE_BUCKET_NAME')


class Settings(Base):
    redis: Redis = Field(default_factory=Redis)
    pg: PostgresSQL = Field(default_factory=PostgresSQL)
    mail: MailSettings = Field(default_factory=MailSettings)
    project: str = Field(alias='PROJECT')
    server_host: str = Field(alias='SERVER_HOST')
    server_port: str = Field(alias='SERVER_PORT')
    domain: str = Field(alias='DOMAIN')
    oauth: OAuth = Field(default_factory=OAuth)
    logger: LogConfig = Field(default_factory=LogConfig)
    app_env: AppEnv = Field(alias='APP_ENV')
    storage: StorageType = Field(alias='STORAGE')
    token_key_prefix: str = Field(
        alias='TOKEN_KEY_PREFIX',
        default='acs_token:',
    )

    @model_validator(mode='after')
    @classmethod
    def _domain(cls, v, values) -> str:
        if not v:
            return f'http://{values["server_host"]}:{values["server_port"]}'
        return v

    @property
    def is_dev(self) -> bool:
        return self.app_env == AppEnv.DEV

    @property
    def is_prod(self) -> bool:
        return self.app_env == AppEnv.PROD


@lru_cache()
def get_settings() -> Settings:
    return Settings()


@lru_cache()
def get_logger() -> logging:
    dictConfig(settings.logger.get_dict_config())
    return logging.getLogger(settings.logger.LOG_NAME)


@lru_cache()
def get_email_config() -> ConnectionConfig:
    mail = get_settings().mail
    return ConnectionConfig(
        MAIL_USERNAME=mail.username,
        MAIL_PASSWORD=mail.password,
        MAIL_FROM=mail.username,
        MAIL_PORT=587,
        MAIL_SERVER='smtp.gmail.com',
        MAIL_FROM_NAME=mail.from_name,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
    )


settings = get_settings()
email_config = get_email_config()
logger = get_logger()
