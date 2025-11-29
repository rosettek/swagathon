# migrations/env.py
from logging.config import fileConfig
from flask import current_app
from alembic import context

config = context.config
fileConfig(config.config_file_name)

def get_engine():
    return current_app.extensions['migrate'].db.get_engine()

def get_engine_url():
    return get_engine().url

def run_migrations_offline():
    url = get_engine_url()
    context.configure(url=url, target_metadata=None, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = get_engine()
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=None)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()