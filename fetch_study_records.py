import os
import sqlalchemy
import requests
import csv
import pickle
from dateutil.parser import parse as date_parse
import dateutil.tz
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import select
from sqlalchemy.orm import Session
from hearings_lib.hearings.load_project_env import ProjectEnv
from hearings_lib.db_models import (
    Base,
    Hearing
)
from hearings_lib.db_handler import DB_Handler
from hearings_lib.api_client import APIClient


def main():
    ProjectEnv.load_env()
    config = ProjectEnv.get_config()
    db_config = config['govinfo_db']
    # Python automatically concatenates strings within brackets that aren't comma-separated.
    # This string definition is broken up due to line-length
    connection_uri = (
        'postgresql+psycopg2://'
        f'{db_config["user"]}'
        f':{os.getenv("DB_POSTGRES_PW")}'
        f'@{db_config["host"]}'
        '/study_test'
    )

    engine = sqlalchemy.create_engine(connection_uri, future=True)
    if not database_exists(connection_uri):
        create_database(connection_uri)
    Base.metadata.create_all(engine)

    handler = DB_Handler(engine)

    with Session(handler.engine) as db:
        existing_packages = {
            i[0]: i[1] for i in db.execute(select(Hearing.package_id, Hearing.last_modified))
        }

    with open(os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'tests',
        'api_client_data_pickles',
        'summary_package_sample.pickle'
    ), 'rb') as f:
        package_summaries = pickle.load(f)
    
    unloaded_packages = [i for i in package_summaries if i.package_id not in existing_packages]

    handler.sync_hearing_records(unloaded_packages)

    with open(os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'tests',
        'study_ids',
        'file_name_id_map.csv'
    ), 'r') as f:
        study_files = [i for i in csv.DictReader(f)]

    study_ids = [i['hearing_id'] for i in study_files]
    with requests.Session() as s:
        client = APIClient(api_key=os.getenv('GPO_API_KEY'), session=s)
        transcripts = client.get_transcripts_by_package_id(study_ids)
    handler.sync_transcripts(transcripts)


if __name__ == '__main__':
    main()
