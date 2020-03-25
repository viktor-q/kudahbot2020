from bs4 import BeautifulSoup as bsp
import requests
import telebot
from fake_useragent import UserAgent
import socketserver
import threading
import os
import http

def weathercheck():
    UserAgent().chrome
    url = 'https://www.gismeteo.ru/weather-sankt-peterburg-4079/'
    page = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    soup = bsp(page.text, 'html.parser')
    weather = soup.findAll('span', class_='js_value tab-weather__value_l')
    weather_first = (weather[0].text)
    return weather_first.strip()

# проверяем парсер
print("Парсер погоды отработал и возвращает " + weathercheck())

#bot = telebot.TeleBot('1073429036:AAGHTJq2nEdp1nbo6-7zpaPECG7x79bH908')
bot = telebot.TeleBot('1014012992:AAGJcR4WCaYO2cSAoEf25ChHJsZI7_Jhh1s')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, питушара. В Питере" + weathercheck())
        # проверяем ответ на привет
        print("Отклик на привет")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
#bot.polling(none_stop=True, interval=0)

def forever_thread():
    global port
    PORT = port
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()


print('started')
port = int(os.getenv("PORT", default="9999"))
t = threading.Thread(target=forever_thread, daemon=True)
t.start()
bot.polling()