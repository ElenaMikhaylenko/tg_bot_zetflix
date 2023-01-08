import time

import telebot

from main import get_new_series

API_KEY = ""

tg_bot = telebot.TeleBot(API_KEY)


@tg_bot.message_handler(commands=["start"])
def start(message):
    tg_bot.send_message(
        message.chat.id,
        "Привет! Напиши 'Старт', чтобы получать информацию о новых сериалах",
    )


@tg_bot.message_handler()
def get_user_text(message):
    if message.text == "Старт":
        tg_bot.send_message(message.chat.id, "Отлично! Жди новых уведомлений")
        last_post_id = 0
        while True:
            new_series = get_new_series(last_post_id)

            if new_series[0] is not None:
                last_post_id = new_series[1]
                tg_bot.send_message(message.chat.id, new_series[0])
                time.sleep(1800)
    else:
        tg_bot.send_message(
            message.chat.id,
            "Пока что новые функции находятся в разработке, напиши 'Старт'",
        )


tg_bot.polling()
