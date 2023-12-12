import telebot
from environs import Env

env = Env()
env.read_env()

bot = telebot.TeleBot(env.str("TELEGRAM_BOT_TOKEN"))


@bot.message_handler(commands=['start'])
def start_work(message):
    bot.send_message(message.chat.id, "Здравствуйте!")


@bot.message_handler(content_types=["text"])
def replie_to_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling(none_stop=True)
