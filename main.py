import flask as flask
from bot import *

if BOT_TYPE == "webhook":
    app = flask.Flask(__name__)
    WEBHOOK_HOST = CONFIG["BOT"]["host"]
    WEBHOOK_PORT = CONFIG["BOT"]["port"]
    WEBHOOK_URL_BASE = f"https://{WEBHOOK_HOST}"
    WEBHOOK_URL_PATH = f"/{BOT_TOKEN}/"
    WEBHOOK_SSL_CERT = 'certificates/webhook_cert.pem'
    WEBHOOK_SSL_PRIVATE = 'certificates/webhook_pkey.pem'


    @app.route(f"/{BOT_TOKEN}", methods=['GET', 'POST'])
    def process():
        request_decoded = flask.request.stream.read().decode("utf-8")
        print(request_decoded)
        try:
            bot.process_new_updates([telebot.types.Update.de_json(request_decoded)])
        except (Exception,):
            pass
        return ""


    if __name__ == "__main__":
        url = f"{WEBHOOK_HOST}:{WEBHOOK_PORT}/{BOT_TOKEN}"

        bot.set_webhook(url=url,
                        certificate=open(WEBHOOK_SSL_CERT, 'r'))
        if DEBUG:
            print("Bot started with webhook type")
        app.run(host=WEBHOOK_HOST,
                port=WEBHOOK_PORT,
                ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIVATE))

elif BOT_TYPE == "polling":
    if __name__ == "__main__":
        if DEBUG:
            print("Bot started with polling type")
        while True:
            try:
                bot.polling(True, timeout=500)
            except:
                continue

else:
    raise KeyError(f'Unknown bot type "{BOT_TYPE}". Check config.ini')
