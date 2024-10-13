import telebot
import requests
import json
from config import tg_bot_token, weather_token

bot = telebot.TeleBot(tg_bot_token)


@bot.message_handler(commands=["start"])
def main(message):
    bot.send_message(message.chat.id, "Привет! Введи название города.")
    
@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip()
    r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric&lang=ru')
    if r.status_code == 200:
        data = json.loads(r.text)
        temp = int(data["main"]["temp"])
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        bot.reply_to(message, f'Сейчас в {city} температура: {temp}°C, влажность: {humidity}%, на улице {description}')
    else:
        bot.reply_to(message, 'Город указан неверно')
        
bot.polling(non_stop=True)