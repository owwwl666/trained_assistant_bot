import telebot
from environs import Env
from google.cloud import dialogflow

env = Env()
env.read_env()

bot = telebot.TeleBot(env.str("TELEGRAM_BOT_TOKEN"))


def get_reply_to_message(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text


@bot.message_handler(content_types=["text"])
def replie_to_message(message):
    response = get_reply_to_message(
        project_id=env.str("GOOGLE_PROJECT_ID"),
        session_id=message.chat.id,
        text=message.text,
        language_code="en-US"
    )

    bot.send_message(message.chat.id, response)


if __name__ == "__main__":
    bot.infinity_polling(none_stop=True)
