from bs4 import BeautifulSoup as bsp
import requests
import telebot
from fake_useragent import UserAgent

UserAgent().chrome

url = 'https://www.gismeteo.ru/weather-sankt-peterburg-4079/'
page = requests.get(url, headers={'User-Agent': UserAgent().chrome})

soup = bsp(page.text, 'html.parser')
weather = soup.findAll('span', class_='js_value tab-weather__value_l')

weather_first = (weather[0].text)
print(weather_first.strip())


bot = telebot.TeleBot('1073429036:AAGHTJq2nEdp1nbo6-7zpaPECG7x79bH908')
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, питушара. В Питере" + weather_first.strip())
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


try:
    print('started')
    port = int(os.getenv("PORT", default="9999"))
    t = threading.Thread(target=forever_thread, daemon=True)
    t.start()
    bot.polling()
except:
    pass

