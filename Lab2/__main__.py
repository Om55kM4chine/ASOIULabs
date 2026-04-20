import time
import random
import asyncio
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

class Tamagotchi:
    def __init__(self, name):
        self.name = name
        self.hunger = 100
        self.thirst = 100
        self.happiness = 100

    def feed(self):
        self.hunger += 20
        if self.hunger > 100:
            self.hunger = 100

    def give_water(self):
        self.thirst += 20
        if self.thirst > 100:
            self.thirst = 100

    def play(self):
        self.happiness += 20
        if self.happiness > 100:
            self.happiness = 100

    def decrease_stats(self):
        self.hunger -= random.randint(5, 15)
        self.thirst -= random.randint(5, 15)
        self.happiness -= random.randint(5, 15)

    def is_alive(self):
        return self.hunger > 0 and self.thirst > 0 and self.happiness > 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Давай создадим твоего тамагочи. Введи имя:")
    context.user_data['waiting_for_name'] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('waiting_for_name'):
        name = update.message.text
        tamagotchi = Tamagotchi(name)
        context.user_data['tamagotchi'] = tamagotchi
        context.user_data['waiting_for_name'] = False
        await show_status(update, context)
    else:
        await update.message.reply_text("Используй команды или кнопки для взаимодействия с тамагочи.")

async def show_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tamagotchi = context.user_data.get('tamagotchi')
    if not tamagotchi:
        await update.message.reply_text("Сначала создай тамагочи с /start")
        return

    if not tamagotchi.is_alive():
        await update.message.reply_text(f"{tamagotchi.name} умер. Начни заново с /start")
        return

    status = f"{tamagotchi.name}\nГолод: {tamagotchi.hunger}\nЖажда: {tamagotchi.thirst}\nСчастье: {tamagotchi.happiness}"

    keyboard = [
        [InlineKeyboardButton("Кормить", callback_data='feed')],
        [InlineKeyboardButton("Дать воду", callback_data='water')],
        [InlineKeyboardButton("Играть", callback_data='play')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(status, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(status, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    tamagotchi = context.user_data.get('tamagotchi')
    if not tamagotchi or not tamagotchi.is_alive():
        await query.edit_message_text("Тамагочи умер. Начни заново с /start")
        return

    action = query.data
    if action == 'feed':
        tamagotchi.feed()
        response = "Ты покормил тамагочи!"
    elif action == 'water':
        tamagotchi.give_water()
        response = "Ты дал воды тамагочи!"
    elif action == 'play':
        tamagotchi.play()
        response = "Ты поиграл с тамагочи!"

    tamagotchi.decrease_stats()

    status = f"{tamagotchi.name}\nГолод: {tamagotchi.hunger}\nЖажда: {tamagotchi.thirst}\nСчастье: {tamagotchi.happiness}"

    keyboard = [
        [InlineKeyboardButton("Кормить", callback_data='feed')],
        [InlineKeyboardButton("Дать воду", callback_data='water')],
        [InlineKeyboardButton("Играть", callback_data='play')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    full_message = f"{response}\n\n{status}"
    await query.edit_message_text(full_message, reply_markup=reply_markup)

def main():
    load_dotenv()
    token = os.getenv('BOT_TOKEN')
    if not token:
        print("Ошибка: BOT_TOKEN не найден в .env файле")
        return

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Обработчик для сообщений (для имени)
    from telegram.ext import MessageHandler, filters
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()