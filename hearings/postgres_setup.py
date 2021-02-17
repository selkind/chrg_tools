import os
import psycopg2
from load_project_env import ProjectEnv


def main():
    ProjectEnv.load_env()
    config = ProjectEnv.get_config()
    db_config = config['database']
    # This script only works if database 'hearings' exists
    with open(config['database']['table_config_path']) as sql_file:
        sql = sql_file.read()

    conn = psycopg2.connect(database=db_config['name'],
                            user=db_config['user'],
                            host=db_config['host'],
                            password=os.getenv('DB_POSTGRES_PW'))
    try:
        crs = conn.cursor()
        crs.execute(sql)
        conn.commit()

        crs.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = crs.fetchall()
        print(tables)

    finally:
        conn.close()


if __name__ == '__main__':
    main()
