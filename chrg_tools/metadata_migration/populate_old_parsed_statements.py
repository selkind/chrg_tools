import os
from load_project_env import ProjectEnv
from db_context_manager import cursor
from hearings_lib.gpo_tools.gpo_tools.parse import Parser
import psycopg2.extras


def main():
    ProjectEnv.load_env()
    config = ProjectEnv.get_config()
    db_config = config['database']

    parser = Parser(
        db=db_config['name'],
        user=db_config['user'],
        password=os.getenv('DB_POSTGRES_PW'),
        host=db_config['host']
    )

    parser.parse_gpo_hearings()

    schema_map = {'speaker': 'name_raw', 'member_id': 'member_id', 'hearing_id': 'jacket', 'statement': 'cleaned'}
    statement_fields = sorted(schema_map.keys())

    statements = []
    for i in parser.results:
        for j in i:
            statement = []
            for k in statement_fields:
                if k == 'member_id':
                    member_id = j[schema_map[k]]
                    if not member_id or (type(member_id) == str and len(member_id) < 4):
                        member_id = 0
                    statement.append(int(member_id))
                else:
                    statement.append(j[schema_map[k]])
            statements.append(statement)

    statement_insert_query = f"INSERT INTO old_parsed_hearing_statements ({','.join(statement_fields)}) VAlUES %s"
    with cursor() as cur:
        psycopg2.extras.execute_values(cur, statement_insert_query, statements)


if __name__ == '__main__':
    main()
