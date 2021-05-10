import os
import sqlalchemy
import requests
from dateutil.parser import parse as date_parse
import dateutil.tz
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import select
from sqlalchemy.orm import Session
from hearings_lib.hearings.load_project_env import load_project_env
from hearings_lib.db_models import (
    Base,
    Hearing
)
from hearings_lib.db_handler import DB_Handler
from hearings_lib.api_client import APIClient


def get_package_summaries_by_congress(congress: int, config_directory: str = ''):
    config = load_project_env(config_directory)
    db_config = config['govinfo_db']
    # Python automatically concatenates strings within brackets that aren't comma-separated.
    # This string definition is broken up due to line-length
    connection_uri = (
        f'{db_config["db_type"]}'
        f'+{db_config["db_driver"]}'
        f'://{db_config["user"]}'
        f':{os.getenv("DB_POSTGRES_PW")}@{db_config["host"]}/{db_config["name"]}'
    )

    engine = sqlalchemy.create_engine(connection_uri, future=True)
    if not database_exists(connection_uri):
        create_database(connection_uri)
    Base.metadata.create_all(engine)

    handler = DB_Handler(engine)

    with Session(handler.engine) as db:
        existing_packages = {i[0]: i[1] for i in db.execute(select(Hearing.package_id, Hearing.last_modified))}

    with requests.Session() as s:
        client = APIClient(api_key=os.getenv('GPO_API_KEY'), session=s)
        packages = []
        for i in range(118):
            new_or_modified_packages = [
                i for i in client.get_package_ids_by_congress(i)
                if i['packageId'] not in existing_packages
                or date_parse(i['lastModified'])
                > existing_packages[i['packageId']].replace(tzinfo=dateutil.tz.tzlocal())
            ]

            packages = packages + new_or_modified_packages
        package_summaries = client.get_package_summaries(packages=packages)

    handler.sync_hearing_records(package_summaries)
