from bs4 import BeautifulSoup as bsp
import requests
import telebot
from fake_useragent import UserAgent
import socketserver
import threading
import os
import http.server

from requests import session
import json
from pprint import pprint

def weathercheck():
    UserAgent().chrome
    url = 'https://www.gismeteo.ru/weather-sankt-peterburg-4079/'
    page = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    soup = bsp(page.text, 'html.parser')
    weather = soup.findAll('span', class_='js_value tab-weather__value_l')
    weather_first = (weather[0].text)
    return weather_first.strip()

def coincheck():
    UserAgent().chrome
    url = 'https://yandex.ru/'
    page = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    soup = bsp(page.text, 'html.parser')
    coin = soup.findAll('span', class_='inline-stocks__value_inner')
    coin_first = (coin[0].text)
    return (coin_first.strip())

def petrolcheck():
    my_session = session()

    my_session.headers['Host'] = 'www.rosneft-azs.ru'
    my_session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'
    my_session.headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    my_session.headers['Accept-Language'] = 'ru-RU'
    my_session.headers['Accept-Encoding'] = 'gzip, deflate'
    my_session.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    my_session.headers['X-Requested-With'] = 'XMLHttpRequest'
    my_session.headers['Content-Length'] = '9'
    my_session.headers['Origin'] = 'http://www.rosneft-azs.ru'
    my_session.headers['Connection'] = 'keep-alive'
    my_session.headers['Referer'] = 'http://www.rosneft-azs.ru/fuel_search'
    my_session.headers['Pragma'] = 'no-cache'
    my_session.headers['Cache-Control'] = 'no-cache'

    # print(my_session.headers)
    all_request = my_session.post('http://www.rosneft-azs.ru/fuel_search', data={'region': "78"})
    # print(all_request.text)
    all_rec_string = json.loads(all_request.text)
    for elem in all_rec_string['price']:
        if elem['type'] == '95':
            extract = elem['avg']
            return int(float(extract) * 100) / 100


# проверяем парсер
print("Парсер погоды отработал и возвращает " + weathercheck())

#bot = telebot.TeleBot('1073429036:AAGHTJq2nEdp1nbo6-7zpaPECG7x79bH908')
bot = telebot.TeleBot('1014012992:AAGJcR4WCaYO2cSAoEf25ChHJsZI7_Jhh1s')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, питушара. В Питере " + weathercheck())
        bot.send_message(message.from_user.id, "А между прочим, бакс сейчас стоит " + coincheck())
        bot.send_message(message.from_user.id, "Если задумал заправить свой сраный трактор и свалить из сраной рашки, то бензинчик сейчас стоит " + str(petrolcheck()))
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