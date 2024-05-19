import telebot
from telebot import types
import sqlite3
import requests
import time
import socket
import qrcode
import os

token = ''
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])
def start(message):
    user_id = message.from_user.id
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Привет, напиши /help")
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        is_root = 'False'
        user_info = [user_id, first_name, last_name, is_root]
        connection = sqlite3.connect('CopyBotData.db')
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        is_root TEXT
        )
        ''')
        try:
            cursor.execute('INSERT INTO Users (id, name, fname, is_root) VALUES (?, ?, ?, ?)', (user_info))
        except:
            cursor.execute('UPDATE Users SET is_root = ? WHERE id = ?', (is_root, user_id))
            cursor.execute('UPDATE Users SET first_name = ? WHERE id = ?', (first_name, user_id))
            cursor.execute('UPDATE Users SET last_name = ? WHERE id = ?', (last_name, user_id))
    elif message.text == '/help':
        bot.send_message(message.from_user.id, """
        /generate_qrcode - генерирует qr-код содержащий текст или ссылку""")
    elif message.text == '/get_info_by_ip':
        if user_id == 1038243662 or 5251851420:
            bot.send_message(message.from_user.id, "Введи ip адрес")
            bot.register_next_step_handler(message, get_info_by_ip)
        else:
            bot.send_message(message.from_user.id, "[!]СЛИШКОМ_НИЗКИЙ_УРОВЕНЬ_ДОСТУПА[!]")
    elif message.text == '/get_ip_by_hostname':
        if user_id == 1038243662 or 5251851420:
            bot.send_message(message.from_user.id, "Введи url адрес (например: google.com)")
            bot.register_next_step_handler(message, get_ip_by_hostname)
        else:
            bot.send_message(message.from_user.id, "[!]СЛИШКОМ_НИЗКИЙ_УРОВЕНЬ_ДОСТУПА[!]")
    elif message.text == '/get_locate_by_ip':
        if user_id == 1038243662 or 5251851420:
            bot.send_message(message.from_user.id, "Введи ip адрес")
            bot.register_next_step_handler(message, get_locate_by_ip)
        else:
            bot.send_message(message.from_user.id, "[!]СЛИШКОМ_НИЗКИЙ_УРОВЕНЬ_ДОСТУПА[!]")
    elif message.text == '/generate_qrcode':
        bot.send_message(message.from_user.id, "Введи ссылку или текст")
        bot.register_next_step_handler(message, generate_qrcode)

def get_info_by_ip(message):
    ip = message.text
    try:
        response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
        bot.send_message(message.from_user.id, f"""
        [IP]: {response.get('query')},
        [STATUS]: {response.get('status')},
        [COUNTRY]: {response.get('country')},
        [COUNTRY_CODE]: {response.get('countryCode')},
        [REGION]: {response.get('region')},
        [REGION_NAME]: {response.get('regionName')},
        [CITY]: {response.get('city')},
        [ZIP]: {response.get('zip')},
        [LAT]: {response.get('lat')},
        [LON]: {response.get('lon')},
        [TIMEZONE]: {response.get('timezone')},
        [ISP]: {response.get('isp')},
        [ORG]: {response.get('org')},
        [AS]: {response.get('as')}""")
    except requests.exceptions.ConnectionError:
        bot.send_message(message.from_user.id, '[!]requests.exceptions.ConnectionError[!]')

def get_locate_by_ip(message):
    ip = message.text
    try:
        for i in range(120):
            response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
            bot.send_message(message.from_user.id, f"""
                [IP]: {response.get('query')},
                [COUNTRY_CODE]: {response.get('countryCode')},
                [CITY]: {response.get('city')},
                [LAT]: {response.get('lat')},
                [LON]: {response.get('lon')},""")
            time.sleep(2)
    except requests.exceptions.ConnectionError:
        bot.send_message(message.from_user.id, '[!]requests.exceptions.ConnectionError[!]')

def get_ip_by_hostname(message):
    hostname = message.text
    try:
        bot.send_message(message.from_user.id, f'{socket.gethostbyname(hostname)}')
    except socket.gaierror as error:
        bot.send_message(message.from_user.id, f'[!]Invailid Hostname - {error}[!]')

def generate_qrcode(message):
    user_id = message.from_user.id
    url = message.text
    name = f'qr_{user_id}.png'
    qr = qrcode.make(data=url)
    qr.save(stream=f'{name}')
    bot.send_photo(message.from_user.id, photo=open(f'{name}', 'rb'))
    os.remove(name)

bot.polling(none_stop=True, interval=0)