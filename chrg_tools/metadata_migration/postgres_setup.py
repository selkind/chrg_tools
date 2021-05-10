from load_project_env import load_project_env
from db_context_manager import cursor


def main():
    config = load_project_env()
    db_config = config['database']
    # This script only works if database 'hearings' exists
    with open(db_config['table_config_path']) as sql_file:
        sql = sql_file.read()

    with cursor() as cur:
        cur.execute(sql)
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = cur.fetchall()
        print(tables)


if __name__ == '__main__':
    main()
