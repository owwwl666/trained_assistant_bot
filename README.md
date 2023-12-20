# Описание
Создание двух ботов-помощников (VK и Telegram) для решения бизнес задач. Обучившись распознаванию естественного языка с помощию [DialogFlow](https://habr.com/ru/articles/502688/), боты отвечают на часто задаваемые [вопросы](https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json) пользователей.

### Установка зависимостей
```
pip install -r requirements.txt
```

### Переменные окружения
```
TELEGRAM_BOT_TOKEN=<Токен телеграм бота, в котором будет вестись диалог>
GOOGLE_APPLICATION_CREDENTIALS=<Путь до файла с ключами от Google, credentials.json>
GOOGLE_PROJECT_ID=<ID вашего проекта в DialogFlow>
VK_BOT_TOKEN=<Токен ВК бота, в котором будет вестись диалог>
LOG_BOT_TOKEN=<Токен телеграм бота для сообщений об ошибках>
CHAT_ID=<Ваш телеграм id>
```
- Для создания переменной окружения `GOOGLE_APPLICATION_CREDENTIALS` необходимо установить [gcloud](https://cloud.google.com/dialogflow/es/docs/quick/setup#sdk)

### create_intent.py
Создает новый раздел с в DialogFlow со списком вопросов от пользователей и общим ответом на все эти вопросы. Для запуска скрипта необходим JSON файл с вопросами (пример такого файла был приведен в Описании).

Введите команду для создания раздела и обучения на основе данных этого раздела:
```
python create_intent.py JSON_PATH
```

- Если данные уже занесены в DailogFlow и обучены, то бот-логгер предупредит вас об этом.

### tg_bot.py

Телеграм бот для общения с пользователем. Приветсвует пользователя, а также отвечает на вопросы, раннее занесенные в DialogFlow.

[**Ссылка на бот**](https://t.me/dialiogflow_bot)
