from telebot.types import ReplyKeyboardMarkup
import datetime

import states
import orders
import client_db
import config

# =========================================================================== #
# Все все ответы собираются здесь. В зависимости от состояния юзера           #
# вызывается соответсвующая функция. В ответ каждая функция отдаёт словарь    #
# следующего формата:                                                         #
# Text = текст сообщения от бота;                                             #
# Markup = нужно ли обновление клавиатуры, и какое;                           #
# Send = Нужно ли послать сообщение мэнеджеру;                                #
# (не актуально пока)                                                         #
# [Order] = ID заказа, по которому будет задан вопрос мэнэджеру               #
# =========================================================================== #


def first_start():
    response = 'Добро пожаловать!\nЭто прикольный бот для всякого\n' \
               'Введите пароль для доступа к боту ' \
               'или обратитесь к администратору'
    markup = ReplyKeyboardMarkup(True, False)
    markup.row('Ввести пароль', 'Администратор')
    send = False
    ret = {'text': response,
           'markup': markup,
           'send': send
           }
    return ret


def password_enter(user_id: int) -> dict:
    response = 'Введите пароль:'
    markup = ReplyKeyboardMarkup(True, False)
    markup.row('Отправить пароль', 'Отмена')
    send = False
    states.update_user_state(user_id, 'password')
    ret = {'text': response,
           'markup': markup,
           'send': send
           }
    return ret


def help_request(user_id: int):
    # TODO обратиться к администратору
    response = 'Ща найдём'
    markup = None
    send = f'Тут чел({user_id}) спрашивает'
    ret = {'text': response,
           'markup': markup,
           'send': send
           }
    return ret


def start(message, command: str) -> dict:
    commands = {'Ввести пароль': password_enter,
                'Администратор': help_request}

    func_name = commands.get(command, False)
    if not func_name:
        response = 'Введите пароль для доступа к боту ' \
                   'или обратитесь к администратору'
        markup = ReplyKeyboardMarkup(True, False)
        markup.row('Ввести пароль', 'Администратор')
        send = False
        ret = {'text': response,
               'markup': markup,
               'send': send
               }
    else:
        ret = func_name(message.from_user.id)
    return ret


def create_order(message, command: str) -> dict:
    commands = {'Сделать заказ': start_order,
                'Администратор': help_request
                }
    ret = commands.get(command, no_command)(message.from_user.id)
    return ret


def no_command(user_id: int)-> dict:
    markup = None
    response = 'Пожалуйста, воспользуйтесь клавиатурой бота'
    send = False
    ret = {'text': response,
           'markup': markup,
           'send': send
           }
    return ret


def order_type(message, command: str) -> dict:
    commands = {'Кэш': cash_order,
                'Транзит': transit_order,
                'Назад': main_menu
                }
    ret = commands.get(command, no_command)(message.from_user.id)
    return ret


def type_purpose(message, command: str) -> dict:
    commands = {config.purpose1: commerc_order,
                config.purpose2: build_order,
                'Назад': main_menu
                }
    ret = commands.get(command, no_command)(message.from_user.id)
    return ret


def commerc_order(user_id: int) -> dict:
    return set_purp_order(user_id, 'advertising')


def build_order(user_id: int) -> dict:
    return set_purp_order(user_id, 'building')


def set_purp_order(user_id: int, purpose: str) -> dict:
    # Новый заказ
    send = False
    response = 'Введите сумму:'
    markup = ReplyKeyboardMarkup(True, False)
    markup.row('Назад')
    orders.update_order(user_id, 'purpose', purpose)
    states.update_user_state(user_id, 'sum_entering')
    ret = {'text': response,
           'markup': markup,
           'send': send
           }
    return ret


def main_menu(user_id: int) -> dict:
    states.update_user_state(user_id, 'active')
    orders.update_order(user_id, 'status', 'ended')
    send = False
    response = 'Отменено'
    markup = ReplyKeyboardMarkup(True, False)
    markup.row('Сделать заказ', 'Администратор')
    ret = {'text': response,
           'markup': markup,
           'send': send
           }
    return ret


def set_operation_type(user_id: int, operation: str) -> dict:
    # Новый заказ
    send = False
    response = 'Выберите назначение операции:'
    markup = ReplyKeyboardMarkup(True, False)
    markup.row(config.purpose1, config.purpose2)
    markup.row('Назад')
    orders.create_order(user_id, operation)
    states.update_user_state(user_id, 'purpose_type')
    ret = {'text': response,
           'markup': markup,
           'send': send
           }
    return ret


def transit_order(user_id: int) -> dict:
    return set_operation_type(user_id, 'transit')


def cash_order(user_id: int) -> dict:
    return set_operation_type(user_id, 'cash')


def start_order(user_id: int) -> dict:
    # Новый заказ
    send = False
    response = 'Выберите тип операции:'
    markup = ReplyKeyboardMarkup(True, False)
    markup.row('Кэш', 'Транзит')
    markup.row('Назад')
    states.update_user_state(user_id, 'order_type')
    ret = {'text': response,
           'markup': markup,
           'send': send
           }
    return ret


def set_sum(message, command: str) -> dict:
    if command == 'Назад':
        ret = main_menu(message.from_user.id)
    else:
        ret = check_sum(message)
    return ret


def check_sum(message) -> dict:
    # Клиент вводит сумму
    # TODO проверить введённое пользователем
    response = ''
    markup = None
    send = False
    # TODO здесь собственно вся байда с лимитами проверками суммы и тд
    check = True
    if check:
        # Клиент прислал число и есть юрлицо с неизрасходованным лимитом
        states.update_user_state(message.from_user.id, 'ready_to_order')
        orders.update_order(message.from_user.id, 'money', message.text)

        response = 'Заказ возможен, вы подтверждаете?'

        markup = ReplyKeyboardMarkup(True, False)
        markup.row('Отправить заказ')
        markup.row('Назад')
    else:
        response = 'Не получится выполнить такой запрос, ' \
                   'попробуйте ввести другую сумму'

    ret = {'text': response,
           'markup': markup,
           'send': send
           }
    return ret


def password_check(message, text: str) -> dict:
    if client_db.check_client_password(message.from_user.id, text):
        response = 'Доступ открыт!'
        markup = ReplyKeyboardMarkup(True, False)
        markup.row('Сделать заказ', 'Администратор')
        send = False
        ret = {'text': response,
               'markup': markup,
               'send': send
               }
    else:
        response = 'Неверный пароль!'
        states.update_user_state(message.from_user.id, 'request')
        markup = ReplyKeyboardMarkup(True, False)
        markup.row('Ввести пароль', 'Администратор')
        send = False
        ret = {'text': response,
               'markup': markup,
               'send': send
               }
    return ret


def conf_order(message, command: str) -> dict:
    commands = {'Отправить заказ': order_confered,
                'Назад': main_menu
                }
    ret = commands.get(command, no_command)(message.from_user.id)
    return ret


def order_confered(user_id: int) -> dict:
    # Клиент подтверждает плату
    response = 'Заказ отправлен'
    markup = None
    send = f'Тут чел один({user_id}) заказ сделал'
    # TODO инструкции, может файл с реквизитами?
    orders.update_order(user_id, 'status', 'waiting')
    orders.update_order(user_id, 'start_date',
                        str(datetime.datetime.now()))
    states.update_user_state(user_id, 'confirming')
    # TODO Инфа в журнал

    ret = {'text': response,
           'markup': markup,
           'send': send
           }
    return ret


def conf_payment(message, command: str) -> dict:
    response = 'Пошлите подтверждение'
    markup = None
    send = False
    ret = {'text': response,
           'markup': markup,
           'send': send
           }
    return ret


def handle_text_user(message, command: str, state: str) -> dict:
    stat = {'request': start,
            'password': password_check,
            'active': create_order,
            'order_type': order_type,
            'purpose_type': type_purpose,
            'sum_entering': set_sum,
            'ready_to_order': conf_order,
            'confirming': conf_payment
            }
    response = stat[state](message, command)

    return response
