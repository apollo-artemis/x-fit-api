from logging.config import fileConfig

from alembic import context
from db.conn import Base
from sqlalchemy import engine_from_config, pool
from db import schemas
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# if config.config_file_name is not None:
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
target_metadata = schemas.Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

import os

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # url = config.get_main_option("sqlalchemy.url")
    url = os.getenv("DATABASE_URL")
    url = "mysql+pymysql://root:9BmwoAFdYgcN4kJhECUG@172.25.0.2:3306/x-fit?charset=utf8mb4"
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    config_section = config.get_section(config.config_ini_section)
    # print(config_section["sqlalchemy.url"])
    url = os.getenv("DATABASE_URL")
    url = "mysql://root:98mwoAFdYgcN4kJhECUG@172.18.0.2:3306/x-fit?charset=utf8mb4"

    config_section["sqlalchemy.url"] = url
    # 위 3줄 새로 추가
    connectable = engine_from_config(
        # config.get_section(config.config_ini_section),
        config_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# if context.is_offline_mode():
#     run_migrations_offline()
# else:
run_migrations_online()
# run_migrations_offline()