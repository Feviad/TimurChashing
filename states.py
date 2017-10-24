import psycopg2

import config


def update_user_state(user_id: int, state: str) -> None:
    '''Изменить состояние юзера'''
    with psycopg2.connect(dbname=config.BD_NAME,
                          user=config.BD_USER,
                          host=config.HOST,
                          password=config.BD_PASS) as conn:
        cur = conn.cursor()
        update_state_query = f'UPDATE clients SET status = \'{state}\'' \
                             f'WHERE telegram_id = {user_id} '
        cur.execute(update_state_query)
        conn.commit()

def get_user_state_by_id(user_id):
    with psycopg2.connect(dbname=config.BD_NAME,
                          user=config.BD_USER,
                          host=config.HOST,
                          password=config.BD_PASS) as conn:
        cur = conn.cursor()
        update_state_query = f'SELECT status FROM clients ' \
                             f'WHERE telegram_id = {user_id} '
        cur.execute(update_state_query)
        status = cur.fetchone()[0]
        return status

def get_order_state_by_id(user_id):
    with psycopg2.connect(dbname=config.BD_NAME,
                          user=config.BD_USER,
                          host=config.HOST,
                          password=config.BD_PASS) as conn:
        cur = conn.cursor()
        update_state_query = f'SELECT status FROM payments ' \
                             f'WHERE client_telegram_id = {user_id} ' \
                             f'AND NOT status = \'ended\''
        cur.execute(update_state_query)
        status = cur.fetchone()[0]
        return status