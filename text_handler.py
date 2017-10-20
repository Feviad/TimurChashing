from telebot.types import ReplyKeyboardMarkup

import states
import orders
import datetime


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

# TODO система состояние-комманда не сделана оптимально, переделать на
# полноценный конечный автомат (через switch-словари в функциях обработчиках?)


def create_order(message, command: str) -> dict:
    # Новый заказ
    response = ''
    markup = None
    send = False

    if command == 'Запросить сумму':
        orders.create_order(message.from_user.id)
        states.update_user_state(message.from_user.id, 'ORDERING')

        response = 'Пожалуйста, введите сумму:'
        markup = ReplyKeyboardMarkup(True, False)
        markup.row('Отменить')
    else:
        markup = None
        response = 'Пожалуйста, воспользуйтесь клавиатурой бота'

    ret = {'Text': response,
           'Markup': markup,
           'Send': send
           }
    return ret


def set_sum(message, command: str) -> dict:
    # Клиент вводит сумму
    response = ''
    markup = None
    send = False

    if command == 'Отменить':
        orders.update_order(message.from_user.id, 'status', 'ENDED')
        states.update_user_state(message.from_user.id, 'WAITING')

        response = 'Заказ отменён'
        markup = ReplyKeyboardMarkup(True, False)
        markup.row('Запросить сумму')

    else:
        # TODO здесь собственно вся байда с лимитами проверками суммы и тд
        check = True
        if check:
            # Клиент прислал число и есть юрлицо с неизрасходованным лимитом
            # TODO инструкции, может файл с реквизитами?
            states.update_user_state(message.from_user.id, 'CONFIRMING')
            orders.update_order(message.from_user.id, 'start_date',
                                str(datetime.datetime.now()))
            orders.update_order(message.from_user.id, 'money', message.text)

            response = 'Совершите платёж, пришлите файл подтверждения'
            # TODO Инфа в журнал
        else:
            response = 'Не получится выполнить такой запрос, ' \
                       'попробуйте ввести другую сумму'

    ret = {'Text': response,
           'Markup': markup,
           'Send': send
           }
    return ret


def conf_payment(message, command: str) -> dict:
    # Клиент подтверждает плату
    response = ''
    markup = None
    send = False

    if command == 'Отменить':
        orders.update_order(message.from_user.id, 'status', 'ENDED')
        states.update_user_state(message.from_user.id, 'WAITING')

        response = 'Заказ отменён'
        markup = ReplyKeyboardMarkup(True, False)
        markup.row('Запросить сумму')
    elif command == 'document':
        # это пошлётся не пользвателю а мэнэджеру
        response = 'Тут чел один ({}) файлик прислал, глянь по братски'.format(
            message.from_user.id)
    else:
        response = 'Вам нужно совершить платёж и прислать файл, ' \
                   'который это подтверждает'

    ret = {'Text': response,
           'Markup': markup,
           'Send': send
           }
    return ret


def handle_text_user(message, command: str, state: str) -> dict:
    stat = {'WAITING': create_order,
            'ORDERING': set_sum,
            'CONFIRMING': conf_payment
            }
    response = stat[state](message, command)
    return response
