import datetime
import psycopg2


def create_order(user_id):
    '''Создать новый заказ юзера'''
    with psycopg2.connect("dbname='finbot' user='postgres' "
                          "host='localhost' password='Solmen'") as conn:
        cur = conn.cursor()
        create_order_query = f'INSERT INTO payments ' \
                             f'(client_telegram_id, creation_date, status) ' \
                             f'VALUES ' \
                             f'({user_id}, ' \
                             f'\'{str(datetime.datetime.now())}\', ' \
                             f'\'IS BEING PREPARED\')'
        cur.execute(create_order_query)
        conn.commit()


def update_order(user_id, field, value):
    '''Добавиь информацию по заказу'''
    with psycopg2.connect("dbname='finbot' user='postgres' "
                          "host='localhost' password='Solmen'") as conn:
        cur = conn.cursor()
        update_state_query = f'UPDATE payments SET {field} = \'{value}\'' \
                             f'WHERE client_telegram_id = {user_id} ' \
                             f'AND NOT status = \'ENDED\''
        cur.execute(update_state_query)
        conn.commit()
