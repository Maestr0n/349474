import psycopg2
from psycopg2.extensions import connection

from config import host, user, password, db_name


def init_db(conn: connection):
    try:
        with conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS users(
                id serial PRIMARY KEY,
                name varchar(50) NOT NULL,
                username varchar(50),
                tg_id INTEGER UNIQUE
                )
                """
            )
            cur.execute(
                """CREATE TABLE IF NOT EXISTS tasks (
                id serial PRIMARY KEY,
                tg_id integer REFERENCES users(tg_id),
                note text NOT NULL
                )
                """)

    except Exception as _ex:
        print('[INFO]Error PostgreSQL', _ex)
    finally:
        try:
            if conn:
                conn.close()
                print('[INFO] PostgreSQL connection closed')
        except Exception as ex:
            print('[INFO] Error closing PostgreSQL connection:', ex)


def get_connection() -> connection:
    db_connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

    db_connection.autocommit = True
    return db_connection


