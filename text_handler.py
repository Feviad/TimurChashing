from telebot.types import ReplyKeyboardMarkup

import states
import orders
import datetime


# ==================================================================================================================== #
# Все все ответы собираются здесь. В зависимости от состояния юзера вызывается соответсвующая функция. В ответ каждая  #
# функция отдаёт словарь следующего формата:                                                                           #
# Text = текст сообщения от бота; Markup = нужно ли обновление клавиатуры, и какое; Send = Нужно ли послать сообщение  #
# мэнеджеру; [Order] = ID заказа, по которому будет задан вопрос мэнэджеру                                             #
# ==================================================================================================================== #


def create_order(message):
    # Новый заказ
    order_id = orders.create_order(message.from_user.id)
    states.update_order_state('IS BEING PREPARED', order_id)
    states.update_user_state('WAITING FOR SUM', message.from_user.id)
    response = 'Пожалуйста, введите сумму:'

    ret = {'Text': response,
           'Markup': None,
           'Send': False
           }
    return ret


def set_sum(message):
    order_id = orders.get_order_id_by_user(message.from_user.id)

    # TODO здесь собственно вся байда с лимитами проверками суммы и тд
    orders.update_order('name', message.text, order_id)

    states.update_user_state('WAITING FOR FILE', message.from_user.id)

    response = 'Вот платёжка:'

    # TODO платёжка?...

    orders.update_order('time', str(datetime.datetime.now()), order_id)

    ret = {'Text': response,
           'Markup': None,
           'Send': False
           }
    return ret


def set_payment(message):
    order_id = orders.get_order_id_by_user(message.from_user.id)
    orders.update_order('persons', message.text, order_id)
    states.update_user_state('WAITING FOR DATE', message.from_user.id)
    response = 'Пожалуйста, введите дату бронирования:'

    ret = {'Text': response,
            'Markup': None,
            'Send': False
            }
    return ret


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


def handle_text(message, state):
    states = {'WAITING FOR ORDER': create_order,
              'WAITING FOR SUM': set_sum,
              'WAITING FOR FILE': set_payment,

              'WAITING FOR DATE': set_date,
              'WAITING FOR TIME': set_time,
              'CHOOSING COMMENT': choose_comment,
              'WAITING FOR COMMENT': set_comment
              }
    response = states[state](message)
    return response