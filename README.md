UkrTennisPlayersBot

Telegram-бот для отримання інформації про українських тенісистів.

Проєкт має дві версії бота:

bot.py — працює тільки з локальною базою гравців
utpbot.py — поєднує локальну базу та AI-генеровану біографію (OpenAI)

Функціональність

bot.py (локальна версія)

Пошук українських тенісистів
Виведення:
року народження, туру (ATP / WTA / ITF), найвищого рейтингу, основних досягнень
Підтримка нечіткого пошуку (через difflib)


utpbot.py (версія з AI)
Додатково до локальної інформації:
Команда /bio <ім’я>
Генерує детальну біографію українською мовою
Використовує OpenAI API

ChatBot/

│

├── bot.py                  # Локальна версія бота
├── utpbot.py               # Версія з AI
├── config\_example.py       # Приклад конфігурації
├── .gitignore
└── README.md


Встановлення:

1.Клонування репозиторію 
git clone https://github.com/Rusynka/UkrTennisPlayersBot.git
cd UkrTennisPlayersBot

2\. Створення віртуального середовища:
python -m venv venv
venv\\Scripts\\activate

3\. Встановлення залежностей
pip install python-telegram-bot openai

4\. Створити файл config.py
TELEGRAM\_TOKEN = "YOUR\_TELEGRAM\_TOKEN"
OPENAI\_API\_KEY = "YOUR\_OPENAI\_API\_KEY"

Запуск
Локальна версія: python bot.py
Версія з AI: python utpbot.py
