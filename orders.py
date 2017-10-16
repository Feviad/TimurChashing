import sqlite3
import random


def create_order(user_id):
    '''Создать новый заказ юзера'''
    with sqlite3.connect('rest_bot.db') as conn:
        cur = conn.cursor()
        create_order_query = f'INSERT INTO orders (user_id, flag) VALUES ({user_id}, 1)'
        cur.execute(create_order_query)
        conn.commit()
        # определяем какой айдишник был создан, чтобы его передать обратно
        create_order_query = f'SELECT id FROM orders WHERE user_id = {user_id} AND flag = 1'
        cur.execute(create_order_query)
        order = cur.fetchone()[0]
        create_order_query = f'UPDATE orders SET flag = 0'
        cur.execute(create_order_query)
        conn.commit()
        create_order_query = f'INSERT INTO orders_states (id) VALUES ({order})'
        print(create_order_query)
        cur.execute(create_order_query)
        conn.commit()
        return order


def end_order(order_id):
    with sqlite3.connect('rest_bot.db') as conn:
        cur = conn.cursor()
        update_state_query = f'DELETE FROM orders ' \
                             f'WHERE id = {order_id}'
        cur.execute(update_state_query)
        update_state_query = f'DELETE FROM orders_states ' \
                             f'WHERE id = {order_id}'
        cur.execute(update_state_query)
        conn.commit()



def update_order(field, value, order_id):
    '''Добавиь информацию по заказу'''
    with sqlite3.connect('rest_bot.db') as conn:
        cur = conn.cursor()
        update_state_query = f'UPDATE orders SET {field} = \'{value}\'' \
                             f'WHERE id = \'{order_id}\''
        cur.execute(update_state_query)
        conn.commit()


def get_order_id_by_user(user_id):
    '''Найти незаконченный заказ юзера'''
    with sqlite3.connect('rest_bot.db') as conn:
        cur = conn.cursor()
        request_state_query = f'SELECT id FROM orders WHERE user_id = {user_id}'
        cur.execute(request_state_query)
        for orders in cur.fetchall():
            request_state_query = f'SELECT state FROM orders_states WHERE id = {orders[0]}'
            cur.execute(request_state_query)
            state = cur.fetchone()[0]
            if state == 'IS BEING PREPARED':
                return orders[0]
    # TODO обработать, если все заказы обработаны


def get_order_for_restaurant(order_id):
    '''Собрать информацию о заказе для мэнэджера'''
    with sqlite3.connect('rest_bot.db') as conn:
        cur = conn.cursor()
        request_state_query = f'SELECT name, persons, date, time, comment FROM orders WHERE id = {order_id}'
        cur.execute(request_state_query)
        order = cur.fetchone()
        text = 'Name: {}\nPersons: {}\nDate: {}\nTime: {}\nComment: {}'.format(order[0], order[1], order[2],
                                                                               order[3], order[4])
        return text
