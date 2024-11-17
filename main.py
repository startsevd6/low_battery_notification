import os
from dotenv import load_dotenv
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import psutil


load_dotenv(dotenv_path=".venv/.env")

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

bot = telebot.TeleBot(BOT_TOKEN)

def sent_current_charge(user_id):
    hours = psutil.sensors_battery()[1] // 3600
    minutes = psutil.sensors_battery()[1] % 3600 // 60
    answer = "Заряд батареи: " + str(psutil.sensors_battery()[0]) + "%\nЭтого хватит на"
    if hours != 0:
        answer += " " + str(hours)
        if hours % 10 in [0, 5, 6, 7, 8, 9]:
            answer += " часов"
        if hours % 10 in [2, 3, 4]:
            answer += " часа"
        if hours % 10 in [1]:
            answer += " час"
    if minutes != 0:
        answer += " " + str(minutes)
        if minutes % 10 in [0, 5, 6, 7, 8, 9]:
            answer += " минут"
        if minutes % 10 in [2, 3, 4]:
            answer += " минуты"
        if minutes % 10 in [1]:
            answer += " минута"
    bot.send_message(user_id, answer)


if psutil.sensors_battery()[0] <= 20:
    sent_current_charge(ADMIN_ID)


if psutil.sensors_battery()[2] == 0:
    bot.send_message(ADMIN_ID, "Зарядка отключена")
    sent_current_charge(ADMIN_ID)
elif psutil.sensors_battery()[2] == 1:
    bot.send_message(ADMIN_ID, "Зарядка подключена")
    sent_current_charge(ADMIN_ID)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создаем клавиатуру
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # Добавляем кнопку
    button = KeyboardButton('заряд')
    markup.add(button)
    # Отправляем сообщение с клавиатурой
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши заряд")
    elif message.text.find("заряд") != -1:
        sent_current_charge(message.from_user.id)
        send_welcome(message)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
bot.polling(none_stop=True, interval=0)
