from telebot.types import ReplyKeyboardMarkup

import states
import orders
import datetime


# ==================================================================================================================== #
# Все все ответы собираются здесь. В зависимости от состояния юзера вызывается соответсвующая функция. В ответ каждая  #
# функция отдаёт словарь следующего формата:                                                                           #
# Text = текст сообщения от бота; Markup = нужно ли обновление клавиатуры, и какое; Send = Нужно ли послать сообщение  #
# мэнеджеру; [Order] = ID заказа, по которому будет задан вопрос мэнэджеру ( не актуально пока)                        #
# ==================================================================================================================== #


def create_order(message, command):
    # Новый заказ
    if command == 'Запросить сумму':
        order_id = orders.create_order(message.from_user.id)
        states.update_order_state('IS BEING PREPARED', order_id)
        states.update_user_state('ORDERING', message.from_user.id)
        response = 'Пожалуйста, введите сумму:'

        request_comment_markup = ReplyKeyboardMarkup(True, False)
        request_comment_markup.row('Отменить')
    else:
        request_comment_markup = None
        response = 'Пожалуйста, воспользуйтесь клавиатурой:'

    ret = {'Text': response,
           'Markup': request_comment_markup,
           'Send': False
           }
    return ret


def set_sum(message, command):
    if command == 'Отменить':
        order_id = orders.get_order_id_by_user(message.from_user.id)
        orders.end_order(order_id)

        response = 'Заказ отменён'
        states.update_user_state('WAITING', message.from_user.id)
        main_markup = ReplyKeyboardMarkup(True, False)
        main_markup.row('Запросить сумму')

        ret = {'Text': response,
              'Markup': main_markup,
              'Send': False
              }
    else:
        order_id = orders.get_order_id_by_user(message.from_user.id)
        # TODO здесь собственно вся байда с лимитами проверками суммы и тд
        check = True
        if check:
            states.update_user_state('CONFIRMING', message.from_user.id)
            response = 'Совершите платёж, пришлите файл подтверждения'
            orders.update_order('time', str(datetime.datetime.now()), order_id)

        else:
            response = 'Не получится выполнить такой запрос, ' \
                       'попробуйте ввести другую сумму'
        ret = {'Text': response,
              'Markup': None,
              'Send': False
              }
    return ret


def set_payment(message, command):
    if command == 'Отменить':
        order_id = orders.get_order_id_by_user(message.from_user.id)
        orders.end_order(order_id)

        response = 'Заказ отменён'
        states.update_user_state('WAITING', message.from_user.id)
        main_markup = ReplyKeyboardMarkup(True, False)
        main_markup.row('Запросить сумму')

        ret = {'Text': response,
               'Markup': main_markup,
               'Send': False
               }
    elif command == 'document':
        #это пошлётся не пользвателю а мэнэджеру
        response = 'Тут чел один {} файлик прислал, глянь по братски'.format(
            message.from_user.id)
        ret = {'Text': response,
               'Markup': None,
               'Send': False
               }
    else:
        response = 'Вам нужно совершить платёж и прислать файл, ' \
                   'который это подтверждает'

        ret = {'Text': response,
               'Markup': None,
               'Send': False
               }


    return ret

'''
def set_date(message):
    order_id = orders.get_order_id_by_user(message.from_user.id)
    orders.update_order('date', message.text, order_id)
    states.update_user_state('WAITING FOR TIME', message.from_user.id)
    response = 'Пожалуйста, введите время бронирования:'

    ret = {'Text': response,
            'Markup': None,
            'Send': False
            }
    return ret


def set_time(message):
    order_id = orders.get_order_id_by_user(message.from_user.id)
    orders.update_order('time', message.text, order_id)
    states.update_user_state('CHOOSING COMMENT', message.from_user.id)
    response = 'Хотите добавить комментарий?'
    request_comment_markup = ReplyKeyboardMarkup(True, True)
    request_comment_markup.row('Да', 'Нет')

    ret = {'Text': response,
           'Markup': request_comment_markup,
           'Send': False
          }
    return ret


def choose_comment(message):
    if message.text in ['Да', 'да', 'Хочу', 'хочу']:
        states.update_user_state('WAITING FOR COMMENT', message.from_user.id)
        response = 'Пожалуйста, введите комментарий:'
        ret = {'Text': response,
               'Markup': None,
               'Send': False
               }
    elif message.text in ['Нет', 'нет', 'Не хочу', 'не хочу']:
        order_id = orders.get_order_id_by_user(message.from_user.id)
        states.update_order_state('WAITING FOR CONFIRMATION', order_id)
        states.update_user_state('WAITING FOR ORDER', message.from_user.id)
        response = 'Ваш заказ оформлен. Пожалуйста, ожидайте подтверждения ' \
                   'от менеджера.'

        ret = {'Text': response,
                'Markup': None,
                'Send': True,
                'Order': order_id
                }
    else:
        response = 'Пожалуйста, выберите "Да" или "Нет"'
        ret = {'Text': response,
                'Markup': None,
                'Send': False
                }
    return ret


def set_comment(message):
    order_id = orders.get_order_id_by_user(message.from_user.id)
    orders.update_order('comment', message.text, order_id)
    states.update_user_state('WAITING FOR ORDER', message.from_user.id)
    states.update_order_state('WAITING FOR CONFIRMATION', order_id)
    response = 'Ваш заказ оформлен. Пожалуйста, ожидайте подтверждения ' \
               'от менеджера.'

    ret = {'Text': response,
            'Markup': None,
            'Send': True,
            'Order': order_id
            }
    return ret
'''

def handle_text(message, command, state):
    #commands = {        'Запросить сумму': ,}
    states = {'WAITING': create_order,
              'ORDERING': set_sum,
              'CONFIRMING': set_payment
              }
    response = states[state](message, command)
    return response