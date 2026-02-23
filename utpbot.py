from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import difflib
import openai
import config  # імпорт токенів з config.py

# Ініціалізація OpenAI
openai.api_key = config.OPENAI_API_KEY

# Локальна база гравців
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


# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Вітаю! Я UkrTennisPlayersBot.\n"
        "Введіть ім’я українського тенісиста/ки англійською.\n\n"
        "Щоб отримати AI-біографію українською, використайте команду:\n"
        "/bio <ім’я гравця>"
    )

# Пошук гравця
def find_player(name: str) -> str:
    name = name.lower().strip()
    if name in players:
        return name
    matches = difflib.get_close_matches(name, players.keys(), n=1, cutoff=0.6)
    return matches[0] if matches else None

# Формат локальної інформації
def format_player_info(name: str) -> str:
    info = players[name]
    return (
        f"{name.title()}\n"
        f"Рік народження: {info['Рік народження']}\n"
        f"Тур: {info['Тур']}\n"
        f"Найвищий рейтинг: {info['Найвищий рейтинг']}\n"
        f"Досягнення: {info['Досягнення']}"
    )

# AI-біографія українською
def get_ai_bio_ukr(player_name: str) -> str:
    prompt = (
        f"Напиши детальну біографію українського тенісиста/ки {player_name} українською. "
        "Включи рік народження, турніри, стиль гри та цікаві факти."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Помилка при отриманні AI-даних: {e}"

# Обробка тексту
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    match = find_player(user_text)
    if match:
        info_text = format_player_info(match)
        await update.message.reply_text(info_text)
    else:
        possible = difflib.get_close_matches(user_text.lower(), players.keys(), n=3, cutoff=0.5)
        suggestion = f"\nСхожі варіанти: {', '.join(possible)}" if possible else ""
        await update.message.reply_text(
            "Гравця не знайдено. Спробуйте ще раз англійською." + suggestion
        )

# Команда /bio
async def bio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Введіть ім’я гравця після команди /bio")
        return

    user_input = " ".join(context.args)
    match = find_player(user_input)
    if match:
        info_text = format_player_info(match)
        ai_text = get_ai_bio_ukr(match.title())
        response = f"{info_text}\n\nAI-біографія:\n{ai_text}"
        await update.message.reply_text(response)
    else:
        possible = difflib.get_close_matches(user_input.lower(), players.keys(), n=3, cutoff=0.5)
        suggestion = f"\nСхожі варіанти: {', '.join(possible)}" if possible else ""
        await update.message.reply_text("Гравця не знайдено." + suggestion)

# Запуск бота
def main():
    app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bio", bio_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущено...")
    app.run_polling()

if __name__ == "__main__":
    main()