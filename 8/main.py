# -*- coding: utf-8 -*-
import telebot
from telebot import types

TOKEN = 'BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)
points = 0

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, 'Привет! 👋')

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Тесты 📋', 'Полезные советы 🪄', 'Информация ℹ️']])

    msg = bot.send_message(m.chat.id, 'Небольшой психологический сеанс, направленный на понимание себя и поиск ответов 🤔', reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def name(m):
    if m.text == 'Тесты 📋':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in
                       ['Интроверт или экстраверт? 🤫', 'Пессимист или оптимист? 🌞',
                        'Вернуться назад 🔙']])
        bot.send_message(m.chat.id, 'Выберите тест 📜:', reply_markup=keyboard)
    elif m.text == 'Полезные советы 🪄':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in
                       ['Как быть счастливым? 😊', 'Как перестать переживать? 😌', 'Вернуться назад 🔙']])
        bot.send_message(m.chat.id, 'Выберите секрет жизни 🌟:', reply_markup=keyboard)
    elif m.text == 'Информация ℹ️':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Об авторе ✍️', 'Поддержка 🆘', 'Вернуться назад 🔙']])
        bot.send_message(m.chat.id, 'Выберите раздел информации 📚:', reply_markup=keyboard)

    elif m.text == 'Интроверт или экстраверт? 🤫':
        bot.send_message(m.chat.id, 'Вы выбрали тест "Интроверт или экстраверт?" 🤔')
        testIE(m)
    elif m.text == 'Пессимист или оптимист? 🌞':
        bot.send_message(m.chat.id, 'Вы выбрали тест "Пессимист или оптимист?" 🌈')
        testPO(m)

    elif m.text == 'Как быть счастливым? 😊':
        bot.send_message(m.chat.id,
                         'Счастье начинается с принятия себя и благодарности за то, что у вас есть 🙏. '
                         'Сфокусируйтесь на позитиве и маленьких радостях жизни 🌸.')
    elif m.text == 'Как перестать переживать? 😌':
        bot.send_message(m.chat.id,
                         'Для того чтобы перестать переживать, учитесь отпускать вещи, которые вы не можете контролировать 🌬️. '
                         'Практикуйте осознанность 🧘 и дыхательные упражнения 🌿.')

    elif m.text == 'Об авторе ✍️':
        bot.send_message(m.chat.id, 'Автор бота — разработчик с любовью к психологии и саморазвитию ❤️.')
    elif m.text == 'Поддержка 🆘':
        bot.send_message(m.chat.id, 'Если вам нужна поддержка, напишите на наш электронный адрес: support@example.com 📧.')

    elif m.text == 'Вернуться назад 🔙':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Тесты 📋', 'Полезные советы 🪄', 'Информация ℹ️']])

        bot.send_message(m.chat.id, 'Выберите раздел снова 🔄:', reply_markup=keyboard)

def testIE(m):
    global points
    global a_count, b_count
    points = 0
    a_count, b_count = 0, 0

    bot.send_message(m.chat.id, 'Прочитайте фразы. Какие из них вам ближе? 👀')

    QandA = {
        'Вопрос 1': ['Мне редко бывает скучно', 'Я часто скучаю'],
        'Вопрос 2': ['Я не люблю быстрой езды', 'Мне нравится скорость, когда замираешь от страха'],
        'Вопрос 3': ['Я предпочитаю провести вечер дома с друзьями', 'Мне больше нравится проводить время в большой шумной компании'],
        'Вопрос 4': ['Иногда мне нравится быть одному (одной)', 'Я ненавижу оставаться в одиночестве'],
        'Вопрос 5': ['Я предпочитаю иметь несколько близких людей', 'Лучше, если есть множество знакомых'],
        'Вопрос 6': ['Лучше писать книги, чем что-нибудь продавать', 'Лучше продавать что-либо, чем писать книги'],
        'Вопрос 7': ['Я едва ли пойду на риск', 'Я радуюсь любому случаю рискнуть'],
        'Вопрос 8': ['Я считаю первоапрелькие шуточки просто глупостью', 'первого апреля можно здорово повеселиться'],
        'Вопрос 9': ['Едва ли вам удастся застать меня смотрящим по телевизору «Маски-шоу»', 'По-моему, «Маски-шоу» - очень смешная передача'],
        'Вопрос 10': ['Я люблю разговоры на отвлеченные темы', 'Для меня чем о чем-то рассуждать, лучше что-нибудь сделать'],
        'Вопрос 11': ['Во время игры в прятки я спрячусь за деревом', 'Во время игры в прятки я спрячусь на дереве'],
        'Вопрос 12': ['Я избегаю толпы', 'Я хорошо себя чувствую в толпе'],
        'Вопрос 13': ['Я не люблю танцевать', 'Я люблю танцевать'],
        'Вопрос 14': ['Машины с открытым верхом опасны, лучше в них не ездить', 'На машинах с открытым верхом ездить веселей'],
        'Вопрос 15': ['Я предпочитаю действовать за кулисами', 'Мне больше нравится быть на авансцене']
    }

    asking(m, "I or E?", list(QandA.items()), 0)


def testPO(m):
    global points
    global a_count, b_count
    points = 0
    a_count, b_count = 0, 0
    bot.send_message(m.chat.id, 'О чем вы подумали, прочитав приведенные ниже слова? 💭')

    QandA = {
        'ТРУБА': ['музыка', 'канализация'],
        'ФИГА': ['фрукт', 'отказ'],
        'ЛУК': ['стрелы', 'слезы'],
        'ПРОЛЕТ': ['мост', 'неудача'],
        'РАК': ['животное', 'болезнь'],
        'ТРЮК': ['фокус', 'обман'],
        'УДАР': ['футбол', 'синяк'],
        'МАХ': ['гимнастика', 'ошибка']
    }

    asking(m, "O or P?", list(QandA.items()), 0)


def asking(m, test_name, q, ind):
    global points
    global a_count, b_count

    if ind >= len(q):
        bot.send_message(m.chat.id, f'Тест завершен! 🎉 Из всех {points} ответов вы выбирали вариант а {a_count} раз, '
                                    f'а вариант б {b_count} раз! Обрабатываю результат... 🤔')
        process_results(m, test_name)

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton('Вернуться назад 🔙'))
        bot.send_message(m.chat.id, 'Вы можете вернуться назад в меню 🔄.', reply_markup=keyboard)
        return

    question, options = q[ind]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('а'), types.KeyboardButton('б'))

    msg_text = f"{question}\n\nа: {options[0]}\nб: {options[1]}"

    msg = bot.send_message(m.chat.id, msg_text, reply_markup=keyboard)
    bot.register_next_step_handler(msg, process_answer, test_name, q, ind)


def process_answer(m, test_name, questions, index):
    global points
    global a_count, b_count
    points += 1
    if m.text == 'а':
        a_count += 1
    elif m.text == 'б':
        b_count += 1

    asking(m, test_name, questions, index + 1)


def process_results(m, test_name):
    global points
    global a_count, b_count

    if test_name == "O or P?":
        if a_count >= 6:
            bot.send_message(m.chat.id, 'Вы оптимист! 🌞 Позитивное восприятие помогает вам справляться с трудностями 😊.')
        elif b_count >= 6:
            bot.send_message(m.chat.id, 'Вы пессимист! 🌧️ Но помните, что иногда пессимизм помогает предвидеть трудности ⚠️.')
    elif test_name == "I or E?":
        if a_count >= 10:
            bot.send_message(m.chat.id,
                             'Вы интроверт! 😌 Вам лучше в тихой и спокойной обстановке, без лишнего шума и суеты.')
        elif b_count >= 10:
            bot.send_message(m.chat.id,
                             'Вы экстраверт! 🎉 Вам нравится быть в центре внимания и черпать энергию от общения с людьми.')
        else:
            bot.send_message(m.chat.id, 'Вы сбалансированы! ⚖️ Вам комфортно как с людьми, так и в одиночестве.')

        bot.send_message(m.chat.id, 'Помните, что для гармонии важны как моменты одиночества, так и общение с окружающими! 🌿')

if __name__ == "__main__":
    bot.polling(none_stop=True)