from functools import lru_cache
from logging.config import dictConfig
from typing import Optional
import logging
import os

from fastapi_mail import ConnectionConfig
from pydantic import BaseSettings, EmailStr, Field, validator

from app.utils.enums import AppEnv, AppEnvPath, StorageType

MODE = os.getenv('MODE', AppEnv.DEV)


class Base(BaseSettings):
    class Config:
        env_file = f'{os.getcwd()}/{AppEnvPath[MODE]}'


class MailSettings(Base):
    username: str = Field(env='MAIL_USERNAME', description='帳號')
    password: str = Field(env='MAIL_PASSWORD', description='密碼')
    from_name: str = Field(env='MAIL_FROM_NAME', description='信件標題')


class PostgresSQL(Base):
    username: str = Field(env='POSTGRESQL_USERNAME', description='帳號')
    password: str = Field(env='POSTGRESQL_PASSWORD', description='密碼')
    host: str = Field(env='POSTGRESQL_HOST', description='位置')
    port: str = Field(env='POSTGRESQL_PORT', description='埠')
    db: str = Field(env='POSTGRESQL_DB', description='DB名稱')

    @property
    def url(self) -> str:
        return f'postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.db}'


class Redis(Base):
    host: str = Field(env='REDIS_HOST', description='位置')
    port: str = Field(env='REDIS_PORT', description='埠')

    @property
    def url(self) -> str:
        return f'redis://{self.host}:{self.port}/'


class Domain(Base):
    host: str = Field(env='DOMAIN_HOST', description='位置')
    port: int = Field(env='DOMAIN_PORT', description='埠')
    ssl: str = Field(env='DOMAIN_SSL')

    @property
    def url(self) -> str:
        return f'{self.ssl}://{self.host}:{self.port}'


class OAuth(Base):
    google_id: Optional[str] = Field(env='GOOGLE_OAUTH_CLIENT_ID')
    google_secret: Optional[str] = Field(env='GOOGLE_OAUTH_CLIENT_SECRET')
    github_id: Optional[str] = Field(env='GITHUB_OAUTH_CLIENT_ID')
    github_secret: Optional[str] = Field(env='GITHUB_OAUTH_CLIENT_SECRET')
    github_associate_id: Optional[str] = Field(env='GITHUB_OAUTH_ASSOCIATE_CLIENT_ID')
    github_associate_secret: Optional[str] = Field(env='GITHUB_OAUTH_ASSOCIATE_CLIENT_SECRET')
    microsoft_id: Optional[str] = Field(env='MICROSOFT_OAUTH_CLIENT_ID')
    microsoft_secret: Optional[str] = Field(env='MICROSOFT_OAUTH_CLIENT_SECRET')

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
    LOG_LEVEL: str = Field(default='DEBUG', env='LOG_LEVEL')
    version = 1
    disable_existing_loggers = False
    formatters = {
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    }
    handlers = {
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
    cert: str = Field(env='GC_STORGE_CERT')
    BUCKET_NAME: str = Field(env='GC_STORAGE_BUCKET_NAME')


class Settings(Base):
    redis: Redis = Field(default_factory=Redis)
    pg: PostgresSQL = Field(default_factory=PostgresSQL)
    mail: MailSettings = Field(default_factory=MailSettings)
    project: str = Field(env='PROJECT')
    server_host: str = Field(env='SERVER_HOST')
    server_port: str = Field(env='SERVER_PORT')
    domain: str = Field(env='DOMAIN')
    oauth: OAuth = Field(default_factory=OAuth)
    logger: LogConfig = Field(default_factory=LogConfig)
    app_env: AppEnv = Field(env='APP_ENV')
    storage: StorageType = Field(env='STORAGE')
    token_key_prefix: str = Field(env='TOKEN_KEY_PREFIX', default='acs_token:')

    @validator('domain')
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
        MAIL_FROM=EmailStr(mail.username),
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
