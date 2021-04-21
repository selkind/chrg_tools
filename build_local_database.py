import os
import pickle
import sqlalchemy
from sqlalchemy_utils import database_exists, create_database
from hearings_lib.hearings.load_project_env import ProjectEnv
from hearings_lib.db_models import Base
from hearings_lib.db_handler import DB_Handler


def main():
    ProjectEnv.load_env()
    config = ProjectEnv.get_config()
    db_config = config['govinfo_db']
    connection_uri = f'postgresql+psycopg2://{db_config["user"]}:{os.getenv("DB_POSTGRES_PW")}@{db_config["host"]}/{db_config["name"]}'

    engine = sqlalchemy.create_engine(connection_uri, future=True)
    if not database_exists(connection_uri):
        create_database(connection_uri)
    Base.metadata.create_all(engine)

    pickle_data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tests', 'summary_package_sample.pickle')
    with open(pickle_data_path, 'rb') as f:
        test_data = pickle.load(f)

    handler = DB_Handler(engine)
    handler.sync_hearing_records(test_data)


if __name__ == '__main__':
    main()
