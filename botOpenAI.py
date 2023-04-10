import telebot
import openai
from telebot import types
import random

# Отримання API ключів для Telegram та OpenAI
TELEGRAM_API_KEY = '5646599316:AAFVGWqEAgPmlvpUByhFwmbDjB-1UFY7LWY'
OPENAI_API_KEY = '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'

# Ініціалізація бота Telegram
bot = telebot.TeleBot(TELEGRAM_API_KEY)

# Функція для відправлення текстової відповіді користувачу
def send_text_reply(chat_id, reply):
    bot.send_message(chat_id, reply)

# Встановлення API ключа OpenAI
openai.api_key = OPENAI_API_KEY

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text_message(message):
    user_message = message.text
    # Виклик OpenAI API для отримання відповіді на запитання
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=user_message,
        max_tokens=1500
    )
    reply = response.choices[0].text.strip()
    # Відправлення відповіді користувачу
    bot.send_message(message.chat.id, reply)
# Функція для обробки команди "/start"
@bot.message_handler(commands=['start'])
def message_handler_start(message):
    # Відправлення привітального повідомлення користувачу з використанням функції format()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Випадкове число 🎲')
    item2 = types.KeyboardButton('Розклад пар')
    item3 = types.KeyboardButton('Контакти викладачів')
    item4 = types.KeyboardButton('Аудиторії')
    item5 = types.KeyboardButton('Інформація про розробників')
    markup.add(item1, item2,item3, item4, item5)
    bot.send_message(message.chat.id, "Привіт\n{0.first_name}!\nЯ бот, який може відповідати на твої запитання. Що б ти хотів(-ла) знати?\nХочеш зі мною поспілкуватися напиши мені @fiz_matbot.".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Випадкове число 🎲':
            bot.send_message(message.chat.id, 'Ваше число:' + str(random.randint(0,1000)))

        elif message.text == 'Розклад пар':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            Monday = types.KeyboardButton('Понеділок')
            Tuesday = types.KeyboardButton('Вівторок')
            Wednesday = types.KeyboardButton('Середа')
            Thursday = types.KeyboardButton('Четвер')
            Friday = types.KeyboardButton('П\'ятниця')
            back = types.KeyboardButton('🔙Назад')

            markup.add(Monday, Tuesday, Wednesday, Thursday, Friday, back)

            bot.send_message(message.chat.id, 'Розклад пар:\nОберіть нище день який вам треба👇', reply_markup = markup)
        elif message.text == '🔙Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Випадкове число 🎲')
            item2 = types.KeyboardButton('Розклад пар')
            item3 = types.KeyboardButton('Контакти викладачів')
            item4 = types.KeyboardButton('Аудиторії')
            item5 = types.KeyboardButton('Інформація про розробників')
            markup.add(item1, item2, item3, item4, item5)
            bot.send_message(message.chat.id,"Привіт\n{0.first_name}!\nЯ бот, який може відповідати на твої запитання. Що б ти хотів(-ла) знати?\nХочеш зі мною поспілкуватися напиши мені @fiz_matbot.".format(message.from_user), reply_markup=markup)
# Обробка команди /support
@bot.message_handler(commands=['support'])
def _support_(message):
    # Відправка автоматичного повідомлення користувачу
    bot.send_message(message.chat.id, 'Детальніше опишіть проблему і з вами зв\'яжеться служба підтримки.')
    bot.send_message(628446966, f'Користувач звернувся за допомогою:\nАйді: {message.chat.id}\nНік: {message.chat.username}\nТекст: {message.text}')

@bot.message_handler(commands=['yura'])
def _yura(message):
    # Відправлення повідомлення
    send_text_reply(message.chat.id, "Найсексуальніший чоловік на цій планеті")

# Обробник подій від бота Telegram


bot.polling(none_stop=True)
