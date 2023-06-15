import telebot
import sqlite3
from telebot import types
from telegram import ParseMode
import datetime
import urllib.request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, KeyboardButton
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
        user_name = message.chat.username
        user_id = message.chat.id

        # Запит email
        bot.send_message(message.chat.id, "Будь ласка, введіть свою email адресу:")
        bot.register_next_step_handler(message, get_email)

    else:
        bot.send_message(message.chat.id, "Ти вже зареєстрований!")


def get_email(message: types.Message):
    email = message.text
    if email == "/start" or email == "/menu" or email == '/support' or email == '/homework' or email == '/idea' or email == '/shurik' or email == '/legion':
        bot.send_message(message.chat.id, "Ви ввели команду а не пошту будь ласка введіть свою фізматівську пошту: ")
        bot.register_next_step_handler(message, get_email)
    else:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Email_Base WHERE Email_Address=?", (email,))
        row = cursor.fetchone()
        if row:
            # Запит групи

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
            bot.register_next_step_handler(message, get_group, email)
        else:
            # Email does not exist, send error message
            bot.send_message(message.chat.id,"Вашої пошти не знайдено в базі даних фізмату. Будь ласка, введіть свою пошту ще раз правильно.")
            # Return to the get_email function to wait for the next input from the user
            bot.register_next_step_handler(message, get_email)

        cursor.close()
        conn.close()


def get_group(message: types.Message, email):
    group = message.text
    if group not in ['СОМІ-32', 'СОІМ-33', 'СОФА-35', 'КН-36', 'мСОФ-11', 'мСОМ-12', 'СОФІ-41', 'СОМІ-42', 'СОIM-43',
                     'СОІнск-24', 'мСОІн-13', 'КМ-14', 'СОІМ-15', 'ІІП-16', 'DA-17', 'СОФІ-21', 'СОФІ-21', 'СОМІ-22',
                     'КН-26',
                     'КН-27', 'СОФІ-31', 'СОІМ-23', 'СОФА-25', 'СОФІ-11', 'СОФА-12', 'СОМІ-13','мСОФ-21','мСОМ-22','мСОІн-23']:
        bot.send_message(message.chat.id,"Ви ввели не правильну групу виберіть ще раз свою групу:")
        bot.register_next_step_handler(message, get_group, email)
    elif email == "/start" or email == "/menu" or email == '/support' or email == '/homework' or email == '/idea' or email == '/shurik' or email == '/legion':
        bot.send_message(message.chat.id, "Будь ласка будьте уважніші ви ввели команду а не назву групи, будь ласка введіть свою групу😡 ")
        bot.register_next_step_handler(message, get_group, email)
    else:
        group = message.text.upper().replace('-', '_')
        bot.send_message(message.chat.id, "Будь ласка, введіть своє ПІБ:")
        bot.register_next_step_handler(message, get_first_last, email, group)
def get_first_last(message: types.Message, email, group):
    first_last = message.text

    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    user_id = message.chat.id
    user_name = message.chat.username

    # Вставка даних в базу даних
    cursor.execute("INSERT INTO login_id (id, username, email, grypa, first_last) VALUES(?, ?, ?, ?, ?);",
                   (user_id, user_name, email, group, first_last))
    connect.commit()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_student = types.KeyboardButton("Студент")
    button_starosta = types.KeyboardButton("Староста")
    button_vikladach = types.KeyboardButton("Викладач")
    keyboard.add(button_student, button_starosta, button_vikladach)
    bot.send_message(message.chat.id, "Виберіть вашу роль:", reply_markup=keyboard)
    bot.register_next_step_handler(message, get_role, email, group, first_last)


def get_role(message: types.Message, email, group, first_last):
    role = message.text

    if role == 'Студент':
        # Встановлення ролі студента в базі даних
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute("UPDATE login_id SET roli = ? WHERE id = ?;", ('студент', message.chat.id))
        connect.commit()

        bot.send_message(message.chat.id, f"Ви зареєстровані як студент!") 
        create_group_tables()
        message_handler_start(message)

    elif role == 'Викладач':
        # Запит паролю для ролі викладача
        bot.send_message(message.chat.id, "Будь ласка, введіть пароль для викладача:")
        bot.register_next_step_handler(message, get_password, 'викладач', email, group, first_last)

    elif role == 'Староста':
        # Запит паролю для ролі старости
        bot.send_message(message.chat.id, "Будь ласка, введіть пароль для старости:")
        bot.register_next_step_handler(message, get_password, 'староста', email, group, first_last)

    else:
        # Надсилання повідомлення про неправильний вибір ролі
        bot.send_message(message.chat.id, "Виберіть роль з наданих кнопок.")
        bot.register_next_step_handler(message, get_role, email, group, first_last)


def get_password(message: types.Message, role, email, group, first_last):
    password = message.text

    if role == 'викладач' and password == '000':
        # Встановлення ролі викладача в базі даних
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute("UPDATE login_id SET roli = ? WHERE id =?;", ('викладач', message.chat.id))
        connect.commit()
        bot.send_message(message.chat.id, f"Ви зареєстровані як викладач!")
        create_group_tables()
        message_handler_start(message)
    elif role == 'староста' and password == '111':
        # Встановлення ролі старости в базі даних
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute("UPDATE login_id SET roli = ? WHERE id = ?;", ('староста', message.chat.id))
        connect.commit()

        bot.send_message(message.chat.id, f"Ви зареєстровані як староста!")
        create_group_tables()

        message_handler_start(message)



    else:
        # Надсилання повідомлення про неправильний пароль
        bot.send_message(message.chat.id, "Неправильний пароль. Спробуйте ще раз.")
        bot.register_next_step_handler(message, get_password, role, email, group, first_last)

def create_group_tables():
    # Встановлення з'єднання з базою даних
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Отримання унікальних груп з бази даних
    cursor.execute("SELECT DISTINCT grypa FROM login_id")
    groups = cursor.fetchall()
    # Створення таблиць для кожної групи
    for group in groups:
        group_name = group[0].replace("-", "_")
        table_name = f"{group_name}"
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} (subject TEXT, text TEXT , photo BLOB, file BLOB)")
    conn.close()
    create_user_tables()


def create_user_tables():
    # підключення до бази даних
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # отримання унікальних ідентифікаторів користувачів з таблиці login_id
    cursor.execute("SELECT DISTINCT id FROM login_id")
    users = cursor.fetchall()
    # створення таблиць для кожного користувача
    for user in users:
        user_id = user[0]
        table_name = f"table_{user_id}"
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} (subject TEXT, text TEXT , photo BLOB, file BLOB, actual TEXT)")
    conn.close()
    create_rozklad_table()

def create_rozklad_table():
    # Встановлення з'єднання з базою даних
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Отримання унікальних груп з бази даних
    cursor.execute("SELECT DISTINCT grypa FROM login_id")
    groups = cursor.fetchall()
    # Створення таблиць для кожної групи
    for group in groups:
        group_name = group[0].replace("-", "_")
        table_name = f"{group_name}"
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS rosklad_{table_name} (Понеділок TEXT, Вівторок TEXT , Середа TEXT, Четвер TEXT, Пятниця TEXT)")
    conn.close()






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
    item2 = types.KeyboardButton('Додати оцінки?')
    homework = types.KeyboardButton('Додати домашку')
    item3 = types.KeyboardButton('Редагувати домашку')
    item4 = types.KeyboardButton('Оголошення для групи')
    back = types.KeyboardButton('🔙Назад')

    markup.add(back)
    markup.add(item1)
    markup.add(item2)
    markup.add(homework)
    markup.add(item3)
    markup.add(item4)
    bot.send_message(message.chat.id, "Це меню призначене спеціально для старост, і ви можете ознайомитися зі списком майбутніх функцій, які будуть додані😌".format(message.from_user), reply_markup=markup)




@bot.message_handler(commands=['menu'])
def message_handler_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('📜Профіль')
    item2 = types.KeyboardButton('✍️Розклад пар')
    item3 = types.KeyboardButton('Контакти викладачів')
    item4 = types.KeyboardButton('Журнал')
    item5 = types.KeyboardButton('Інформація про розробників')
    item6 = types.KeyboardButton('Домашка')
    item_menu = types.KeyboardButton('Старостам')
    markup.add(item1, item2, item3, item4, item5,item6)
    markup.add(item_menu)
    bot.send_message(message.chat.id, "👇".format(message.from_user), reply_markup=markup)



@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Інформація про розробників':
            bot.send_message(message.chat.id, 'Засновник @yura_krykh\nВведіть команду /support якшо виникли проблеми')
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


        elif message.text == 'Журнал':
            bot.send_message(message.chat.id, "Ця функція покищо недоступна")


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

        elif message.text == '🔙Назад':
            message_handler_start(message)

        elif message.text == 'Назад🔙':
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
                    item3 = types.KeyboardButton('Середа')
                    item4 = types.KeyboardButton('Четвер')
                    item5 = types.KeyboardButton('П\'ятниця')
                    back = types.KeyboardButton('Назад🔙')
                    keyboard.add(back)
                    keyboard.add(item1, item2, item3, item4, item5)

                    bot.send_message(message.chat.id, "АГА", reply_markup=keyboard)
                    bot.register_next_step_handler(message, redaguvanna, user_id)
                else:
                    bot.send_message(message.chat.id, "Ви не є старостою, ви не можете користуватися цим меню)")
                    message_handler_start(message)


def redaguvanna(message,user_id):
    den = message.text
    if den not in ['Понеділок','Вівторок','Середа','Четвер','П\'ятниця']:
        bot.send_message(user_id, "Ви ввели не правильний день, будь ласка виберіть день із наявних кнопок: ")
        bot.register_next_step_handler(message, redaguvanna, user_id)
    else:
        key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT grypa FROM login_id WHERE id = {user_id}")
        user_grypa = cursor.fetchone()[0]
        back = types.KeyboardButton('Назад🔙')
        key.add(back)
        bot.send_message(message.chat.id, f"Ви вибрали {den}...", reply_markup=key)#Продовження допиши як правильно вставляти
        bot.register_next_step_handler(message, redaguvanna2, user_id, user_grypa)


def redaguvanna2(message, user_id,user_grypa):
    print(user_grypa)






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
