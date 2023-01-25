"""
Основной файл, делаем импорты и запускаем все подряд.
"""
from bot import payment_bot
import telebot
from flask import Flask, request, render_template
from config import MERCHANT_ID, ORDER_AMOUNT, SECRET_WORD, SECRET_WORD_2
import hashlib
import time
import json

app = Flask(__name__)


@app.route('/telegram/', methods=['POST'])
def telegram():
    """
    Вебхук для телеграма, ничего не обычного
    Единственное что, надо будет перейти по ссылке https://api.telegram.org/bot<token>/setWebhook?url=<url>/telegram/
    """
    if request.method == 'POST':
        json_string = request.stream.read().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        payment_bot.process_new_updates([update])
        return '', 200


@app.route('/pay/', methods=['GET'])
def pay():
    """
    Здесь мы создаем форму для оплаты, которая будет отправлена пользователю.
    По итогу пользователя перекинет на страницу оплаты, где он сможет оплатить заказ.
    """
    user_id = request.args.get('user_id')
    payment_id = int(time.time())
    sign = hashlib.md5(
        (str(MERCHANT_ID) + ':' + str(ORDER_AMOUNT) + ':' + SECRET_WORD + ':' + str(payment_id)).encode()).hexdigest()
    return render_template('payment_form.html',
                           MERCHANT_ID=MERCHANT_ID,
                           ORDER_AMOUNT=ORDER_AMOUNT,
                           PAYMENT_ID=payment_id,
                           sign=sign,
                           bot_url='https://t.me/{}'.format(payment_bot.get_me().username),
                           user_id=user_id)


@app.route('/callback/', methods=['POST'])
def callback():
    """
    Здесь мы получаем ответ от платежной системы, проверяем подпись и обрабатываем ответ.
    Итог - пользователю падает сообщения о том, что его заказ оплачен
    """
    merchant = request.form['merchant']
    amount = request.form['amount']
    merchant_id = request.form['merchant_id']
    sign_2 = request.form['sign_2']
    user_id = json.loads(request.form['custom_field'])['user_id']

    sign = hashlib.md5((merchant + ':' + amount + ':' + SECRET_WORD_2 + ':' + merchant_id).encode()).hexdigest()

    if sign != sign_2:
        return 'bad sign!', 400

    payment_bot.send_message(user_id, 'Спасибо за платеж!\nСумма: {}'.format(amount))
    return 'Good', 200


if __name__ == '__main__':
    # Запускаем сервер
    app.run(port=5000, debug=True)