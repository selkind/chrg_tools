import os
import psycopg2
import psycopg2.extras
import contextlib
from load_project_env import ProjectEnv


@contextlib.contextmanager
def connection(cursor_type=psycopg2.extras.DictCursor):
    ProjectEnv.load_env()
    config = ProjectEnv.get_config()
    connection = psycopg2.connect(
        database=config['database']['name'],
        user=config['database']['user'],
        host=config['database']['host'],
        password=os.getenv('DB_POSTGRES_PW'),
        cursor_factory=cursor_type
    )

    try:
        yield connection
    except Exception as e:
        connection.rollback()
        raise e
    else:
        connection.commit()
    finally:
        connection.close()


@contextlib.contextmanager
def cursor(cursor_type=psycopg2.extras.DictCursor):
    with connection(cursor_type=cursor_type) as conn:
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()
