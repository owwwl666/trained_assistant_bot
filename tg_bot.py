from environs import Env
from telegram.ext import Updater, MessageHandler, Filters

from message_reply import get_reply_to_message


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

    updater = Updater(env.str("TELEGRAM_BOT_TOKEN"))

    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text, replie_to_message))

    updater.start_polling()
