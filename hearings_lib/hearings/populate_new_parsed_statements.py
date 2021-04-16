import os
from load_project_env import ProjectEnv
from db_context_manager import cursor
from hearings_lib.hearings.parser import Parser
import psycopg2.extras


def main():
    select_all_hearing_query: str = 'SELECT id, transcript FROM hearings'
    hearings: list = []
    with cursor() as cur:
        cur.execute(select_all_hearing_query)
        hearings = [i for i in cur]
    
    new_parser = Parser()

    statement_entries = []
    for transcript_id, transcript in hearings:
        new_parser.

