import os
import requests
import sqlalchemy
from sqlalchemy.orm import Session
from hearings_lib.hearings.load_project_env import ProjectEnv
from hearings_lib.db_models import (
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
        f':{os.getenv("DB_POSTGRES_PW")}@{db_config["host"]}/{db_config["name"]}'
    )

    engine = sqlalchemy.create_engine(connection_uri, future=True)

    handler = DB_Handler(engine)

    with Session(handler.engine) as db:
        packages_to_fetch = [i[0] for i in db.execute(sqlalchemy.select(Hearing).filter_by(congress=117))]

    with requests.Session() as s:
        client = APIClient(api_key=os.getenv('GPO_API_KEY'), session=s)
        transcripts = client.get_transcripts_by_package_id([i.package_id for i in packages_to_fetch])

    for i in transcripts:
        if transcripts[i]:
            with open(f'tests/transcript_{i}.txt', 'wb+') as f:
                f.write(transcripts[i])


if __name__ == '__main__':
    main()
