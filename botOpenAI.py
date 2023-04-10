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
        if message.text == 'Інформація про розробників':
            bot.send_message(message.chat.id, 'Засновник @yura_krykh\nГоловний кодер також він')
        elif message.text == 'Розклад пар':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            COIM_23 = types.KeyboardButton('COIM-23')
            COFA_25 = types.KeyboardButton('СОФА-25')
            back = types.KeyboardButton('🔙Назад')
            markup.add(COIM_23, COFA_25, back)
            bot.send_message(message.chat.id, 'Виберіть вашу групу:', reply_markup = markup)
        elif message.text in ['COIM-23', 'СОФА-25']:
            group = message.text  # Оновлюємо значення змінної group на основі вибраної групи
            if group == 'COIM-23':
                schedule = "Понеділок:\n8:00-9:20 1. Аналіз алгоритмів\n9:35-10:55 2. Аналіз алгоритмів\n11:10-12:30 3. Іноземна мова\n12:45-14:05 4. Фізичне виховання\n\nВівторок:\n8:00-9:20 1. -\n9:35-10:55 2. Дискретна математика\n11:10-12:30 3. Дискретна математика\n12:45-14:05 4. Основи теорії графів\n\nСереда:\n8:00-9:20 1. Комп'ютерні мережі\n9:35-10:55 2. Комп'ютерні мережі\n11:10-12:30 3. Комп'ютерна графіка\n12:45-14:05 4. Комп'ютерна графіка\n\nЧетвер:\n8:00-9:20 1. Комп'ютерна математика\n9:35-10:55 2. Комп'ютерна математика\n11:10-12:30 3. Програмування\n12:45-14:05 4. Програмування\n\nП'ятниця:\n8:00-9:20 1. Диференціальні рівняння\n9:35-10:55 2. Диференціальні рівняння\n11:10-12:30 3. Етика і естетика\n12:45-14:05 4. Етика і естетика"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'СОФА-25':
                schedule = "Понеділок:\n8:00-9:20 1. Елементарна фізика \n9:35-10:55 2. Елементарна фізика\n11:10-12:30 3. Фізичне виховання \n12:45-14:05 4. -\nВівторок:\n8:00-9:20 1. Практичний курс англійської мови\n9:35-10:55 2. Практичний курс англійської мови\n11:10-12:30 3. -\n12:45-14:05 4. -\nСереда:\n8:00-9:20 1.  Практична граматика і практична фонетика)\n9:35-10:55 2. Практична граматика і практична фонетика\n11:10-12:30 3. Загальна фізика\n12:45-14:05 4. -\nЧетвер:\n8:00-9:20 1.  Загальна фізика\n9:35-10:55 2.  ПРФЗ\n11:10-12:30 3.  Цифрові технології в освітньому процесі\n12:45-14:05 4.  Цифрові технології в освітньому процесі \nП’ятниця:\n8:00-9:20 1.  Методика навчання англійської мови\n9:35-10:55 2.  Методика навчання англійської мови\n11:10-12:30 3.  Основи права\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)

        elif message.text == '🔙Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Випадкове число 🎲')
            item2 = types.KeyboardButton('Розклад пар')
            item3 = types.KeyboardButton('Контакти викладачів')
            item4 = types.KeyboardButton('Аудиторії')
            item5 = types.KeyboardButton('Інформація про розробників')
            markup.add(item1, item2, item3, item4, item5)
            bot.send_message(message.chat.id,"👇".format(message.from_user), reply_markup=markup)
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
