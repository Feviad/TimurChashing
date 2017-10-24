import logging
from logging.handlers import RotatingFileHandler
import telebot

import config
import text_handler
import states
import client_db

import requests


bot = telebot.TeleBot(config.TOKEN_CLIENT)
managerbot = telebot.TeleBot(config.TOKEN_OPERATOR)

# Самая важная херня кода - кто мэнэджер?
# TODO изменить это на функцию выбора
MANAGER = 87435164


# Старт
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    user_info = client_db.check_client_in_db(user_id)
    if not user_info['found']:
        client_db.add_user(user_id)
        # TODO start mess
        response = text_handler.first_start()
    else:
        rights = client_db.check_rights(user_id)
        if rights:
            # TODO hello mess
            response = text_handler.first_start()
        else:
            # TODO password mess
            response = text_handler.first_start()
    bot.send_message(user_id, response['text'],
                         reply_markup=response['markup'])


# Обычное сообщение
@bot.message_handler(func=lambda mesage: True, content_types=['text'])
def handle_text(message):
    user_id = message.from_user.id
    # узнаём, в каком состоянии сейчас пользователь
    state = states.get_user_state_by_id(user_id)
    # формируем ответ исходя из состояния
    response = text_handler.handle_text_user(message, message.text, state)

    # Сперва отправляем ответ юзеру
    if response['markup']:
        # обычный ответ юзеру, но с обновлением клавиатуры
        bot.send_message(message.from_user.id,
                         response['text'],
                         reply_markup=response['markup'])
    else:
        # самый простой ответ юзеру
        bot.send_message(message.from_user.id, response['text'])

    if response['send']:
        # Ещё нужно что-то сообщить мэнэджеру

        managerbot.send_message(message.from_user.id, response['send'])
        '''
        keyboard = telebot.types.InlineKeyboardMarkup()
        data = {'Answer': True, 'ID': message.from_user.id}
        callback_button = telebot.types.InlineKeyboardButton(text="Всё верно",
                                                             callback_data=str(
                                                                 data))
        keyboard.add(callback_button)
        data = {'Answer': False, 'ID': message.from_user.id}
        callback_button = telebot.types.InlineKeyboardButton(
            text="Ты чё прислал?", callback_data=str(data))
        keyboard.add(callback_button)
        bot.send_message(MANAGER, 'Заказ\n' + text, reply_markup=keyboard)
        '''

# сообщение c файлом
@bot.message_handler(func=lambda mesage: True, content_types=['document'])
def handle_doc(message):
    # узнаём, в каком состоянии сейчас пользователь
    state = states.get_user_state_by_id(message.from_user.id)
    # формируем ответ исходя из состояния
    if state == 'confirming':

        bot.send_message(message.from_user.id, 'Ща проверят')
        # TODO сделать полноценный словарь информации
        keyboard = telebot.types.InlineKeyboardMarkup()
        data = {'Answer': True, 'ID': message.from_user.id}
        callback_button = telebot.types.InlineKeyboardButton(text="Всё верно",
                                                             callback_data=str(
                                                                 data))
        keyboard.add(callback_button)
        data = {'Answer': False, 'ID': message.from_user.id}
        callback_button = telebot.types.InlineKeyboardButton(
            text="Ты чё прислал?",
            callback_data=str(
                data))
        keyboard.add(callback_button)

        file_info = bot.get_file(message.document.file_id)

        downloaded_file = bot.download_file(file_info.file_path)
        managerbot.send_message(MANAGER, 'OLOLOLOLO')
        managerbot.send_document(MANAGER, downloaded_file, reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'вы ничего не заказывали')


# инлайн ответ
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        resp = eval(call.data)
        if resp['Answer']:
            # если приняли заказ

            #TODO изменения состояний
            # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")
            bot.send_message(int(resp['ID']), 'Заказ принят!')
            states.update_user_state(int(resp['ID']), 'WAITING')
        else:
            # если заказ не принят

            # TODO изменения состояний
            # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Sad")
            bot.send_message(int(resp['ID']), 'а идика ты с ослом')
    elif call.inline_message_id:
        bot.send_message(MANAGER, 'чухчух')
        resp = eval(call.data)
        if resp['Answer']:
            # если приняли заказ

            # TODO изменения состояний
            # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")
            bot.send_message(int(resp['ID']), 'Заказ принят!')
            states.update_user_state(int(resp['ID']), 'WAITING')
        else:
            # если заказ не принят

            # TODO изменения состояний
            # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Sad")
            bot.send_message(int(resp['ID']), 'а идика ты с ослом')


if __name__ == '__main__':
    logger = logging.getLogger('bot_logger')
    logger.setLevel(logging.INFO)

#    bot.remove_webhook()
#    time.sleep(3)  # это для первого запуска
    handler = RotatingFileHandler('logs/bot_logger',
                                  maxBytes=1024*1024*3,
                                  backupCount=20)
    formatter = logging.Formatter(fmt='%(filename)s[LINE:%(lineno)d]# '
                                      '%(levelname)-8s [%(asctime)s]  '
                                      '%(message)s'
                                  )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    bot.polling(none_stop=True)


'''        lol = {
               'chat_id' : '101088393'
        }
   #requests.get('https://api.telegram.org/bot390987414:AAEudQE6TAdUNJfCbKbDxg9izOyraRexeDA/sendDocument?chat_id=101088393&document=' + message.document.file_id)
        #print('https://api.telegram.org/bot390987414:AAEudQE6TAdUNJfCbKbDxg9izOyraRexeDA/sendDocument?chat_id=101088393&document=' + message.document.file_id)
        ff = {'file': downloaded_file}
        #294832802:AAEdQSuUAg_o8K4hDt9eX21h_2cGrYI9HdE

        #requests.post('https://api.telegram.org/bot390987414:AAEudQE6TAdUNJfCbKbDxg9izOyraRexeDA/sendDocument', data=lol, files=ff)

'''