from environs import Env
from google.cloud import dialogflow
from telegram.ext import Updater, MessageHandler, Filters


def get_reply_to_message(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text


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
