import random

import vk_api as vk
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

from message_reply import get_reply_to_message


def replie_to_message(event, vk_api):
    response = get_reply_to_message(
        project_id=env.str("GOOGLE_PROJECT_ID"),
        session_id=event.user_id,
        text=event.text,
        language_code="en-US"
    )

    vk_api.messages.send(
        user_id=event.user_id,
        message=response,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    env = Env()
    env.read_env()

    vk_session = vk.VkApi(token=env.str("VK_BOT_TOKEN"))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                replie_to_message(event, vk_api)
            except vk.exceptions.ApiError:
                pass
