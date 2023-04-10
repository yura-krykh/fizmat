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

# Функція для взаємодії з OpenAI API та отримання відповіді на запитання
def get_openai_reply(question):
    openai.api_key = OPENAI_API_KEY

    # Виклик OpenAI API для отримання відповіді на запитання
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        max_tokens=1500
    )
    reply = response.choices[0].text.strip()
    return reply
# Функція для обробки команди "/start"
@bot.message_handler(commands=['start'])
def message_handler_start(message):
    # Відправлення привітального повідомлення користувачу з використанням функції format()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Випадкове число 🎲')
    item2 = types.KeyboardButton('Розклад пар')
    item3 = types.KeyboardButton('Контакти викладачів')
    item4 = types.KeyboardButton('Випадкове число2 🎲')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Привіт\n{0.first_name}!\nЯ бот, який може відповідати на твої запитання. Що б ти хотів(-ла) знати?\nХочеш зі мною поспілкуватися напиши мені @fiz_matbot.".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Випадкове число 🎲':
            bot.send.message(message.chat.id, 'Ваше число:' + str(random.randint(0,1000)))
    elif message.text == 'Випадкове число2 🎲':


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
@bot.message_handler(commands=['stepan'])
def _stepan(message):
    # Відправлення повідомлення
    send_text_reply(message.chat.id, "@mamyn_synok")
@bot.message_handler(commands=['shyrik'])
def _shyrik(message):
    # Відправлення повідомлення
    send_text_reply(message.chat.id, "Мельник Олександр Сергійович(ми всі тебе любимо і поважаємо❤️)")
@bot.message_handler(commands=['panda'])
def panda(message):
    # Відправлення повідомлення
    send_text_reply(message.chat.id, "Громяк Мирон Іванович\nКандидат фізико-математичних наук, доцент,\nдекан фізико-математичного факультету\nНародився 10 вересня 1960 року в селі Геленки Козівського району Тернопільської області.\nКоло наукових інтересів: математичний аналіз.\nВикладає дисципліни: математичний аналіз.")
@bot.message_handler(commands=['all'])
def all(message):
    # Відправлення повідомлення
    send_text_reply(message.chat.id, "@yura_krykh , @bodian001 , @KolyaTymchak , @mamyn_synok , @darkness_undead_ronin")


@bot.message_handler(commands=['help'])
def help(message):
    # Відправлення повідомлення
    send_text_reply(message.chat.id, "Поки що, доступні лише такі команди для виклику учасників\n/ivan\n/bodia\n/stepan\n/kolya\n/yura\n/help\nВ скорому часі будуть ще додані цікаві функції.\nЗалишайтеся з нами🥺❤️")




# Обробник подій від бота Telegram


bot.polling(none_stop=True)
