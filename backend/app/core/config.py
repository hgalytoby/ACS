import os
import logging
from logging.config import dictConfig
from functools import lru_cache
from fastapi_mail import ConnectionConfig
from pydantic import BaseSettings, Field, EmailStr, validator

from app.utils.enums import AppEnv, StorageType

env_dev = f'{os.getcwd()}/.env.dev'

env_prod = f'{os.getcwd()}/.env'


class Base(BaseSettings):
    class Config:
        env_file = env_prod if os.getenv('MODE') == 'PROD' else env_dev


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
    google_id: str = Field(env='GOOGLE_OAUTH_CLIENT_ID')
    google_secret: str = Field(env='GOOGLE_OAUTH_CLIENT_SECRET')
    github_id: str = Field(env='GITHUB_OAUTH_CLIENT_ID')
    github_secret: str = Field(env='GITHUB_OAUTH_CLIENT_SECRET')
    facebook_id: str = Field(env='FACEBOOK_OAUTH_CLIENT_ID')
    facebook_secret: str = Field(env='FACEBOOK_OAUTH_CLIENT_SECRET')

    @property
    def google(self) -> tuple[str, str]:
        return self.google_id, self.google_secret

    @property
    def github(self) -> tuple[str, str]:
        return self.github_id, self.github_secret

    @property
    def facebook(self) -> tuple[str, str]:
        return self.facebook_id, self.facebook_secret


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

    @validator('domain')
    def _domain(cls, v, values) -> str:
        if not v:
            return f'http://{values["server_host"]}:{values["server_port"]}'
        return v


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
