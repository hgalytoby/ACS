from __future__ import with_statement

from logging.config import fileConfig
import asyncio
import pathlib
import sys

from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncEngine

from alembic import context
from app.core.config import settings
from app.models import *  # necessarily to import something from file where your models are stored

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = settings.pg.url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        expression_type=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        expression_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = AsyncEngine(
        create_engine(
            settings.pg.url,
            echo=True,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
