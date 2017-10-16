import sqlite3


def add_id(user):
    with sqlite3.connect('rest_bot.db') as conn:
        cur = conn.cursor()

        user_in_db_query = f'SELECT id FROM users WHERE id = {user.id}'
        cur.execute(user_in_db_query)
        status = cur.fetchone()
        if not status:
            if not user.first_name:
                user.first_name = 'NULL'
            if not user.last_name:
                user.last_name = 'NULL'

            users_query = f'INSERT INTO users VALUES (' \
                          f'\'{user.id}\', \'{user.first_name}\', ' \
                          f'\'{user.last_name}\')'

            states_query = f'INSERT INTO users_states VALUES (\'{user.id}\', ' \
                           f'\'WAITING\')'

            cur.execute(users_query)
            cur.execute(states_query)
