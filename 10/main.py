import telebot
import requests
from telebot import types

# TG
TG_TOKEN = 'TG_TOKEN'
bot = telebot.TeleBot(TG_TOKEN)

# VK
VK_ACCESS_TOKEN = 'VK_ACCESS_TOKEN'
VK_USER_ID = 'VK_USER_ID'


def send_to_vk(message_text, chat_id):
    url = 'https://api.vk.com/method/wall.post'
    params = {
        'access_token': VK_ACCESS_TOKEN,
        'owner_id': VK_USER_ID,
        'message': message_text,
        'privacy_view': 'friends',
        'v': '5.131'
    }

    response = requests.post(url, params=params)

    if response.status_code == 200:
        bot.send_message(chat_id, "Сообщение успешно отправлено в ВКонтакте!")
        print("Сообщение успешно отправлено в ВКонтакте!")
    else:
        bot.send_message(chat_id, f"Ошибка при отправке сообщения: {response.status_code}, {response.text}")
        print(f"Ошибка при отправке сообщения: {response.status_code}, {response.text}")


@bot.message_handler(content_types=['text'])
def handle_message(message):
    text = message.text
    print(f"Получено сообщение от пользователя: {text}")

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button_yes = types.InlineKeyboardButton("Отправить в ВКонтакте", callback_data=f"send_{text}_{message.chat.id}")
    button_no = types.InlineKeyboardButton("Отказаться", callback_data="no")
    keyboard.add(button_yes, button_no)

    bot.send_message(message.chat.id, f"Вы хотите отправить это сообщение: {text} ?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda m: True)
def handle_query(m):
    callback_data = m.data
    chat_id = m.message.chat.id

    if callback_data.startswith('send_'):
        text_to_send = callback_data.split('send_')[1].split('_')[0]
        chat_id_from_callback = callback_data.split('_')[-1]

        send_to_vk(text_to_send, chat_id_from_callback)

    elif callback_data == 'no':
        bot.send_message(chat_id, "Вы отказались от отправки сообщения в ВКонтакте.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
