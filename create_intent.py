import argparse
import json
import logging

import telegram
from environs import Env
from google.api_core.exceptions import InvalidArgument
from google.cloud import dialogflow

from logger_bot import TelegramLogsHandler


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases = []

    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=[message_texts])
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    return intents_client.create_intent(request={"parent": parent, "intent": intent})


if __name__ == "__main__":
    env = Env()
    env.read_env()

    logger = logging.getLogger("logger")
    log_bot = telegram.Bot(token=env.str("LOG_BOT_TOKEN"))

    logging.basicConfig(format="%(levelname)s::%(message)s", level=logging.ERROR)
    logger.addHandler(TelegramLogsHandler(bot=log_bot, chat_id=env.str("CHAT_ID")))

    parser = argparse.ArgumentParser(
        description="Создает Intent в DialogFlow для дальнейшего обучения данных."
    )
    parser.add_argument("json_path", help="Путь до Json файла с данными.")
    args = parser.parse_args()

    with open(args.json_path, "r") as file:
        training_dataset = json.loads(file.read()).items()

    for category, dialog in training_dataset:
        questions = dialog["questions"]
        answer = dialog["answer"]

        try:
            create_intent(
                project_id=env.str("GOOGLE_PROJECT_ID"),
                display_name=category,
                training_phrases_parts=questions,
                message_texts=answer,
            )
        except InvalidArgument:
            logger.error(f"Intent with the display name {category} already exists.")
