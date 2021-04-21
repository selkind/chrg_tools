import os
import pickle
import sqlalchemy
from sqlalchemy_utils import database_exists, create_database
from hearings_lib.hearings.load_project_env import ProjectEnv
from hearings_lib.db_models import Base
from hearings_lib.db_handler import DB_Handler
from hearings_lib.api_client import APIClient


def main():
    ProjectEnv.load_env()
    config = ProjectEnv.get_config()
    db_config = config['govinfo_db']
    connection_uri = f'postgresql+psycopg2://{db_config["user"]}:{os.getenv("DB_POSTGRES_PW")}@{db_config["host"]}/{db_config["name"]}'

    engine = sqlalchemy.create_engine(connection_uri, future=True)
    if not database_exists(connection_uri):
        create_database(connection_uri)
    Base.metadata.create_all(engine)

    handler = DB_Handler(engine)

    client = APIClient(api_key=os.getenv('GPO_API_KEY'))
    package_ids = client.get_package_ids_by_congress(113)
    package_summaries = client.get_package_summaries(packages=package_ids[:10])
    with open('tests/summary_package_sample.pickle', 'wb+') as f:
        pickle.dump(package_summaries, f)

    handler.sync_hearing_records(package_summaries)


if __name__ == '__main__':
    main()
