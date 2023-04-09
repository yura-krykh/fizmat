import telebot
import openai



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
def handle_start_command(message):
    # Відправлення привітального повідомлення користувачу
    send_text_reply(message.chat.id, "Привіт! Я бот, який може відповідати на твої запитання. Що б ти хотів(-ла) знати?\nХочеш зі мною поспілкуватися напиши мені @fiz_matbot.")



@bot.message_handler(commands=['yura'])
def handle_yura(message):
    # Відправлення повідомлення
    send_text_reply(message.chat.id, "Найсексуальніший чоловік на цій планеті")
@bot.message_handler(commands=['stepan'])
def handle_yura(message):
    # Відправлення повідомлення
    send_text_reply(message.chat.id, "@mamyn_synok")
@bot.message_handler(commands=['shyrik'])
def handle_yura(message):
    # Відправлення повідомлення
    send_text_reply(message.chat.id, "Мельник Олександр Сергійович(ми всі тебе любимо і поважаємо❤️)")
@bot.message_handler(commands=['panda'])
def handle_yura(message):
    # Відправлення повідомлення
    send_text_reply(message.chat.id, "Громяк Мирон Іванович\nКандидат фізико-математичних наук, доцент,\nдекан фізико-математичного факультету\nНародився 10 вересня 1960 року в селі Геленки Козівського району Тернопільської області.\nКоло наукових інтересів: математичний аналіз.\nВикладає дисципліни: математичний аналіз.")
@bot.message_handler(commands=['k0sheva'])
def handle_yura(message):
    # Відправлення повідомлення
    send_text_reply(message.chat.id, "Кóшева")


@bot.message_handler(commands=['help'])
def handle_yura(message):
    # Відправлення повідомлення
    send_text_reply(message.chat.id, "Поки що, доступні лише такі команди для виклику учасників\n/ivan\n/bodia\n/stepan\n/kolya\n/yura\n/help\nВ скорому часі будуть ще додані цікаві функції.\nЗалишайтеся з нами🥺❤️")




# Обробка команди /support
@bot.message_handler(commands=['support'])
def handle_support_command(message):
    # Відправка автоматичного повідомлення користувачу
    bot.send_message(message.chat.id, 'Детальніше опишіть проблему і з вами зв\'яжеться служба підтримки.')
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    # Відправка повідомлення власнику бота
    bot.send_message(628446966, f'Користувач звернувся за допомогою:\nАйді: {message.chat.id}\nНік: {message.chat.username}\nТекст: {message.text}')




@bot.message_handler(func=lambda message: 'ivan' in message.text.lower())
def handle_ban(message):
    # Відправлення повідомлення "без бану"
    send_text_reply(message.chat.id, "Іван не гей")


# Обробник подій від бота Telegram
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Отримання текстового повідомлення від користувача
    user_message = message.text

    if user_message == '/start':
        # Обробка команди "/start"
        handle_start_command(message)
    else:
        # Взаємодія з OpenAI API для отримання відповіді на запитання
        reply = get_openai_reply(user_message)

        # Відправлення відповіді користувачу
        send_text_reply(message.chat.id, reply)

# Запуск бота

bot.polling(none_stop=True)


