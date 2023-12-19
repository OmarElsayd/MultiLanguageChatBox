# pylint: disable=W0611, E1101
from logging.config import fileConfig

from alembic import context

from rtvt_services.config.get_creds import DbCreds
from rtvt_services.db_engine.engine import create_db_engine, ssh_db_engine
from rtvt_services.db_models import base, models
from rtvt_services.util.constant import DB_URL
from rtvt_services.util.constant import DB_SCHEMA

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = base.Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
db_creds = DbCreds()
schema = DB_SCHEMA


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    url = DB_URL.format(**db_creds.to_dict)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        include_schemas=True,
        version_table_schema=schema,
    )

    with context.begin_transaction():
        context.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
        context.execute(f"SET search_path TO {schema}")
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    engine_generator = ssh_db_engine()

    with engine_generator as connectable:
        connection = connectable.connect()

        try:
            context.configure(
                connection=connection, target_metadata=target_metadata,
                include_schemas=True,
                version_table_schema=schema,
            )

            with context.begin_transaction():
                context.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
                context.execute(f"SET search_path TO {schema}")
                context.run_migrations()

        finally:
            connection.close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
