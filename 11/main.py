import matplotlib
matplotlib.use('Agg')

import math
import re
import matplotlib.pyplot as plt
import io
from PIL import Image
import xml.dom.minidom
import requests
import telebot
from telebot import types

# TG
TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)

dict_of_names = dict()  # {ID: Names}
dict_of_val = dict()  # {ID: [Value, CharCode]}
user_page_clicks = {}


def parse_val(Id, data_start=None, data_end=None):
    global dict_of_val
    if data_start and data_end:
        data_start = data_start.replace('.', '/')
        data_end = data_end.replace('.', '/')
        r = requests.get(
            f'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={data_start}&date_req2={data_end}&VAL_NM_RQ={Id}')

    dom = xml.dom.minidom.parseString(r.text)
    dom.normalize()
    items = dom.getElementsByTagName('Record')

    dict_of_val = dict()
    for item in items:
        date = item.getAttribute('Date')
        vunit_rate = item.getElementsByTagName('VunitRate')[0].firstChild.nodeValue
        dict_of_val[date] = vunit_rate


def parse_dict():
    global dict_of_names
    r = requests.get('http://www.cbr.ru/scripts/XML_val.asp?d=0')
    dom = xml.dom.minidom.parseString(r.text)
    dom.normalize()
    items = dom.getElementsByTagName('Item')

    dict_of_names = dict()
    for item in items:
        if not(item.getElementsByTagName('Name')[0].firstChild.nodeValue in list(dict_of_names.values())):
            dict_of_names[item.getAttribute('ID')] = item.getElementsByTagName('Name')[0].firstChild.nodeValue


def get_course(name_of_val):
    global dict_of_names
    ind = -1
    for i in dict_of_names.items():
        if i[1] == name_of_val:
            ind = i[0]
    return ind


# def get_val(ind):
#     global dict_of_val
#     coarse = []
#     if ind != -1:
#         for i in dict_of_val.items():
#             if i[0] == ind:
#                 coarse = i[1]
#     return coarse


@bot.message_handler(commands=['start'])
def start(m):
    chat_id = m.chat.id
    if chat_id not in user_page_clicks:
        user_page_clicks[chat_id] = 0  # Initialize clicks for new user

    parse_dict()
    MAX_CLICKS = math.ceil(len(dict_of_names) / 10)

    bot.send_message(m.chat.id, 'Здравствуйте! Здесь вы можете получить информацию о курсе валют')
    keyboard = generate_keyboard(chat_id, MAX_CLICKS)
    bot.send_message(m.chat.id, 'Выберите интересующую вас валюту', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda m: True)
def handle_query(m):
    chat_id = m.message.chat.id

    if m.data == 'Вернуться назад 🔙':
        user_page_clicks[chat_id] = 0
        keyboard = generate_keyboard(chat_id, math.ceil(len(dict_of_names) / 10))
        bot.edit_message_text('Выберите интересующую вас валюту', m.message.chat.id, m.message.message_id, reply_markup=keyboard)
    elif m.data == 'next_page' and user_page_clicks[chat_id] < math.ceil(len(dict_of_names) / 10) - 1:
        user_page_clicks[chat_id] += 1
        keyboard = generate_keyboard(chat_id, math.ceil(len(dict_of_names) / 10))
        bot.edit_message_reply_markup(m.message.chat.id, m.message.message_id, reply_markup=keyboard)
    else:
        id = get_course(m.data)
        if id != -1:
            bot.send_message(m.message.chat.id,
                             f'Вы выбрали валюту: {dict_of_names[id]}. Пожалуйста, введите период в формате – dd/mm/yyyy - dd/mm/yyyy')
            bot.register_next_step_handler(m.message, get_period, id)
        else:
            bot.send_message(m.message.chat.id, 'Не удалось найти валюту.')


def generate_graph():
    global dict_of_val

    dates = list(dict_of_val.keys())
    rates = list(dict_of_val.values())

    rates = [float(rate.replace(',', '.')) for rate in rates]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, rates, marker='o', linestyle='-', color='b')
    plt.xlabel('Дата')
    plt.ylabel('Курс')
    plt.title('Динамика курса валют')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image = Image.open(buf)
    return image


def get_period(message, currency_id):
    period = message.text.strip()
    period_pattern = r'^\d{2}/\d{2}/\d{4} - \d{2}/\d{2}/\d{4}$'
    if re.match(period_pattern, period):
        try:
            data_start, data_end = period.split(" - ")
            parse_val(currency_id, data_start, data_end)
            bot.send_message(message.chat.id, f"Курс на период с {data_start} по {data_end} для {dict_of_names[currency_id]}")
            if dict_of_val:
                for date, value in dict_of_val.items():
                    bot.send_message(message.chat.id, f"Дата: {date} - Курс: {value}")
                image = generate_graph()
                bot.send_photo(message.chat.id, image)

            else:
                bot.send_message(message.chat.id, 'Не удалось получить курс на указанный период.')
        except ValueError:
            bot.send_message(message.chat.id, 'Ошибка при обработке периода. Пожалуйста, попробуйте снова.')
            bot.register_next_step_handler(message, get_period, currency_id)
    else:
        bot.send_message(message.chat.id, 'Некорректный формат периода. Пожалуйста, введите период в формате dd/mm/yyyy - dd/mm/yyyy.')
        bot.register_next_step_handler(message, get_period, currency_id)


def get_date(message, currency_id):
    period = message.text.strip()
    print(period)

    if len(period) == 21:
        start, end = period.split('-')
        parse_val(currency_id, start, end)
        bot.send_message(message.chat.id, f"Динамика курса за период {start}-{end} для {dict_of_names[currency_id]}")
        if dict_of_val:
            for value, char_code in dict_of_val.items():
                 bot.send_message(message.chat.id, f"({char_code}): {value}")
        else:
            bot.send_message(message.chat.id, 'Не удалось получить курс на указанную дату.')

        keyboard = generate_keyboard(message.chat.id, math.ceil(len(dict_of_names) / 10))
        bot.send_message(message.chat.id, "Хотите выбрать другую валюту?", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Некорректная дата. Пожалуйста, введите дату в формате dd/mm/yyyy.')
        bot.register_next_step_handler(message, get_date, currency_id)


def generate_keyboard(chat_id, max_clicks):
    start_index = user_page_clicks.get(chat_id, 0) * 10
    end_index = start_index + 10
    total_values = len(dict_of_names)

    items_to_show = min(10, total_values - start_index)
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    keyboard.add(*[types.InlineKeyboardButton(name, callback_data=name) for name in
                   list(dict_of_names.values())[start_index:start_index + items_to_show]])
    if end_index < total_values and user_page_clicks[chat_id] < max_clicks - 1:
        keyboard.add(types.InlineKeyboardButton("Далее ➡️", callback_data="next_page"))

    keyboard.add(types.InlineKeyboardButton("Вернуться назад 🔙", callback_data="Вернуться назад 🔙"))

    return keyboard


if __name__ == "__main__":
    bot.polling(none_stop=True)
