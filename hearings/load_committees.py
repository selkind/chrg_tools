import os
import csv
import psycopg2
import psycopg2.extras
from load_project_env import ProjectEnv


def main():
    ProjectEnv.load_env()
    config = ProjectEnv.get_congfig()

    columns = ['name', 'code', 'chamber']

    with open(config['data']['committee_path']) as f:
        reader = csv.DictReader(f, fieldnames=columns)
        data = []
        for i in reader:
            i['name'] = i['name'][i['name'].find('-') + 1:]
            data.append(i)

    query = f"Insert INTO committees ({','.join(columns)}) VALUES %s"
    values = [[val for val in row.values()] for row in data]

    db_config = config['database']

    conn = psycopg2.connect(database=db_config['name'],
                            user=db_config['user'],
                            host=db_config['host'],
                            password=os.getenv('DB_POSTGRES_PW'))

    try:
        crs = conn.cursor()
        psycopg2.extras.execute_values(crs, query, values)
        conn.commit()

    except Exception as e:
        print(e)

    finally:
        conn.close()


if __name__ == '__main__':
    main()
