import telebot
import sqlite3
from telebot import types
from telegram import ParseMode
import datetime
import urllib.request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os
import openai
from telebot import TeleBot
import urllib.request
import time
import json
CHAT_ID = 628446966
TELEGRAM_API_KEY = '5428270852:AAEbBDt8RiYgiizDEC7o5oTz4vl-x7Ls5ng'
OPENAI_API_KEY = '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'
bot = telebot.TeleBot(TELEGRAM_API_KEY)







def get_user_data(user_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT grypa, email, first_last FROM login_id WHERE id = {user_id}")
    data = cursor.fetchone()
    connect.close()
    return data


# ЗБЕРЕЖЕННЯ ФОТО З ДЗ У БАЗУ ДАННИХ

@bot.message_handler(commands=['start'])
def start(message: types.Message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT NOT NULL,
            grypa TEXT NOT NULL,
            first_last TEXT NOT NULL,
            roli TEXT )""")

    connect.commit()
    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id} ")
    data = cursor.fetchone()
    if data is None:

        # Запит email
        bot.send_message(message.chat.id, "Будь ласка, введіть свою email адресу:")
        bot.register_next_step_handler(message, get_email)

    else:
        bot.send_message(message.chat.id, "Ти вже зареєстрований!")
        message_handler_start(message)

def get_email(message: types.Message):
    email = message.text
    email = email.lower()
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("SELECT email FROM login_id")
    rows = cursor.fetchall()
    emails = [row[0] for row in rows]  # Створення списку зі значень email

    if email in emails:
        bot.send_message(message.chat.id, "Користувач за такою електронною адресою вже зареєстрований введіть будь ласка свою адресу")
        bot.register_next_step_handler(message, get_email)

    elif email.startswith('/'):
        bot.send_message(message.chat.id, "Ви ввели команду а не пошту будь ласка введіть свою фізматівську пошту: ")
        bot.register_next_step_handler(message, get_email)

    else:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Email_Base WHERE Email_Address=?", (email,))
        row = cursor.fetchone()
        if row:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_student = types.KeyboardButton("Студент")
            button_starosta = types.KeyboardButton("Староста")
            button_vikladach = types.KeyboardButton("Викладач")
            keyboard.add(button_student, button_starosta, button_vikladach)
            bot.send_message(message.chat.id, "Виберіть вашу роль:", reply_markup=keyboard)
            bot.register_next_step_handler(message, get_role, email)


        else:
            # Email does not exist, send error message
            bot.send_message(message.chat.id,"Вашої пошти не знайдено в базі даних фізмату. Будь ласка, введіть свою пошту ще раз правильно.")
            # Return to the get_email function to wait for the next input from the user
            bot.register_next_step_handler(message, get_email)
        cursor.close()
        conn.close()



def get_role(message, email):
    role = message.text

    if role.startswith('/'):
        bot.send_message(message.chat.id,"Ви ввели команду, а не роль")
        bot.register_next_step_handler(message, get_role, email)

    elif role == 'Студент':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('СОФІ-11')
        item2 = types.KeyboardButton('СОФА-12')
        item3 = types.KeyboardButton('СОМІ-13')
        item4 = types.KeyboardButton('КМ-14')
        item5 = types.KeyboardButton('СОІМ-15')
        item6 = types.KeyboardButton('ІІП-16')
        item7 = types.KeyboardButton('DA-17')
        item8 = types.KeyboardButton('СОФІ-21')
        item9 = types.KeyboardButton('СОМІ-22')
        item10 = types.KeyboardButton('СОІМ-23')
        item11 = types.KeyboardButton('СОФА-25')
        item12 = types.KeyboardButton('КН-26')
        item13 = types.KeyboardButton('КН-27')
        item14 = types.KeyboardButton('СОФІ-31')
        item15 = types.KeyboardButton('СОМІ-32')
        item16 = types.KeyboardButton('СОІМ-33')
        item17 = types.KeyboardButton('СОФА-35')
        item18 = types.KeyboardButton('КН-36')
        item19 = types.KeyboardButton('СОФІ-41')
        item20 = types.KeyboardButton('СОМІ-42')
        item21 = types.KeyboardButton('СОIM-43')
        item22 = types.KeyboardButton('СОІнск-24')
        item23 = types.KeyboardButton('мСОФ-11')
        item24 = types.KeyboardButton('мСОМ-12')
        item25 = types.KeyboardButton('мСОІн-13')
        item26 = types.KeyboardButton('мСОФ-21')
        item27 = types.KeyboardButton('мСОМ-22')
        item28 = types.KeyboardButton('мСОІн-23')
        keyboard.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12, item13,
                     item14, item15, item16, item17, item18, item19, item20, item21, item22, item23, item24,
                     item25, item26, item27, item28)
        bot.send_message(message.chat.id,
                         "Будь ласка, будьте уважні при виборі своєї групи. Оберіть дійсну групу, оскільки редагування групи не буде можливим. Якщо помилилися з вибором групи напишіть в /support",
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, get_group_stud, email,role)





    elif role == 'Викладач':
        # Запит паролю для ролі викладача
        bot.send_message(message.chat.id, "Будь ласка, введіть пароль для викладача:")
        bot.register_next_step_handler(message, get_password,  role, email)

    elif role == 'Староста':
        # Запит паролю для ролі старости
        bot.send_message(message.chat.id, "Будь ласка, введіть пароль для старости:")
        bot.register_next_step_handler(message, get_password, role, email )

    else:
        # Надсилання повідомлення про неправильний вибір ролі
        bot.send_message(message.chat.id, "Виберіть роль з наданих кнопок.")
        bot.register_next_step_handler(message, get_role, email)


def get_password(message, role, email):
    password = message.text

    if role == 'Викладач' and password == '000':
        board = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Математика📏')
        item2 = types.KeyboardButton('Інформатика🧑‍💻')
        item3 = types.KeyboardButton('Фізика👨‍🔬')
        board.add(item1, item2, item3)
        bot.send_message(message.chat.id, "Виберіть із якої ви кафедри:", reply_markup=board)
        bot.register_next_step_handler(message, kafedra, email, role)

    elif role == 'Староста' and password == '111':
        # Встановлення ролі старости в базі даних


        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('СОФІ-11')
        item2 = types.KeyboardButton('СОФА-12')
        item3 = types.KeyboardButton('СОМІ-13')
        item4 = types.KeyboardButton('КМ-14')
        item5 = types.KeyboardButton('СОІМ-15')
        item6 = types.KeyboardButton('ІІП-16')
        item7 = types.KeyboardButton('DA-17')
        item8 = types.KeyboardButton('СОФІ-21')
        item9 = types.KeyboardButton('СОМІ-22')
        item10 = types.KeyboardButton('СОІМ-23')
        item11 = types.KeyboardButton('СОФА-25')
        item12 = types.KeyboardButton('КН-26')
        item13 = types.KeyboardButton('КН-27')
        item14 = types.KeyboardButton('СОФІ-31')
        item15 = types.KeyboardButton('СОМІ-32')
        item16 = types.KeyboardButton('СОІМ-33')
        item17 = types.KeyboardButton('СОФА-35')
        item18 = types.KeyboardButton('КН-36')
        item19 = types.KeyboardButton('СОФІ-41')
        item20 = types.KeyboardButton('СОМІ-42')
        item21 = types.KeyboardButton('СОIM-43')
        item22 = types.KeyboardButton('СОІнск-24')
        item23 = types.KeyboardButton('мСОФ-11')
        item24 = types.KeyboardButton('мСОМ-12')
        item25 = types.KeyboardButton('мСОІн-13')
        item26 = types.KeyboardButton('мСОФ-21')
        item27 = types.KeyboardButton('мСОМ-22')
        item28 = types.KeyboardButton('мСОІн-23')
        keyboard.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12, item13,
                     item14, item15, item16, item17, item18, item19, item20, item21, item22, item23, item24,
                     item25, item26, item27, item28)
        bot.send_message(message.chat.id,
                         "Будь ласка, будьте уважні при виборі своєї групи. Оберіть дійсну групу, оскільки редагування групи не буде можливим. Якщо помилилися з вибором групи напишіть в /support",
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, get_group_stud, email, role)




    else:
        # Надсилання повідомлення про неправильний пароль
        bot.send_message(message.chat.id, "Неправильний пароль. Спробуйте ще раз.")
        bot.register_next_step_handler(message, get_password, role, email)

def kafedra(message, email, role):
    group = message.text
    if group not in ['Математика📏', 'Інформатика🧑‍💻', 'Фізика👨‍🔬']:
        bot.send_message(message.chat.id, "Ви що з хімбіо?🤨")
        bot.register_next_step_handler(message, kafedra, message, email, role)

    elif group.startswith('/'):
        bot.send_message(message.chat.id, "Будь ласка будьте уважніші ви ввели команду, а не назву кафедри, будь ласка введіть свою кафедру😡 ")
        bot.register_next_step_handler(message, kafedra, email, role)
    else:
        bot.send_message(message.chat.id, 'Будь ласка надішліть своє повне прізвище ім\'я по-батькові')
        if group == 'Математика📏':
            group = "Математик"
        elif group == 'Інформатика🧑‍💻':
            group = 'Інформатик'
        elif group == 'Фізика👨‍🔬':
            group = 'Фізик'
        bot.register_next_step_handler(message, get_first_last, email, role, group)

def get_group_stud(message,email,role):
    group = message.text
    if group not in ['СОМІ-32', 'СОІМ-33', 'СОФА-35', 'КН-36', 'мСОФ-11', 'мСОМ-12', 'СОФІ-41', 'СОМІ-42', 'СОIM-43',
                     'СОІнск-24', 'мСОІн-13', 'КМ-14', 'СОІМ-15', 'ІІП-16', 'DA-17', 'СОФІ-21', 'СОФІ-21', 'СОМІ-22',
                     'КН-26',
                     'КН-27', 'СОФІ-31', 'СОІМ-23', 'СОФА-25', 'СОФІ-11', 'СОФА-12', 'СОМІ-13', 'мСОФ-21', 'мСОМ-22',
                     'мСОІн-23']:
        bot.send_message(message.chat.id, "Ви ввели не правильну групу виберіть ще раз свою групу:")
        bot.register_next_step_handler(message, get_group_stud, email, role)
    elif group.startswith('/'):
        bot.send_message(message.chat.id, "Будь ласка будьте уважніші ви ввели команду а не назву групи, будь ласка введіть свою групу😡 ")
        bot.register_next_step_handler(message, get_group_stud, email,role)
    else:
        group = message.text.upper().replace('-', '_')
        bot.send_message(message.chat.id, "Будь ласка, введіть своє ПІБ:")
        bot.register_next_step_handler(message, get_first_last, email, role, group)


def get_first_last(message, email, role, group):
    first_last = message.text
    role = role.lower()
    email = email.lower()

    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    user_id = message.chat.id
    user_name = message.chat.username

    # Вставка даних в базу даних
    cursor.execute("INSERT INTO login_id (id, username, email, grypa, first_last, roli) VALUES(?, ?, ?, ?, ?, ?);",
                   (user_id, user_name, email, group, first_last, role))
    connect.commit()
    bot.send_message(message.chat.id, "Успішна реєстрація")
    create_rozklad_table(message)

def create_rozklad_table(message):
    # Встановлення з'єднання з базою даних
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    # Отримання унікальних груп з бази даних
    groups = ['СОМІ-32', 'СОІМ-33', 'СОФА-35', 'КН-36', 'мСОФ-11', 'мСОМ-12', 'СОФІ-41', 'СОМІ-42', 'СОIM-43',
              'СОІнск-24', 'мСОІн-13', 'КМ-14', 'СОІМ-15', 'ІІП-16', 'DA-17', 'СОФІ-21', 'СОФІ-21', 'СОМІ-22',
              'КН-26', 'КН-27', 'СОФІ-31', 'СОІМ-23', 'СОФА-25', 'СОФІ-11', 'СОФА-12', 'СОМІ-13', 'мСОФ-21', 'мСОМ-22',
              'мСОІн-23']

    # Створення таблиць для кожної групи
    for group in groups:
        table_name = f"rosklad_{group.replace('-', '_')}"
        # Перевірка наявності таблиці
        cursor.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        result = cursor.fetchone()
        if result[0] == 0:
            # Створення таблиці, якщо вона не існує
            cursor.execute(
                f"CREATE TABLE {table_name} (Перша TEXT, друга TEXT, третя TEXT, четверта TEXT, пята TEXT)")
            # Додавання значення "пара ще не вказана" у всі стовпці таблиці
            cursor.execute(
                f"INSERT INTO {table_name} (Перша, друга, третя, четверта, пята) VALUES ('пара ще не вказана', 'пара ще не вказана', 'пара ще не вказана', 'пара ще не вказана', 'пара ще не вказана')")
            cursor.execute(
                f"INSERT INTO {table_name} (Перша, друга, третя, четверта, пята) VALUES ('пара ще не вказана', 'пара ще не вказана', 'пара ще не вказана', 'пара ще не вказана', 'пара ще не вказана')")
            cursor.execute(
                f"INSERT INTO {table_name} (Перша, друга, третя, четверта, пята) VALUES ('пара ще не вказана', 'пара ще не вказана', 'пара ще не вказана', 'пара ще не вказана', 'пара ще не вказана')")
            cursor.execute(
                f"INSERT INTO {table_name} (Перша, друга, третя, четверта, пята) VALUES ('пара ще не вказана', 'пара ще не вказана', 'пара ще не вказана', 'пара ще не вказана', 'пара ще не вказана')")

    connect.commit()  # Застосовуємо зміни до бази даних
    cursor.close()
    connect.close()
    message_handler_start(message)






###############################################################################################################################################################################





@bot.message_handler(commands=['shurik'])
def shurik(message):
    bot.send_message(message.chat.id, "Помідор ваше пєрсік, мамою твоєю клянусь".format(message.from_user))


@bot.message_handler(commands=['legion'])
def legion(message):
    bot.send_message(message.chat.id, "пшш пшш пшш Олег пукнув\nце Олег @phantomkahueta ".format(message.from_user))

#####################################################################################################################




######################################################################################################################


@bot.message_handler(commands=['homework'])
def check_starost(message):
    user_id = message.from_user.id
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT roli FROM login_id WHERE id = {user_id}")
    user_rol = cursor.fetchone()
    if user_rol:
        user_rol = user_rol[0]
        if user_rol == 'староста':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item7 = types.KeyboardButton('🔙 Назад')
            keyboard.add(item7)
            bot.send_message(message.chat.id, "Надішліть мені предмет з якого вам задали дошнє завдання: ", reply_markup=keyboard)
            bot.register_next_step_handler(message, homework_subject)
        else:
            bot.send_message(message.chat.id, "Ви не є старостою, ви не можете надсилати домашнє завдання")
            message_handler_start(message)
    else:
        bot.send_message(message.chat.id, "Користувача не знайдено в базі даних")
        message_handler_start(message)
def homework_subject(message: types.Message):
    subject = message.text
    if message.text == '🔙 Назад':
        # Виклик команди "/start" при натисканні кнопки "🔙 Назад"
        bot.send_message(message.chat.id, 'Повертаюся в головне меню...')
        message_handler_start(message)
    else:
        bot.send_message(message.chat.id,'Будь ласка, коротко опишіть, які завдання вам задані у цьому предметі:')
        bot.register_next_step_handler(message, save_homework, subject)
def save_homework(message: types.Message, subject):
    text_work = message.text
    user_id = message.from_user.id
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT grypa FROM login_id WHERE id = {user_id}")
    user_grypa = cursor.fetchone()[0]
    # вставляємо новий запис до таблиці з назвою, що міститься у змінній user_grypa
    insert_query = f"INSERT INTO {user_grypa} (subject, text) VALUES (?, ?)"
    cursor.execute(insert_query, (subject, text_work))
    conn.commit()
    bot.send_message(message.chat.id, "✅ Домашнє завдання збережено та розіслано вашим одногрупникам!")
    save_studend_text(message, subject, text_work)
def save_studend_text(message, subject, text_work):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    chat_id = message.chat.id
    cursor.execute(f"SELECT grypa FROM login_id WHERE id = {chat_id}")
    user_group = cursor.fetchone()[0]
    cursor.execute(f"SELECT id FROM login_id WHERE grypa = '{user_group}'")
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0]
        insert_query =  f"INSERT INTO table_{user_id} (subject, text) VALUES (?, ?)"
        cursor.execute(insert_query, (subject, text_work))
    conn.commit()
    conn.close()




########################################################################################################################






@bot.message_handler(commands=['delete'])
def delete(message):
    # запитуємо у користувача айді отримувача повідомлення
    chat_id = message.chat.id
    if chat_id != CHAT_ID:
        bot.send_message(chat_id=chat_id, text='Ви не маєте доступу до цієї команди.')
        return
    else:
        bot.send_message(message.chat.id, "Введіть айді користувача: ")
        bot.register_next_step_handler(message, handle_user_id)
def handle_user_id(message):
    # Отримуємо введене айді користувача
    user_id = message.text

    # Викликаємо функцію для видалення користувача з бази даних
    delete_user(user_id)

    # Відправляємо підтвердження видалення користувача
    bot.send_message(message.chat.id, f"Користувач з айді {user_id} видалений.")

def delete_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Видаляємо користувача з бази даних
    cursor.execute("DELETE FROM login_id WHERE id=?", (user_id,))
    conn.commit()
##############################################

    ##########################################################################################################################

@bot.message_handler(commands=['support'])
def message_handler_support(message):
    # Відправлення повідомлення від бота з кнопкою "🔙Назад"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_back = types.KeyboardButton('🔙Назад')
    markup.add(item_back)
    bot.send_message(chat_id=message.chat.id,
                     text='<b>Доброго дня, будь ласка опишіть детально з якими труднощами ви зіткнулися?</b>',
                     parse_mode=ParseMode.HTML, reply_markup=markup)
    # Реєстрація наступного кроку з обробником повідомлення користувача
    bot.register_next_step_handler(message, support_reply_handler)


def support_reply_handler(message):
    if message.text == '🔙Назад':
        # Виклик команди "/start" при натисканні кнопки "🔙Назад"
        message_handler_start(message)
    else:
        # Відправка повідомлення користувачем до підтримки
        bot.send_message(chat_id=628446966,
                         text=f'Користувач звернувся за допомогою:\nАйді: {message.chat.id}\nНік: @{message.chat.username}\nТекст: {message.text}')
        bot.send_message(chat_id=message.chat.id,
                         text='Дякуємо за ваше повідомлення! Наша команда підтримки зв\'яжеться з вами найближчим часом.')

#################################################################################################
@bot.message_handler(commands=['idea'])
def message_handler_idea(message):
    # Відправлення повідомлення від бота з кнопкою "🔙Назад"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_back = types.KeyboardButton('🔙Назад')
    markup.add(item_back)
    bot.send_message(chat_id=message.chat.id,
                     text='<b>Яка у вас є ідея для мене? Напишіть її, і ми розглянемо її реалізацію в майбутньому.</b>',
                     parse_mode=ParseMode.HTML, reply_markup=markup)
    # Реєстрація наступного кроку з обробником повідомлення користувача
    bot.register_next_step_handler(message, idea_reply_handler)


def idea_reply_handler(message):
    if message.text == '🔙Назад':
        # Виклик команди "/start" при натисканні кнопки "🔙Назад"
        message_handler_start(message)
    else:
        # Відправка ідеї користувачем
        bot.send_message(chat_id=628446966,
                         text=f'Користувач запропонував ідею для бота:\nАйді: {message.chat.id}\nНік: @{message.chat.username}\nТекст: {message.text}')
        bot.send_message(chat_id=message.chat.id,
                         text='Дякуємо за вашу ідею! Ми розглянемо її в майбутньому.')

#################################################################################################
@bot.message_handler(commands=['userhelp'])
def send_help(message):
    # запитуємо у користувача айді отримувача повідомлення
    uhat_id = message.chat.id
    if uhat_id != CHAT_ID:
        bot.send_message(chat_id=uhat_id, text='Ви не маєте доступу до цієї команди.')
        return
    else:
        bot.send_message(message.chat.id, "Введіть айді користувача: ")
        bot.register_next_step_handler(message, get_recipient_id)


def get_recipient_id(message):
    # зберігаємо айді отримувача повідомлення та запитуємо текст повідомлення
    recipient_id = message.text
    bot.send_message(message.chat.id, "Введіть текст повідомлення:")
    bot.register_next_step_handler(message, send_message, recipient_id)


def send_message(message, recipient_id):
    # відправляємо повідомлення з введеним текстом до користувача з введеним айді
    try:
        bot.send_message(recipient_id, message.text)
        bot.send_message(message.chat.id, "Повідомлення надіслано!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка: {str(e)}")


#############################################################################################

@bot.message_handler(content_types=['voice', 'video_note'])
def handle_message(message):
    channel_id = '-1001955388901'
    if message.voice:
        # Отримано голосове повідомлення
        bot.forward_message(chat_id=channel_id, from_chat_id=message.chat.id, message_id=message.message_id)
    elif message.video_note:
        # Отримано кружечок повідомлення
        bot.forward_message(chat_id=channel_id, from_chat_id=message.chat.id, message_id=message.message_id)



@bot.message_handler(commands=['news'])
def send_news(message):
    # Запит повідомлення, яке потрібно розіслати
    bot.send_message(chat_id=message.chat.id, text='Введіть повідомлення для розсилки:')
    bot.register_next_step_handler(message, news_handler)
def news_handler(message):
    # Отримання повідомлення від користувача та розсилка його всім користувачам бота
    news = message.text
    users = get_all_users()  # Отримання всіх користувачів бота
    blocked_users = []
    for user in users:
        try:
            bot.send_message(chat_id=user, text=news)
        except telebot.apihelper.ApiTelegramException as e:
            if e.result.status_code == 403:
                blocked_users.append(user)
    # Перевірка, чи є заблоковані користувачі
    if blocked_users:
        # Формування повідомлення про заблокованих користувачів
        blocked_users_text = '\n'.join([str(user) for user in blocked_users])
        error_message = f"Користувачі {blocked_users_text} заблокували бота."
        # Надсилання повідомлення про заблокованих користувачів адміністратору бота
        bot.send_message(chat_id=CHAT_ID, text=error_message)
def get_all_users():
    # Підключення до бази даних
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Отримання списку всіх користувачів з таблиці login_id
    cursor.execute("SELECT id FROM login_id")
    users = cursor.fetchall()
    # Закриття підключення до бази даних
    cursor.close()
    conn.close()
    # Повернення списку всіх користувачів
    return [user[0] for user in users]


def menu_starostam(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Редагувати розклад')
    item2 = types.KeyboardButton('Робота з журналом')
    homework = types.KeyboardButton('Додати домашку')
    item4 = types.KeyboardButton('Оголошення для групи')
    back = types.KeyboardButton('🔙Назад')

    markup.add(back)
    markup.add(item1)
    markup.add(item2)
    markup.add(homework)
    markup.add(item4)
    bot.send_message(message.chat.id, "Це меню призначене спеціально для старост, і ви можете ознайомитися зі списком майбутніх функцій, які будуть додані😌".format(message.from_user), reply_markup=markup)




@bot.message_handler(commands=['menu'])
def message_handler_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('📜Профіль')
    item2 = types.KeyboardButton('✍️Розклад пар')
    item3 = types.KeyboardButton('Контакти викладачів')
    item4 = types.KeyboardButton('Старостам')
    item5 = types.KeyboardButton('Домашка')
    item_menu = types.KeyboardButton('Інформація про розробників')
    item5_6 = types.KeyboardButton('Підтримка проекту')
    markup.add(item1, item2, item3, item4, item5)
    markup.add(item_menu)
    markup.add(item5_6)
    bot.send_message(message.chat.id, "👇".format(message.from_user), reply_markup=markup)



@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':

        if message.text == 'Інформація про розробників':
            bot.send_message(message.chat.id, 'Засновник @yura_krykh\nВведіть команду /support якшо виникли проблеми')

        elif message.text == 'Підтримка проекту':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            info = types.KeyboardButton('Інформація про підтримку')
            info2 = types.KeyboardButton('Донатик')
            back = types.KeyboardButton('🔙Назад')
            markup.add(info)
            markup.add(info2)
            markup.add(back)
            bot.send_message(message.chat.id, "Будемо раді, якщо ви підтримаєте проект🥹", reply_markup=markup)

        elif message.text == 'Інформація про підтримку':
            bot.send_message(message.chat.id, "Привіт, ми збираємо суму для оренди сервера, на якому буде встановлений наш бот, памʼятайте донат не є обов'язковим, але це сильно допоможе полегшити завдання розробникам та підтримати нашу працю, дякуємо всім, ну і звісно нагадуємо що маленьких донатів не буває)")

        elif message.text == 'Донатик':
            bot.send_message(message.chat.id, "Посилання на банку\nhttps://send.monobank.ua/jar/9qjTL2dtrB\nНомер картки банки\n5375 4112 0659 5113")

        elif message.text == 'Додати домашку':
            user_id = message.from_user.id
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT roli FROM login_id WHERE id = {user_id}")
            user_rol = cursor.fetchone()
            if user_rol:
                user_rol = user_rol[0]
                if user_rol == 'староста':
                    homework(message)
                else:
                    bot.send_message(message.chat.id, "Ви не є старостою, ви не можете користуватися цим меню)")
                    message_handler_start(message)
            else:
                bot.send_message(message.chat.id, "Користувача не знайдено в базі даних")
                message_handler_start(message)


        elif message.text == 'Старостам':
            user_id = message.from_user.id
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT roli FROM login_id WHERE id = {user_id}")
            user_rol = cursor.fetchone()
            if user_rol:
                user_rol = user_rol[0]
                if user_rol == 'староста':
                    menu_starostam(message)
                else:
                    bot.send_message(message.chat.id, "Ви не є старостою, ви не можете користуватися цим меню)")
                    message_handler_start(message)
            else:
                bot.send_message(message.chat.id, "Користувача не знайдено в базі даних")
                message_handler_start(message)

        elif message.text == 'я староста' or message.text == "Я староста":
            bot.send_message(message.chat.id, "Ти піздюк, а не староста😏")

        elif message.text == 'Редагувати розклад':
            user_id = message.from_user.id
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT roli FROM login_id WHERE id = {user_id}")
            user_rol = cursor.fetchone()
            if user_rol:
                user_rol = user_rol[0]
                if user_rol == 'староста':
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton('Понеділок')
                    item2 = types.KeyboardButton('Вівторок')
                    item3 =types.KeyboardButton('Середа')
                    item4 = types.KeyboardButton('Четвер')
                    item5 = types.KeyboardButton('П\'ятниця')
                    back =types.KeyboardButton('🔙Назад')
                    keyboard.add(back)
                    keyboard.add(item1, item2, item3, item4, item5)

                    bot.send_message(message.chat.id,"Оберіть день, у який ви внесете корекцію", reply_markup=keyboard)
                    bot.register_next_step_handler(message, redaguvanna,user_id)
                else:
                    bot.send_message(message.chat.id, "Ви не є старостою, ви не можете користуватися цим меню)")
                    message_handler_start(message)

        elif message.text == 'Домашка':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Перегляд домашки')
            item2 = types.KeyboardButton('Відмітити виконане дз')
            item3 = types.KeyboardButton('🔙Назад')
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            bot.send_message(message.chat.id, 'Виберіть:', reply_markup=markup)

        elif message.text == 'Перегляд домашки':
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM table_{message.chat.id}")
            rows = cursor.fetchall()
            if len(rows) == 0:
                bot.send_message(message.chat.id, "У вас немає домашніх завдань.")
            else:
                for row in rows:
                    subject = row[0]
                    text = row[1]
                    photo = row[2]
                    file = row[3]
                    caption = f"Предмет: {subject}\nПояснення: {text}"
                    bot.send_message(message.chat.id, caption)
            conn.close()

        elif message.text == 'Відмітити виконане дз':
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
          # вибираємо дані з таблиці для поточного користувача
            cursor.execute(f"SELECT * FROM table_{message.chat.id}")
            rows = cursor.fetchall()
            if len(rows) == 0:
                # якщо в таблиці немає даних, виводимо відповідне повідомлення
                bot.send_message(message.chat.id, "У вас немає домашніх завдань.")
            else:
                # створюємо список для кнопок
                keyboard = []
                # проходимось по кожному рядку таблиці та додаємо кнопки з текстом з колонки text
                for row in rows:
                    text = row[0]
                    keyboard.append([KeyboardButton(text)])
            # створюємо розмітку для кнопок та відправляємо повідомлення разом з нею
                    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                    reply_markup = json.dumps(reply_markup.to_dict())
            bot.send_message(message.chat.id, "Оберіть виконане домашнє завдання:", reply_markup=reply_markup)
                # закриваємо з'єднання з базою даних
            conn.close()

        elif message.text == '✍️Розклад пар':
            user_id = message.chat.id
            rozklad_par_0(message, user_id)

        elif message.text == '📜Профіль':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            update_profile = types.KeyboardButton('🔧Редагувати профіль')
            back = types.KeyboardButton('🔙Назад')
            markup.add(update_profile, back)
            user_id = message.chat.id
            user_data = get_user_data(user_id)
            if user_data is not None:
                grypa, email, first_last = user_data
                profile_info = f"📜Профіль\n📚Група: {grypa}\n✉️Email: {email}\n👨‍🎓ПІБ: {first_last}"
                bot.send_message(message.chat.id, profile_info, reply_markup=markup)
            else:
                bot.send_message(message.chat.id, "Вас не знайдено(\nЗвернись до /support!")

        elif message.text == '🔧Редагувати профіль':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            up_email = types.KeyboardButton('🛠📨Email')
            up_grypa = types.KeyboardButton('🛠👥Групу')
            up_firstlast = types.KeyboardButton("🛠🪪ПІБ")
            back = types.KeyboardButton('📜Профіль')
            markup.add(up_email, up_grypa, up_firstlast, back)
            bot.send_message(message.chat.id, "Виберіть, що саме хочете редагувати?🧐", reply_markup=markup)

        elif message.text == '🛠📨Email':

            bot.send_message(message.chat.id, "Введіть фізматівську пошту:")
            bot.register_next_step_handler(message, update_email)

        elif message.text == '🛠👥Групу':
            keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('СОФІ-11')
            item2 = types.KeyboardButton('СОФА-12')
            item3 = types.KeyboardButton('СОМІ-13')
            item4 = types.KeyboardButton('КМ-14')
            item5 = types.KeyboardButton('СОІМ-15')
            item6 = types.KeyboardButton('ІІП-16')
            item7 = types.KeyboardButton('DA-17')
            item8 = types.KeyboardButton('СОФІ-21')
            item9 = types.KeyboardButton('СОМІ-22')
            item10 = types.KeyboardButton('СОІМ-23')
            item11 = types.KeyboardButton('СОФА-25')
            item12 = types.KeyboardButton('КН-26')
            item13 = types.KeyboardButton('КН-27')
            item14 = types.KeyboardButton('СОФІ-31')
            item15 = types.KeyboardButton('СОМІ-32')
            item16 = types.KeyboardButton('СОІМ-33')
            item17 = types.KeyboardButton('СОФА-35')
            item18 = types.KeyboardButton('КН-36')
            item19 = types.KeyboardButton('СОФІ-41')
            item20 = types.KeyboardButton('СОМІ-42')
            item21 = types.KeyboardButton('СОIM-43')
            item22 = types.KeyboardButton('СОІнск-24')
            item23 = types.KeyboardButton('мСОФ-11')
            item24 = types.KeyboardButton('мСОМ-12')
            item25 = types.KeyboardButton('мСОІн-13')
            item26 = types.KeyboardButton('мСОФ-21')
            item27 = types.KeyboardButton('мСОМ-22')
            item28 = types.KeyboardButton('мСОІн-23')
            keyboard2.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12, item13,
                          item14, item15, item16, item17, item18, item19, item20, item21, item22, item23, item24,
                          item25, item26, item27, item28)

            bot.send_message(message.chat.id, "Виберіть нову групу:", reply_markup=keyboard2)
            bot.register_next_step_handler(message, update_grypa)

        elif message.text == "🛠🪪ПІБ":
            bot.send_message(message.chat.id, "Введіть нове ПІБ:")
            bot.register_next_step_handler(message, update_first_last)

        elif message.text == 'Контакти викладачів':
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            cursor.execute("SELECT Викладач FROM Teachers")
            teachers = cursor.fetchall()


            keyboard = []
            for i in range(0, len(teachers), 3):
                row = []
                for j in range(i, min(i + 3, len(teachers))):
                    teacher_name = teachers[j][0]
                    row.append(InlineKeyboardButton(teacher_name, callback_data=teacher_name))
                keyboard.append(row)


            reply_markup = InlineKeyboardMarkup(keyboard)
            reply_markup = json.dumps(reply_markup.to_dict())

            conn.close()
            bot.send_message(message.chat.id, "Оберіть викладача за прізвищем якого шукаєте:",reply_markup=reply_markup)

        elif message.text == "Робота з журналом":
            user_id = message.from_user.id
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT roli FROM login_id WHERE id = {user_id}")
            user_rol = cursor.fetchone()
            if user_rol:
                user_rol = user_rol[0]
                if user_rol == 'староста':
                    jurnal1(message)
                else:
                    bot.send_message(message.chat.id, "Ви не є старостою, ви не можете користуватися цим меню)")
                    message_handler_start(message)
            else:
                bot.send_message(message.chat.id, "Користувача не знайдено в базі даних")
                message_handler_start(message)


        elif message.text == '🔙Назад':
            message_handler_start(message)



def homework(message):
    user_id = message.chat.id
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT grypa FROM login_id WHERE id = {user_id}")
    user_grypa = cursor.fetchone()[0]
    user_grypa = user_grypa.upper().replace('_', '-')

    db_filename = user_grypa + '_DOMASHKA.db'
    if os.path.exists(db_filename):  # 1_1234
        bot.send_message(message.chat.id, f"Оберіть з якого предмету хочете задати дошнє завдання для своєї групи {user_grypa}")


    else:  # 2_1234
        bot.send_message(message.chat.id, f"Таблиці із домашніми завданнями для твоєї групи {user_grypa} ще не створенно, давай я тобі допоможу їх створити🧑‍💻", reply_markup=telebot.types.ReplyKeyboardRemove())
        homework2_1(message,user_grypa)


def homework2_1(message,user_grypa):
    # Створення бази даних з назвою групи
    conn = sqlite3.connect(f"{user_grypa}_DOMASHKA.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Предмети (Предмети TEXT)")
    conn.commit()
    conn.close()

    db_filename = user_grypa + '.db'
    if os.path.exists(db_filename):
        conn1 = sqlite3.connect(f"{user_grypa}.db")
        cursor2 = conn1.cursor()
        cursor2.execute("SELECT Предмети FROM Предмети")
        results = cursor2.fetchall()
        subjects = [row[0] for row in results]
        sub = ", ".join(subjects)
        conn1.close()
        bot.send_message(message.chat.id,f"Ви можете використати ось ці навчальні дисципліни із журналу з оцінками\n\n<code>{sub}</code>\n\nНадішліть через кому)))",parse_mode=ParseMode.HTML)
        bot.register_next_step_handler(message, homework2_2, user_grypa)

    else:
        bot.send_message(message.chat.id, "Будь ласка надішліть мені всі свої навчальні дисципліни за таким зразком\n\n<code>Алгебра, Фізика, Інформатика, Іноземна мова, Фізра, Українська мова</code>\n\nТобто через кому))", parse_mode=ParseMode.HTML)
        bot.register_next_step_handler(message, homework2_2, user_grypa)

def homework2_2(message,user_grypa):
    predmety = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Так все вірно')
    item2 = types.KeyboardButton('Редагувати')
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id, "Перевірте чи ви правильно надіслали усі навчальні дисципліни",reply_markup=markup)
    bot.send_message(message.chat.id, f"<code>{predmety}</code>", parse_mode=ParseMode.HTML)
    bot.register_next_step_handler(message,homework2_3,user_grypa,predmety)
    
def homework2_3(message, user_grypa,predmety):
    vidpovid = message.text

    if vidpovid == 'Так все вірно':

        bot.send_message(message.chat.id, "Зберігаю ваші предмети...", reply_markup=telebot.types.ReplyKeyboardRemove())
        time.sleep(2)
        homework2_4(message,user_grypa,predmety)

    elif vidpovid == 'Редагувати':
        bot.send_message(message.chat.id,"Будь ласка надішліть мені ще раз ваші навчальні дисципліни і переконайтеся чи все вірно)", reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, homework2_2, user_grypa)


def homework2_4(message, user_grypa,predmety):
    subjects = predmety.split(', ')  # Розділяємо рядок за комами

    conn = sqlite3.connect(f"{user_grypa}_DOMASHKA.db")
    cursor = conn.cursor()

    for subject in subjects:
        cursor.execute("INSERT INTO Предмети (Предмети) VALUES (?)", (subject,))

    conn.commit()
    bot.send_message(message.chat.id, "Створюю таблиці з вашими предметами...")
    time.sleep(2)
    homework2_5(message, user_grypa)

def homework2_5(message, user_grypa):
    conn = sqlite3.connect(f"{user_grypa}_DOMASHKA.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Предмети FROM Предмети")
    result = cursor.fetchall()
    result = [(item[0].replace(" ", "_"),) for item in result]
    for row in result:
        pre = row[0]
        cursor.execute(
            f'CREATE TABLE "{pre}" ("id" TEXT, username TEXT)'
        )
        cursor.execute(
            f'CREATE TABLE "{pre}_dz" ("Завдання" TEXT, ФОТО_1 BLOB, ФОТО_2 BLOB, ФОТО_3 BLOB, ФАЙЛ_1 BLOB, ФАЙЛ_2 BLOB, ФАЙЛ_3 BLOB, КОЛИ_ЗАДАНО TEXT, ДОКИ_АКТУАЛЬНА TEXT, ДАТА_ВИДАЛЕННЯ TEXT)'
        )
    bot.send_message(message.chat.id, "Все готово")
    message_handler_start(message)





























def jurnal1(message):
    user_id = message.chat.id
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT grypa FROM login_id WHERE id = {user_id}")
    user_grypa = cursor.fetchone()[0]
    user_grypa = user_grypa.upper().replace('_', '-')

    db_filename = user_grypa + '.db'
    if os.path.exists(db_filename):                 #1_1234
        bot.send_message(message.chat.id,f"Журнал групи {user_grypa} вже створений.")
        jurnal1_1(message)

    else:                                           #2_1234
        bot.send_message(message.chat.id,f"Давайте я допоможу вам створити журнал для вашої групи {user_grypa}",reply_markup=telebot.types.ReplyKeyboardRemove())
        jurnal2_1(message, user_grypa)



def jurnal1_1(message):
    user_id = message.chat.id
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT grypa FROM login_id WHERE id = {user_id}")
    user_grypa = cursor.fetchone()[0]
    user_grypa = user_grypa.upper().replace('_', '-')

    db_filename = user_grypa + '.db'
    conn.close()
    jurnal1_2(message, db_filename, user_grypa)
def jurnal1_2(message,db_filename,user_grypa):
    conn = sqlite3.connect(f'{db_filename}')
    cursor = conn.cursor()
    cursor.execute('SELECT Предмети FROM Предмети')
    result = cursor.fetchall()

    keyboard = []
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for row in result:
        subject = row[0]
        keyboard.append(subject)
        markup.add(types.KeyboardButton(subject))

    markup.add(types.KeyboardButton('🔙Назад'))
    bot.send_message(message.chat.id, "Оберіть журнал предмету з яким ви хочете працювати:", reply_markup=markup)
    bot.register_next_step_handler(message, jurnal1_3, db_filename,user_grypa,keyboard)
    conn.close()
def jurnal1_3(message,db_filename,user_grypa,keyboard):
    subject = message.text
    if subject == '🔙Назад':
        message_handler_start(message)
    elif subject not in keyboard:
        bot.send_message(message.chat.id, "Ви вибрали не вірний предмет")
        jurnal1_2(message,db_filename,user_grypa)

    elif subject.startswith('/'):
        bot.send_message(message.chat.id, "Ви ввели команду будь ласка оберіть предмет:")
        jurnal1_2(message, db_filename, user_grypa)

    elif subject in keyboard:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Модуль 1')
        item2 = types.KeyboardButton('Модуль 2')
        item3 = types.KeyboardButton('Інше')
        back = types.KeyboardButton('🔙Назад')
        markup.add(back)
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)

        bot.send_message(message.chat.id, "Оберіть, розділ:",reply_markup=markup)
        bot.register_next_step_handler(message, jurnal1_4, db_filename, user_grypa, subject)
def jurnal1_4(message,db_filename,user_grypa,subject):
    subject = subject.replace(" ", "_")
    table = message.text
    if table == '🔙Назад':
        message_handler_start(message)

    elif table.startswith('/'):
        bot.send_message(message.chat.id, "Ви ввели команду будь ласка оберіть розділ, який хочете редагувати")
        jurnal1_3(message, db_filename, user_grypa,subject)



    elif table in ['Модуль 1', 'Модуль 2', 'Інше']:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Додати оцінку')
        item2 = types.KeyboardButton('Редагувати назву теми')
        item3 = types.KeyboardButton('Додати тему')
        back = types.KeyboardButton('🔙Назад')
        markup.add(back)
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(message.chat.id, "Оберіть, що саме ви хочете редагувати в журналі:", reply_markup=markup)
        if table == 'Модуль 1':
            table = '1'
        elif table == 'Модуль 2':
            table = '2'
        elif table == 'Інше':
            table = "3"

        bot.register_next_step_handler(message, jurnal1_5, db_filename, user_grypa, subject, table)
def jurnal1_5(message, db_filename, user_grypa, subject, table):
    if message.text == '🔙Назад':
        message_handler_start(message)

    elif message.text == 'Додати оцінку':
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        # Формуємо назву таблиці у форматі {subject}_{table}
        table_name = f'{subject}_{table}'

        # Отримуємо назви стовпців таблиці
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns if column[1] != 'Студенти' and column[1] != 'модуль 1']

        # Створюємо клавіатуру з кнопками зі списку column_names
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for column_name in column_names:
            markup.add(column_name)
        markup.add(types.KeyboardButton('🔙Назад'))

        # Надсилаємо повідомлення з клавіатурою
        bot.send_message(message.chat.id, "Оберіть тему в яку хочете внести оцінки:", reply_markup=markup)
        bot.register_next_step_handler(message, jurnal1_5_1, db_filename, user_grypa, table_name ,column_names)
        conn.close()#1_5_1

    elif message.text == 'Редагувати назву теми':
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        # Формуємо назву таблиці у форматі {subject}_{table}
        table_name = f'{subject}_{table}'

        # Отримуємо назви стовпців таблиці
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns if column[1] != 'Студенти' and column[1] != 'модуль 1' and column[1] != 'модуль 2']

        # Створюємо клавіатуру з кнопками зі списку column_names
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for column_name in column_names:
            markup.add(column_name)
        markup.add(types.KeyboardButton('🔙Назад'))

        # Надсилаємо повідомлення з клавіатурою
        bot.send_message(message.chat.id, "Оберіть тему, яку ви хочете відредагувати:", reply_markup=markup)

        conn.close()
    elif message.text == 'Додати тему':
        bot.send_message(message.chat.id,"Функція покищо не доступна, але вам доступно 10 тем, які ви можете редагувати")
def jurnal1_5_1(message, db_filename, user_grypa,  table_name,column_names):
    tema = message.text
    if tema == '🔙Назад':
        message_handler_start(message)

    elif tema in column_names:
        bot.send_message(message.chat.id,"Будь ласка надішліть мені список студентів вашої групи їхнє повне ім\'я.\nЗа таким зразком⬇️\nТакож я надішлю вам список вашої групи, для зручнішого виставлення оцінок")
        bot.send_message(message.chat.id,"ПІП(Одногрупника) - оцінка\nПІП(Одногрупника) - оцінка\nПІП(Одногрупника) - оцінка")
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        # Витягуємо всі значення зі стовпця "Студенти" таблиці "STUDENTY"
        cursor.execute("SELECT Студенти FROM STUDENTY")
        students = cursor.fetchall()

        # Формуємо повідомлення зі списком студентів
        students_list = "\n".join([student[0] for student in students])

        # Надсилаємо повідомлення зі списком студентів у бота
        bot.send_message(message.chat.id, f"<code>{students_list}</code>", parse_mode=ParseMode.HTML)
        conn.close()
        bot.register_next_step_handler(message,jurnal1_5_2, db_filename, user_grypa,  table_name,tema)
def jurnal1_5_2(message, db_filename, user_grypa, table_name, tema):
    text = message.text
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    rows = text.split("\n")
    for row in rows:
        student_data = row.split(" - ")
        if len(student_data) == 2:
            name, grade = student_data
            cursor.execute(
                f"UPDATE {table_name} SET [{tema}] = ? WHERE Студенти = ?",
                (grade, name))

    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Дані успішно додано до бази даних.")

###########################################################

def jurnal2_1(message, user_grypa):
    # Створення бази даних з назвою групи
    conn = sqlite3.connect(f"{user_grypa}.db")
    cursor = conn.cursor()

    # Створення таблиці STUDENTY
    cursor.execute("CREATE TABLE IF NOT EXISTS STUDENTY (Студенти TEXT)")

    # Створення таблиці Предмети
    cursor.execute("CREATE TABLE IF NOT EXISTS Предмети (Предмети TEXT, Закритий_модуль_1 TEXT, Закритий_модуль_2 TEXT)")

    # Збереження змін до бази даних
    conn.commit()

    # Закриття підключення до бази даних
    conn.close()
    bot.send_message(message.chat.id, "Будь ласка, надішліть мені список студентів вашої групи за таким зразком", reply_markup=None)
    bot.send_message(message.chat.id, "Прізвище ім'я по-батькові\nПрізвище ім'я по-батькові\nПрізвище ім'я по-батькові\nПрізвище ім'я по-батькові\nПрізвище ім'я по-батькові")
    bot.register_next_step_handler(message, jurnal2_2, user_grypa)

def jurnal2_2(message, user_grypa):
    text = message.text
    # Видаляємо цифри з тексту
    text = ''.join(filter(lambda x: not x.isdigit(), text))

    # Знаки, які ми хочемо видалити
    characters_to_remove = '().:;,+#*$&?!`~"'

    # Видаляємо знаки з тексту
    for char in characters_to_remove:
        text = text.replace(char, '')

    jurnal2_3(message, user_grypa,text)

def jurnal2_3(message,user_grypa,text):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Так все вірно')
    item2 = types.KeyboardButton('Редагувати список')
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id, "Будь ласка, перевірте чи ви правильно надіслали мені список своїх одногрупників".format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message,jurnal2_4,user_grypa,text)

def jurnal2_4(message,user_grypa,text):
    vid = message.text


    if vid == 'Так все вірно':

        bot.send_message(message.chat.id, "Вношу в базу...", reply_markup=telebot.types.ReplyKeyboardRemove())
        time.sleep(2)
        jurnal2_5(message, user_grypa, text)

    elif vid == 'Редагувати список':
        jurnal2_1(message, user_grypa)

    #Виводимо результат в консоль

def jurnal2_5(message,user_grypa,text):
    conn = sqlite3.connect(f"{user_grypa}.db")
    cursor = conn.cursor()

    rows = text.split('\n')  # Розділяємо текст на рядки

    # Видаляємо порожні рядки та сортуємо рядки за алфавітом
    rows = [row.strip() for row in rows if row.strip()]
    rows.sort()

    for row in rows:
        cursor.execute("INSERT INTO STUDENTY (Студенти) VALUES (?)", (row,))

    conn.commit()
    bot.send_message(message.chat.id, "Збережено✅")
    bot.send_message(message.chat.id, "А тепер перейдемо до створення журналу предметів, надішліть мені будь ласка ЧЕРЕЗ КОМУ повні назви своїх навчальних дисциплін цього семестру.\nНадсилати ПІП викладачів, які ведуть у вас цей предмет, не потрібно🫠")
    bot.register_next_step_handler(message, jurnal2_6, user_grypa)

def jurnal2_6(message,user_grypa):
    pred = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Так все вірно')
    item2 = types.KeyboardButton('Редагувати')
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id, "Перевірте чи ви правильно надіслали усі навчальні дисципліни", reply_markup=markup)
    bot.send_message(message.chat.id, f"<code>{pred}</code>", parse_mode=ParseMode.HTML)
    bot.register_next_step_handler(message, jurnal2_7 ,user_grypa, pred)

def jurnal2_7(message,user_grypa, pred):
    vid = message.text

    if vid == 'Так все вірно':

        bot.send_message(message.chat.id, "Зберігаю ваші предмети...", reply_markup=telebot.types.ReplyKeyboardRemove())
        time.sleep(2)
        jurnal2_8(message, user_grypa, pred)


    elif vid == 'Редагувати':
        bot.send_message(message.chat.id,"Будь ласка надішліть мені ще раз ваші навчальні дисципліни і переконайтеся чи все вірно)", reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message,jurnal2_6, user_grypa)

def jurnal2_8(message,user_grypa, pred):
    subjects = pred.split(', ')  # Розділяємо рядок за комами

    conn = sqlite3.connect(f"{user_grypa}.db")
    cursor = conn.cursor()

    for subject in subjects:
        cursor.execute("INSERT INTO Предмети (Предмети) VALUES (?)", (subject,))

    conn.commit()
    bot.send_message(message.chat.id, "Створюю таблиці з вашими предметами...")
    jurnal2_9(message, user_grypa)

def jurnal2_9(message,user_grypa):

    conn = sqlite3.connect(f"{user_grypa}.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Предмети FROM Предмети")
    result = cursor.fetchall()
    result = [(item[0].replace(" ", "_"),) for item in result]

    cursor.execute("SELECT Студенти FROM STUDENTY")
    students = cursor.fetchall()

    for row in result:
        pre = row[0]
        cursor.execute(
            f'CREATE TABLE "{pre}_1" ("Студенти" TEXT, [модуль 1] REAL, [тема 0] TEXT, [тема 1] TEXT, [тема 2] TEXT, [тема 3] TEXT, [тема 4] TEXT, [тема 5] TEXT, [тема 6] TEXT, [тема 7] TEXT, [тема 8] TEXT, [тема 9] TEXT)'
        )
        cursor.execute(
            f'CREATE TABLE "{pre}_2" ("Студенти" TEXT, [модуль 2] REAL, [тема 0] TEXT, [тема 1] TEXT, [тема 2] TEXT, [тема 3] TEXT, [тема 4] TEXT, [тема 5] TEXT, [тема 6] TEXT, [тема 7] TEXT, [тема 8] TEXT, [тема 9] TEXT)'
        )
        cursor.execute(
            f'CREATE TABLE "{pre}_3" ("Студенти" TEXT, [модуль 1] REAL, [модуль 2] REAL, [індз] INTEGER, [підсумковий контроль] INTEGER, [загальна кількість балів] REAL)'
        )

        for student in students:
            cursor.execute(f"INSERT INTO \"{pre}_1\" (\"Студенти\") VALUES (?)", (str(student[0]),))
            cursor.execute(f"INSERT INTO \"{pre}_2\" (\"Студенти\") VALUES (?)", (str(student[0]),))
            cursor.execute(f"INSERT INTO \"{pre}_3\" (\"Студенти\") VALUES (?)", (str(student[0]),))

    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Таблиці успішно створенні✅")
    message_handler_start(message)

def redaguvanna(message,user_id):
    den = message.text
    if den == "🔙Назад":
        message_handler_start(message)
    elif den not in ['Понеділок','Вівторок','Середа','Четвер','П\'ятниця']:
        bot.send_message(user_id, "Ви ввели не правильний день, будь ласка виберіть день із наявних кнопок: ")
        bot.register_next_step_handler(message, redaguvanna, user_id)
    else:
        key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT grypa FROM login_id WHERE id = {user_id}")
        user_grypa = cursor.fetchone()[0]
        back = types.KeyboardButton('🔙Назад')
        key.add(back)
        bot.send_message(message.chat.id, f"Ви вибрали {den}, будь ласка надішліть відредагований розкла.\nЗА ТАКИМ ЗРАЗКОМ!!!", reply_markup=key)
        #Продовження допиши як правильно вставляти
        bot.send_message(message.chat.id,'Напишіть назви пар відповідно до їх порядку, якщо у вас вікно тобто не має пари, то можете пропусти її нумерацію, або поставити прочерк')
        redaguvanna2(message, user_id, user_grypa, den)


def redaguvanna2(message, user_id,user_grypa,den):
    days = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'П\'ятниця']
    den_123 = days.index(den)

    # Встановлюємо з'єднання з базою даних
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Виконуємо запит, щоб отримати перший рядок з таблиці "rosklad_СОІМ_23"
    cursor.execute(f'SELECT * FROM rosklad_{user_grypa}')
    # Отримуємо результат запиту (перший рядок таблиці)
    first_row = cursor.fetchall()[den_123]

    mess = ''
    for j, item in enumerate(first_row):
        if item is not None:
            mess += f"{j + 1}. {item}\n"

    bot.send_message(user_id, f'\n<code>{mess}</code>', parse_mode=ParseMode.HTML)
    bot.register_next_step_handler(message, redaguvanna3, user_grypa, user_id, den_123)
    # Закриваємо з'єднання з базою даних
    cursor.close()
    conn.close()

def redaguvanna3(message, user_grypa, user_id, den_123):
    text = message.text  # Отримуємо текст повідомлення
    try:


        # Розбиваємо текст на окремі рядки
        lines = text.split('\n')

        result = [None] * 5  # Результат (кортеж) з початковим значенням None

        for line in lines:
            # Розбиваємо рядок на індекс і значення
            index, value = line.split('. ', 1)

            # Перевіряємо, чи індекс є числом від 1 до 5
            if index.isdigit() and 1 <= int(index) <= 5:
                result[int(index) - 1] = value

        # Виводимо результат (кортеж)
        result = tuple(result)
        bot.send_message(user_id, "Розклад успішно оновленно")
        redaguvanna4(message, user_grypa, user_id, den_123, result )

    except Exception as e:
        bot.send_message(user_id, 'Ви ввели не по зразку, будь ласка надішліть мені ще раз відредагований розклад за зразком')
        bot.send_message(user_id,'<code>1. (Назва пари)\n2. (Назва пари)\n3. (Назва пари)\n4. (Назва пари)\n5. (Назва пари)</code>', parse_mode=ParseMode.HTML)
        bot.register_next_step_handler(message, redaguvanna3, user_grypa, user_id, den_123)

def redaguvanna4(message, user_grypa, user_id, den_123, result):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM rosklad_{user_grypa}')
    rows = cursor.fetchall()
    rows[den_123] = result
    cursor.execute(f'DELETE FROM rosklad_{user_grypa}')
    cursor.executemany(f'INSERT INTO rosklad_{user_grypa} VALUES (?,?,?,?,?)', rows)
    conn.commit()
    cursor.close()
    conn.close()
    message_handler_start(message)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    # Отримання інформації про викладача з бази даних
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Teachers WHERE Викладач=?", (call.data,))
    teacher_info = cursor.fetchone()
    conn.close()

    # Формування повідомлення про викладача
    teacher_name = teacher_info[0]
    phone_number = teacher_info[1]
    email = teacher_info[2]
    full_name = teacher_info[3]
    message_text = f"Викладач: {full_name}\nТелефон: {phone_number}\nПошта: {email}"

    # Відправка повідомлення про викладача
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text)

################################################################################################################################

def rozklad_par_0(message,user_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('СОФІ-11')
    item2 = types.KeyboardButton('СОФА-12')
    item3 = types.KeyboardButton('СОМІ-13')
    item4 = types.KeyboardButton('КМ-14')
    item5 = types.KeyboardButton('СОІМ-15')
    item6 = types.KeyboardButton('ІІП-16')
    item7 = types.KeyboardButton('DA-17')
    item8 = types.KeyboardButton('СОФІ-21')
    item9 = types.KeyboardButton('СОМІ-22')
    item10 = types.KeyboardButton('СОІМ-23')
    item11 = types.KeyboardButton('СОФА-25')
    item12 = types.KeyboardButton('КН-26')
    item13 = types.KeyboardButton('КН-27')
    item14 = types.KeyboardButton('СОФІ-31')
    item15 = types.KeyboardButton('СОМІ-32')
    item16 = types.KeyboardButton('СОІМ-33')
    item17 = types.KeyboardButton('СОФА-35')
    item18 = types.KeyboardButton('КН-36')
    item19 = types.KeyboardButton('СОФІ-41')
    item20 = types.KeyboardButton('СОМІ-42')
    item21 = types.KeyboardButton('СОIM-43')
    item22 = types.KeyboardButton('СОІнск-24')
    item23 = types.KeyboardButton('мСОФ-11')
    item24 = types.KeyboardButton('мСОМ-12')
    item25 = types.KeyboardButton('мСОІн-13')
    item26 = types.KeyboardButton('мСОФ-21')
    item27 = types.KeyboardButton('мСОМ-22')
    item28 = types.KeyboardButton('мСОІн-23')
    back = types.KeyboardButton('🔙Назад')
    keyboard.add(back)
    keyboard.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12, item13,
                 item14, item15, item16, item17, item18, item19, item20, item21, item22, item23, item24,
                 item25, item26, item27, item28)
    bot.send_message(message.chat.id, 'Виберіть вашу групу:', reply_markup=keyboard)
    bot.register_next_step_handler(message, rozklad_par,user_id)

def rozklad_par(message,user_id):
    data = message.text
    if message.text == '🔙Назад':
        message_handler_start(message)

    elif data not in ['СОМІ-32', 'СОІМ-33', 'СОФА-35', 'КН-36', 'мСОФ-11', 'мСОМ-12', 'СОФІ-41', 'СОМІ-42', 'СОIM-43',
          'СОІнск-24', 'мСОІн-13', 'КМ-14', 'СОІМ-15', 'ІІП-16', 'DA-17', 'СОФІ-21', 'СОФІ-21', 'СОМІ-22',
          'КН-26', 'КН-27', 'СОФІ-31', 'СОІМ-23', 'СОФА-25', 'СОФІ-11', 'СОФА-12', 'СОМІ-13', 'мСОФ-21', 'мСОМ-22', 'мСОІн-23']:
        bot.send_message(message.chat.id, "Ви ввели не правильну групу, будь ласка виберіть групу із наявних кнопок: ")
        bot.register_next_step_handler(message, rozklad_par,user_id)
    else:
        data = message.text.upper().replace('-', '_')
        bot.send_message(message.chat.id, "✅")
        rozklad_par2(message, data, user_id)

def rozklad_par2(message,data,user_id):

    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM rosklad_{data}")
    dates = cursor.fetchall()
    days = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'П`ятниця']
    times = ['8:00-9:20', '9:35-10:55', '11:10-12:30', '12:45-14:05', '14:20-15:40']
    mess = ''
    for i, date in enumerate(dates):
        mess += days[i] + ':\n'
        for j, item in enumerate(date):
            if item is not None:
                mess += f"{times[j]} {j + 1}. {item}\n"
        mess += '\n'

    bot.send_message(user_id,"Розклад пар для групи " + data.replace('_', '-') + ':\n\n' + mess)
    bot.register_next_step_handler(message, rozklad_par,user_id )


def update_email(message):
    new_email = message.text
    user_id = message.from_user.id
    if new_email == "/start" or new_email == "/menu" or new_email == '/support' or new_email == '/homework' or new_email == '/idea' or new_email == '/shurik' or new_email == '/legion':
        bot.send_message(message.chat.id,'Ви ввели команду, а не пошту будь ласка введіть пошту🥹')
        bot.register_next_step_handler(message, update_email)
    else:

        # Перевірка чи введений email закінчується на "@fizmat.tnpu.edu.ua"
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Email_Base WHERE Email_Address=?", (new_email,))
        row = cursor.fetchone()
        if row:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            cursor.execute("UPDATE login_id SET email=? WHERE id=?", (new_email, user_id))
            conn.commit()

            conn.close()
            bot.send_message(message.chat.id, "🦦Пошту успішно оновлено!")
            message_handler_start(message)
        else:
            # Надсилання повідомлення про неправильний формат email
            bot.send_message(message.chat.id,
                             "🙅Введена email адреса не є фізматівською. Будь ласка, введіть ще раз свою email адресу")
            # Повернення до функції get_email для очікування наступного вводу від користувача

            bot.register_next_step_handler(message, update_email)

def update_grypa(message):
    new_grypa = message.text.upper().replace('-', '_')
    user_id = message.from_user.id
    if new_grypa == "/start" or new_grypa == "/menu" or new_grypa == '/support' or new_grypa == '/homework' or new_grypa == '/idea' or new_grypa == '/shurik' or new_grypa == '/legion':
        bot.send_message(message.chat.id, "Ви ввели команду, а не групу. Будь ласка, виберіть групу із кнопок.")
        bot.register_next_step_handler(message, update_grypa)
    elif message.text in ['СОМІ-32','СОІМ-33', 'СОФА-35', 'КН-36', 'мСОФ-11', 'мСОМ-12', 'СОФІ-41', 'СОМІ-42', 'СОІМ-43',
                              'СОІнск-24', 'мСОІн-13','КМ-14', 'СОІМ-15', 'ІІП-16','DA-17', 'СОФІ-21', 'СОФІ-21', 'СОМІ-22', 'КН-26',
                              'КН-27', 'СОФІ-31','СОМІ-23', 'СОФА-25', 'СОФІ-11', 'СОФА-12', 'СОМІ-13',]:
        # Встановлення підключення до бази даних
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        # Виконання запиту для оновлення групи користувача
        cursor.execute("UPDATE login_id SET grypa=? WHERE id=?", (new_grypa, user_id))
        conn.commit()
        # Відправлення повідомлення з питанням про нову групу
        bot.send_message(message.chat.id, "🦦Група оновлена успішно!")
        # Закриття підключення до бази даних
        conn.close()
        message_handler_start(message)
    else:
        bot.send_message(message.chat.id, "Ви ввели щось не зрозуміле мені, напевно це не група(")
        bot.register_next_step_handler(message, update_grypa)

def update_first_last(message):
    new_first_last = message.text
    user_id = message.from_user.id
    # Встановлення підключення до бази даних
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Виконання запиту для оновлення прізвища та імені користувача
    cursor.execute("UPDATE login_id SET first_last=? WHERE id=?", (new_first_last, user_id))
    conn.commit()
    # Відправлення повідомлення з підтвердженням оновлення
    bot.send_message(message.chat.id, "🦦Прізвище та ім'я оновлені успішно!")
    # Закриття підключення до бази даних
    conn.close()


bot.polling(none_stop=True)
