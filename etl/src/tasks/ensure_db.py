#!/usr/bin/env python
import logging.config

import alembic.config
from sqlalchemy import create_engine

from persistence.repository import Repository

logging.config.fileConfig("aggregator.logging.conf")

repository = Repository.provide()

try:
    repository.execute("select 1")
except Exception:
    logging.info(f"Was not able to run a test query. Possibly due to missing DB. Attempting to create one now")

    try:
        connection_str = repository.connection_string
        [connection_str, database_name] = connection_str.rsplit("/", 1)
    except Exception as err:
        logging.error(
            f"Was not able to split connection string into "
            f"connection string and database name: {repository.connection_string}"
        )
        raise

    try:
        engine = create_engine(connection_str, isolation_level="AUTOCOMMIT")
        engine.execute(f"create database {database_name}")

        logging.info(f"Database {database_name} has been successfully created")
    except Exception as err:
        logging.error(
            f"Was not able to create a database. "
            f"Possibly due to insufficient permissions"
        )
        raise

alembic_args = [
    'upgrade',
    'head'
]

alembic.config.main(argv=alembic_args)

logging.info(f"Database exists and updated to use the latest schema definition")
