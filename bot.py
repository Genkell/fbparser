import datetime
import traceback

import telebot

from excel_utils import create_table
from config_parser import get_config
from parser import *

CONFIG = get_config()
BOT_TOKEN = CONFIG["BOT"]["token"]
BOT_TYPE = CONFIG["BOT"]["type"]
DEBUG = CONFIG["GLOBAL"]["debug"]
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    if DEBUG:
        print(message)
    bot.send_message(
        message.chat.id,
        f"👋 Приветствую, {message.from_user.first_name}!\n"
        f"Чтобы запросить данные по поиску, отправьте мне ключевое слово:"
    )


@bot.message_handler(content_types=["text"])
def answer_message(message):
    try:
        bot.send_message(message.chat.id, "Пожалуйста, подождите...")
        groups = get_groups_info(message.text)
        name = create_table(groups)
        bot.send_document(message.chat.id, open(name, "rb"))
    except (Exception, ) as e:
        if DEBUG:
            answer = f"Возникла непредвиденная ошибка. Информация для разработчика:\n" \
                      f"{str(traceback.format_exc()).splitlines()[-1]}\n" \
                      f'Чтобы отключить информацию для разработчика, измените значение ' \
                      f'параметра "debug" подпункта "GLOBAL" в файле config.ini'
            bot.send_message(message.chat.id, answer)
        else:
            bot.send_message(message.chat.id, "Произошла ошибка. Обратитесь к разработчику "
                                              "или проверьте токен приложения в файл конфигурации config.ini")
            with open(f"{datetime.datetime.now().isoformat(' ')}.log", "w") as log:
                log.write(str(traceback.format_exc()))
    else:
        if "error" in groups:
            if DEBUG:
                answer = f"Возникла непредвиденная ошибка. Информация для разработчика:\n" \
                         f"{str(groups)}\n" \
                         f'Чтобы отключить информацию для разработчика, измените значение ' \
                         f'параметра "debug" подпункта "GLOBAL" в файле config.ini'
                bot.send_message(message.chat.id, answer)
            else:
                bot.send_message(message.chat.id, "Произошла ошибка. Обратитесь к разработчику "
                                                  "или проверьте токен приложения в файл конфигурации config.ini")
                with open(f"{datetime.datetime.now().isoformat(' ')}.log", "w") as log:
                    log.write(str(groups))
        else:
            """file = create_table(groups)
            bot.send_document(message.chat.id, document=file)"""


