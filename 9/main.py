import telebot
from telebot import types
import json


TOKEN = 'BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)


def load_data():
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

QandA = load_data()['questions']
results = load_data()['results']

votes = {question: {option: 0 for option in QandA[question]['options']} for question in QandA}  # {question: {option: count}}
user_votes = {}  # {user_id: {question: chosen_option}}

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, 'Привет! 👋')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(name, callback_data=name) for name in
                   ['Тесты 📋', 'Полезные советы 🪄', 'Информация ℹ️']])

    bot.send_message(m.chat.id, 'Небольшой психологический сеанс, направленный на понимание себя и поиск ответов 🤔',
                     reply_markup=keyboard)

# Основной обработчик всех callback-запросов
@bot.callback_query_handler(func=lambda m: True)
def handle_query(m):
    # Обработка пунктов главного меню
    if m.data == 'Тесты 📋':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*[types.InlineKeyboardButton(name, callback_data=name) for name in
                       ['Вопрос 1: Двери 🚪', 'Вопрос 2: Действие 🧑‍🦳', 'Вопрос 3: Фигуры 🔺', 'Вопрос 4: Картинка 🖼️', 'Вернуться назад 🔙']])
        bot.send_message(m.message.chat.id, 'Выберите вопрос для теста 📜:', reply_markup=keyboard)

    elif m.data == 'Полезные советы 🪄':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*[types.InlineKeyboardButton(name, callback_data=name) for name in
                       ['Как быть счастливым? 😊', 'Как перестать переживать? 😌', 'Вернуться назад 🔙']])
        bot.send_message(m.message.chat.id, 'Выберите секрет жизни 🌟:', reply_markup=keyboard)

    elif m.data == 'Информация ℹ️':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*[types.InlineKeyboardButton(name, callback_data=name) for name in
                       ['Об авторе ✍️', 'Поддержка 🆘', 'Вернуться назад 🔙']])
        bot.send_message(m.message.chat.id, 'Выберите раздел информации 📚:', reply_markup=keyboard)

    # Обработка тестовых вопросов
    elif m.data == 'Вопрос 1: Двери 🚪':
        bot.send_message(m.message.chat.id, 'Представьте, что вы оказались перед четырьмя дверями. '
                                            'Войдите в одну из них в поисках выхода. Осмотритесь по сторонам. '
                                            'Ответьте на вопросы: Как она выглядит? Какие чувства и мысли у вас '
                                            'возникают? Запомните все, что увидели и почувствовали. А затем выходите.')
        ask_question(m, 'Вопрос 1')

    elif m.data == 'Вопрос 2: Действие 🧑‍🦳':
        bot.send_message(m.message.chat.id, 'Выберите одно из четырех действий в ситуации на картинке ниже.')
        ask_question(m, 'Вопрос 2')

    elif m.data == 'Вопрос 3: Фигуры 🔺':
        bot.send_message(m.message.chat.id, 'Взгляните на эти геометрические фигуры. Какая из них вам ближе?')
        ask_question(m, 'Вопрос 3')

    elif m.data == 'Вопрос 4: Картинка 🖼️':
        bot.send_message(m.message.chat.id, 'Посмотрите на эту картинку и скажите, что вы увидели на ней первым?')
        ask_question(m, 'Вопрос 4')

    elif m.data.startswith("Вопрос"):
        question, option = m.data.split("_")
        user_votes[m.message.from_user.id] = user_votes.get(m.message.from_user.id, {})
        user_votes[m.message.from_user.id][question] = option

        votes[question][option] += 1
        display_votes(m, question)

        callback_data = m.data.split('_')
        if len(callback_data) > 1:
            question = callback_data[0]
            choice = callback_data[1]
            result_message = results.get(choice, 'Результат не найден')

            bot.send_message(m.message.chat.id, result_message)

            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton('Назад к тестам 📋', callback_data='Тесты 📋'))
            bot.send_message(m.message.chat.id, 'Вы можете вернуться к тестам:', reply_markup=keyboard)

    elif m.data == 'Как быть счастливым? 😊':
        bot.send_message(m.message.chat.id,
                         'Счастье начинается с принятия себя и благодарности за то, что у вас есть 🙏'
                         'Сфокусируйтесь на позитиве и маленьких радостях жизни 🌸')

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('20 вещей, которые надо отпустить, чтобы стать счастливым',
                                                url='https://lifehacker.ru/20-veshhej-kotorye-nado-otpustit-chtoby-byt-schastlivym/'))

        image_url = 'https://www.litres.ru/pub/c/cover/6881047.jpg'

        bot.send_message(m.message.chat.id, 'Полезная статья и книга по теме: ', reply_markup=keyboard)
        bot.send_photo(m.message.chat.id, image_url)
        bot.send_message(m.message.chat.id,
                         'Как быть счастливым. 128 советов, как жить в любви и гармонии — Мринал Кумар Гупта')

    elif m.data == 'Как перестать переживать? 😌':
        bot.send_message(m.message.chat.id,
                         'Для того чтобы перестать переживать, учитесь отпускать вещи, которые вы не можете контролировать 🌬️. '
                         'Практикуйте осознанность 🧘 и дыхательные упражнения 🌿')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('Как меньше переживать из-за ерунды', url='https://t-j.ru/short/stop-worrying/'))

        image_url = 'https://www.litres.ru/pub/c/cover/21128756.jpg'

        bot.send_message(m.message.chat.id, 'Полезная статья и книга по теме: ', reply_markup=keyboard)
        bot.send_photo(m.message.chat.id, image_url)
        bot.send_message(m.message.chat.id,
                         'Как перестать беспокоиться и начать жить — Дейл Карнеги')

    elif m.data == 'Об авторе ✍️':
        bot.send_message(m.message.chat.id, 'Автор бота — разработчик с любовью к психологии и саморазвитию ❤️.')

    elif m.data == 'Поддержка 🆘':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('Написать в Telegram', url='https://t.me/lab_7_test_bot'))
        bot.send_message(m.message.chat.id, 'Если вам нужна поддержка, напишите нам в Telegram 📱: ', reply_markup=keyboard)

    elif m.data == 'Вернуться назад 🔙':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(name, callback_data=name) for name in
                       ['Тесты 📋', 'Полезные советы 🪄', 'Информация ℹ️']])
        bot.send_message(m.message.chat.id, 'Выберите раздел снова 🔄:', reply_markup=keyboard)


def ask_question(m, question):
    image_url = QandA[question]['image']
    bot.send_photo(m.message.chat.id, image_url)

    keyboard = types.InlineKeyboardMarkup()
    for option in QandA[question]['options']:
        button = types.InlineKeyboardButton(text=option, callback_data=f'{question}_{option}')
        keyboard.add(button)
    bot.send_message(m.message.chat.id, f'Выберите вариант: {question}', reply_markup=keyboard)


def display_votes(m, question):
    vote_text = "Голоса за каждый вариант:\n"
    for option, vote_count in votes[question].items():
        vote_text += f"{option}: {vote_count} голосов\n"

    bot.send_message(m.message.chat.id, vote_text)


if __name__ == "__main__":
    bot.polling(none_stop=True)
