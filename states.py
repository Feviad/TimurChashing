import datetime
import psycopg2


def add_user(user_id):
    with psycopg2.connect("dbname='finbot' user='postgres' "
                          "host='localhost' password='Solmen'") as conn:
        cur = conn.cursor()

        user_in_db_query = f'SELECT telegram_id FROM operators WHERE ' \
                           f'telegram_id = {user_id}'
        cur.execute(user_in_db_query)
        status = cur.fetchone()
        if not status:
            users_query = f'INSERT INTO operators (telegram_id, ' \
                          f'creation_date, status)  VALUES ({user_id}, ' \
                          f'\'{str(datetime.datetime.now())}\', \'WAITING\')'

            cur.execute(users_query)
            conn.commit()


def update_user_state(user_id: int, state: str) -> None:
    '''Изменить состояние юзера'''
    with psycopg2.connect("dbname='finbot' user='postgres' "
                          "host='localhost' password='Solmen'") as conn:
        cur = conn.cursor()
        update_state_query = f'UPDATE operators SET status = \'{state}\'' \
                             f'WHERE telegram_id = {user_id} '
        cur.execute(update_state_query)
        conn.commit()

def get_user_state_by_id(user_id):
    with psycopg2.connect("dbname='finbot' user='postgres' "
                          "host='localhost' password='Solmen'") as conn:
        cur = conn.cursor()
        update_state_query = f'SELECT status FROM operators ' \
                             f'WHERE telegram_id = {user_id} '
        cur.execute(update_state_query)
        status = cur.fetchone()[0]
        return status

def get_order_state_by_id(user_id):
    with psycopg2.connect("dbname='finbot' user='postgres' "
                          "host='localhost' password='Solmen'") as conn:
        cur = conn.cursor()
        update_state_query = f'SELECT status FROM payments ' \
                             f'WHERE client_telegram_id = {user_id} ' \
                             f'AND NOT status = \'ENDED\''
        cur.execute(update_state_query)
        status = cur.fetchone()[0]
        return status