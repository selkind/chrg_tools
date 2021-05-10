import os
import sqlalchemy
import csv
import sys
csv.field_size_limit(sys.maxsize)
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import select
from sqlalchemy.orm import Session
from hearings_lib.hearings.load_project_env import ProjectEnv
from hearings_lib.transcript_parser import Parser
from hearings_lib.db_models import (
    Base,
    HearingTranscript
)
from hearings_lib.db_handler import DB_Handler


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
        study_transcripts = [i[0] for i in db.execute(select(HearingTranscript))]

    parser = Parser()

    parsed_transcripts = {i.package_id: parser.parse(i.body.split('\n')) for i in study_transcripts}

    with open('tests/study_ids/file_name_id_map.csv', 'r') as f:
        nb_parsed_packages = {i['hearing_id']: i['file_name'] for i in csv.DictReader(f)}

    existing_parsed_path_root = "/mnt/c/Users/samue/Dropbox/Hearings"

    parsed_entries = {}
    for i in parsed_transcripts:
        print(i, nb_parsed_packages[i])
        file_name = f'{os.path.splitext(nb_parsed_packages[i])[0]}.csv'
        file_path = os.path.join(existing_parsed_path_root, 'alt_output', file_name)
        with open(file_path, 'r') as f:
            parsed_entries[i] = [j for j in csv.DictReader(f)]
        print(f'old len: {len(parsed_entries[i])} new len: {len(parsed_transcripts[i][0])}')
    

if __name__ == '__main__':
    main()
