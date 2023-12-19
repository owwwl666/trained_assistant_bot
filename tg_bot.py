import logging

import telegram
from environs import Env
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from logger_bot import TelegramLogsHandler
from message_reply import get_reply_to_message


def start_callback(update, _):
    update.message.reply_text("Здравствуйте! Чем могу помочь?")

def replie_to_message(update, context):
    response = get_reply_to_message(
        project_id=env.str("GOOGLE_PROJECT_ID"),
        session_id=update.message.chat_id,
        text=update.message.text,
        language_code="en-US"
    )

    context.bot.send_message(update.message.chat.id, response)


if __name__ == "__main__":
    env = Env()
    env.read_env()

    logger = logging.getLogger('logger')
    log_bot = telegram.Bot(token=env.str('LOG_BOT_TOKEN'))

    logging.basicConfig(format="%(levelname)s::%(message)s", level=logging.ERROR)
    logger.addHandler(TelegramLogsHandler(
        bot=log_bot,
        chat_id=env.str("CHAT_ID")
    )
    )

    updater = Updater(env.str("TELEGRAM_BOT_TOKEN"))

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_callback))
    dispatcher.add_handler(MessageHandler(Filters.text, replie_to_message))

    try:
        updater.start_polling()
    except Exception as err:
        logger.error(err, exc_info=True)
