import sqlite3


def get_order_state_by_id(order_id):
    '''Получить состояние заказа'''
    with sqlite3.connect('rest_bot.db') as conn:
        cur = conn.cursor()
        request_state_query = f'SELECT state FROM orders_state WHERE id = {order_id}'
        cur.execute(request_state_query)
        state = cur.fetchone()[0]
        return state


def update_order_state(state, order_id):
    '''Изменить состояние заказа'''
    with sqlite3.connect('rest_bot.db') as conn:
        cur = conn.cursor()
        update_state_query = f'UPDATE orders_states SET state = \'{state}\'' \
                             f'WHERE id = \'{order_id}\''
        cur.execute(update_state_query)
        conn.commit()


def update_user_state(state, user_id):
    '''Изменить состояние юзера'''
    with sqlite3.connect('rest_bot.db') as conn:
        cur = conn.cursor()
        update_state_query = f'UPDATE users_states SET state = \'{state}\'' \
                             f'WHERE id = \'{user_id}\''
        cur.execute(update_state_query)
        conn.commit()


def get_user_state_by_id(user_id):
    '''Получить состояние юзера'''
    with sqlite3.connect('rest_bot.db') as conn:
        cur = conn.cursor()
        request_state_query = f'SELECT state FROM users_states WHERE id = {user_id}'
        cur.execute(request_state_query)
        state = cur.fetchone()[0]
        return state