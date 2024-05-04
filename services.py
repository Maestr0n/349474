
from psycopg2.extensions import connection


def add_task(task: str, user_id: int, conn: connection) -> None:
    query = f"""INSERT INTO tasks (tg_id, note)
                VALUES (%s, %s);   
            """
    with conn.cursor() as cur:
        cur.execute(query, (user_id, task))


def get_tasks(conn: connection) -> tuple:
    query = f"""SELECT * 
                FROM tasks;   
            """
    with conn.cursor() as cur:
        cur.execute(query)
        res = cur.fetchall()
    return res


def del_task(task_id: int, conn: connection):
    query = (f'DELETE FROM tasks '
             f'WHERE id = {task_id};')
    with conn.cursor() as cur:
        cur.execute(query)


def get_user(user_id: int, conn: connection) -> tuple:
    query = f"""SELECT * 
                FROM users
                WHERE tg_id = %s;   
                """
    with conn.cursor() as cur:
        cur.execute(query, (user_id,))
        res = cur.fetchone()
    return res


def add_user(user_id: int, username: str, name: str, conn: connection) -> None:
    query = f"""INSERT INTO users (tg_id, name, username)
                VALUES (%s, %s, %s);   
            """
    with conn.cursor() as cur:
        cur.execute(query, (user_id, name, username))

