from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import difflib
from config import TELEGRAM_TOKEN  # Імпортуємо токен із локального файлу

# Повний словник 25 українських тенісистів
players = {
    "elina svitolina": {"Рік народження": "1994", "Тур": "WTA", "Найвищий рейтинг": "№3 WTA", "Досягнення": "WTA Finals 2018, Бронза Олімпіади 2020"},
    "marta kostyuk": {"Рік народження": "2002", "Тур": "WTA", "Найвищий рейтинг": "№45 WTA", "Досягнення": "Перемоги на турнірах WTA"},
    "dayana yastremska": {"Рік народження": "2000", "Тур": "WTA", "Найвищий рейтинг": "№21 WTA", "Досягнення": "3 титули WTA"},
    "lesia tsurenko": {"Рік народження": "1989", "Тур": "WTA", "Найвищий рейтинг": "№23 WTA", "Досягнення": "4 титули WTA"},
    "anhelina kalinina": {"Рік народження": "1997", "Тур": "WTA", "Найвищий рейтинг": "№36 WTA", "Досягнення": "Фіналістка WTA 1000"},
    "oleksandra oliynykova": {"Рік народження": "1998", "Тур": "WTA / ITF", "Найвищий рейтинг": "№150 WTA", "Досягнення": "Перемоги на турнірах ITF"},
    "andriy medvedev": {"Рік народження": "1974", "Тур": "ATP", "Найвищий рейтинг": "№4 ATP", "Досягнення": "Фінал Roland Garros 1999, 11 титулів ATP"},
    "sergiy stakhovsky": {"Рік народження": "1986", "Тур": "ATP", "Найвищий рейтинг": "№31 ATP", "Досягнення": "4 титули ATP, перемога над Federer"},
    "ilya marchenko": {"Рік народження": "1987", "Тур": "ATP", "Найвищий рейтинг": "№49 ATP", "Досягнення": "Перемоги на турнірах ATP Challenger"},
    "vitaliy sachko": {"Рік народження": "1993", "Тур": "ATP", "Найвищий рейтинг": "№158 ATP", "Досягнення": "Перемоги на турнірах ATP Challenger"},
    "kateryna bondarenko": {"Рік народження": "1986", "Тур": "WTA", "Найвищий рейтинг": "№29 WTA", "Досягнення": "2 титули WTA"},
    "alona bondarenko": {"Рік народження": "1984", "Тур": "WTA", "Найвищий рейтинг": "№19 WTA", "Досягнення": "3 титули WTA"},
    "olga savchuk": {"Рік народження": "1987", "Тур": "WTA", "Найвищий рейтинг": "№79 WTA", "Досягнення": "Перемоги в парних турнірах"},
    "veronika podrez": {"Рік народження": "2000", "Тур": "ITF", "Найвищий рейтинг": "№300 WTA", "Досягнення": "Учасниця ITF турнірів"},
    "lyudmyla kichenok": {"Рік народження": "1992", "Тур": "WTA", "Найвищий рейтинг": "№40 WTA", "Досягнення": "1 титул WTA"},
    "nadiia kichenok": {"Рік народження": "1992", "Тур": "WTA", "Найвищий рейтинг": "№56 WTA", "Досягнення": "2 титули WTA"},
    "katarina zavatska": {"Рік народження": "2000", "Тур": "WTA / ITF", "Найвищий рейтинг": "№103 WTA", "Досягнення": "Перемоги на ITF турнірах"},
    "darya snigur": {"Рік народження": "2002", "Тур": "WTA", "Найвищий рейтинг": "№81 WTA", "Досягнення": "Перемоги на турнірах WTA"},
    "oleksandr dovgopolov": {"Рік народження": "1988", "Тур": "ATP", "Найвищий рейтинг": "№13 ATP", "Досягнення": "7 титулів ATP, півфінал Australian Open 2008"},
    "eva lys": {"Рік народження": "2002", "Тур": "WTA", "Найвищий рейтинг": "№120 WTA", "Досягнення": "Перемоги на ITF турнірах"},
    "vladyslav orlov": {"Рік народження": "1995", "Тур": "ATP / Challenger", "Найвищий рейтинг": "№250 ATP", "Досягнення": "Участь у ATP Challenger"},
    "oleksandr ovcharenko": {"Рік народження": "2000", "Тур": "ITF", "Найвищий рейтинг": "№350 ATP", "Досягнення": "Перемоги на ITF турнірах"},
    "yuliia strodubtseva": {"Рік народження": "2000", "Тур": "ITF", "Найвищий рейтинг": "№300 WTA", "Досягнення": "Участь у ITF турнірах"},
    "oleksii krutykh": {"Рік народження": "2001", "Тур": "ATP / Challenger", "Найвищий рейтинг": "№200 ATP", "Досягнення": "Перемоги на ATP Challenger"}
}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Вітаю! Я UkrTennisPlayersBot\n"
        "Введіть ім’я українського тенісиста або тенісистки англійською.\n\n"
        "Наприклад: Elina Svitolina"
    )

# Обробка повідомлень з пошуком за схожістю
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower().strip()

    if user_text in players:
        info = players[user_text]
        response = (
            f"{user_text.title()}\n"
            f"Рік народження: {info['Рік народження']}\n"
            f"Тур: {info['Тур']}\n"
            f"Найвищий рейтинг: {info['Найвищий рейтинг']}\n"
            f"Досягнення: {info['Досягнення']}"
        )
        await update.message.reply_text(response)
    else:
        closest_matches = difflib.get_close_matches(user_text, players.keys(), n=1, cutoff=0.6)
        if closest_matches:
            match = closest_matches[0]
            info = players[match]
            response = (
                f"Можливо, ви мали на увазі: {match.title()}\n\n"
                f"{match.title()}\n"
                f"Рік народження: {info['Рік народження']}\n"
                f"Тур: {info['Тур']}\n"
                f"Найвищий рейтинг: {info['Найвищий рейтинг']}\n"
                f"Досягнення: {info['Досягнення']}"
            )
            await update.message.reply_text(response)
        else:
            await update.message.reply_text(
                "Гравця не знайдено.\n"
                "Спробуйте ввести ім’я ще раз англійською."
            )

# Основна функція запуску бота
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущено...")
    app.run_polling()

if __name__ == "__main__":
    main()