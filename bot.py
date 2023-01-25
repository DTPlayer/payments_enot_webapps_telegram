from telebot import types, TeleBot
from config import TOKEN, URL

payment_bot = TeleBot(TOKEN)


@payment_bot.message_handler(commands=['start'])
def start(message):
    # Создаем веб-приложение и кнопку к ней
    payment_web_app = types.WebAppInfo(
        title='Payment',
        description='Payment by user for service',
        url=URL+f'/pay/?user_id={message.from_user.id}',
        method='get',
    )

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton('Оплата', web_app=payment_web_app),
    )
    # Отправляем сообщение с кнопкой
    payment_bot.send_message(
        message.chat.id,
        'Добро пожаловать, {}!'.format(message.from_user.first_name),
        reply_markup=keyboard,
    )


@payment_bot.message_handler(content_types=['text'])
def text(message):
    payment_web_app = types.WebAppInfo(
        title='Payment',
        description='Payment by user for service',
        url=URL+f'/pay/?user_id={message.from_user.id}',
        method='get',
        )

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton('Оплата', web_app=payment_web_app),
        )

    payment_bot.send_message(
    message.chat.id,
        'Оплата производится внутри бота, нажмите на кнопку "Оплата"',
        reply_markup=keyboard,
        )
