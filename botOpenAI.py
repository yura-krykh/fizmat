import telebot
import sqlite3
from telebot import types
from telegram import ParseMode
import datetime
import urllib.request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json

ALLOWED_CHAT_ID = 628446966
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
    if email == '/start' or email == "/menu" or email == '/support' or email == '/homework' or email == '/idea' or email == '/shurik':
        bot.send_message(message.chat.id, "Ви ввели команду а не пошту будь ласка введіть свою фізматівську пошту: ")
        bot.register_next_step_handler(message, get_email)
    else:

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Check if the email exists in the Email_Base table
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
            item21 = types.KeyboardButton('СОІМ-43')
            item22 = types.KeyboardButton('СОІнск-24')
            item23 = types.KeyboardButton('мСОФ-11')
            item24 = types.KeyboardButton('мСОМ-12')
            item25 = types.KeyboardButton('мСОІн-13')
            item26 = types.KeyboardButton('мСОФ-21')
            item27 = types.KeyboardButton('мСОМ-22')
            item28 = types.KeyboardButton('мСОІн-23')

            keyboard.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12, item13,item14, item15, item16, item17, item18, item19, item20, item21, item22, item23, item24, item25,item26, item27, item28)
            bot.send_message(message.chat.id,"Будь ласка, будьте уважні при виборі своєї групи. Оберіть дійсну групу, оскільки редагування групи не буде можливим.",reply_markup=keyboard)
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
    if group == '/start' or group == "/menu" or group == '/support' or group == '/homework' or group == '/idea' or group == '/shurik':
        bot.send_message(message.chat.id, "Ви ввели команду а не групу будь ласка виберіть свою групу: ")
        bot.register_next_step_handler(message, get_group, email)
    else:
        # Запит імені та прізвища
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('📜Профіль')
        item2 = types.KeyboardButton('✍️Розклад пар')
        item3 = types.KeyboardButton('Контакти викладачів')
        item4 = types.KeyboardButton('Журнал')
        item5 = types.KeyboardButton('Інформація про розробників')
        item6 = types.KeyboardButton('Домашка')
        markup.add(item1, item2, item3, item4, item5, item6)
        bot.send_message(message.chat.id, "👇".format(message.from_user), reply_markup=markup)

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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('📜Профіль')
        item2 = types.KeyboardButton('✍️Розклад пар')
        item3 = types.KeyboardButton('Контакти викладачів')
        item4 = types.KeyboardButton('Журнал')
        item5 = types.KeyboardButton('Інформація про розробників')
        item6 = types.KeyboardButton('Домашка')
        markup.add(item1, item2, item3, item4, item5, item6)
        bot.send_message(message.chat.id, "👇".format(message.from_user), reply_markup=markup)
    elif role == 'староста' and password == '111':
        # Встановлення ролі старости в базі даних
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute("UPDATE login_id SET roli = ? WHERE id = ?;", ('староста', message.chat.id))
        connect.commit()

        bot.send_message(message.chat.id, f"Ви зареєстровані як староста!")

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('📜Профіль')
        item2 = types.KeyboardButton('✍️Розклад пар')
        item3 = types.KeyboardButton('Контакти викладачів')
        item4 = types.KeyboardButton('Журнал')
        item5 = types.KeyboardButton('Інформація про розробників')
        item6 = types.KeyboardButton('Домашка')
        markup.add(item1, item2, item3, item4, item5, item6)
        bot.send_message(message.chat.id, "👇".format(message.from_user), reply_markup=markup)

    else:
        # Надсилання повідомлення про неправильний пароль
        bot.send_message(message.chat.id, "Неправильний пароль. Спробуйте ще раз.")
        bot.register_next_step_handler(message, get_password, role, email, group, first_last)


@bot.message_handler(commands=['menu'])
def message_handler_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('📜Профіль')
    item2 = types.KeyboardButton('✍️Розклад пар')
    item3 = types.KeyboardButton('Контакти викладачів')
    item4 = types.KeyboardButton('Журнал')
    item5 = types.KeyboardButton('Інформація про розробників')
    item6 = types.KeyboardButton('Домашка')
    markup.add(item1, item2, item3, item4, item5,item6)
    bot.send_message(message.chat.id, "👇".format(message.from_user), reply_markup=markup)


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
        bot.register_next_step_handler(message, photo_work, subject)



def photo_work(message: types.Message, subject):
    text_work = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Так')
    item2 = types.KeyboardButton('Ні')
    keyboard.add(item1, item2)
    bot.send_message(message.chat.id, "У Вас будуть якісь ще додаткові фото або файли?\nВиберіть варіант нижче", reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_extra_files, subject=subject, text_work=text_work)

def handle_extra_files(message: types.Message, subject, text_work):
    if message.text == 'Ні':
        save_homework(message, subject, text_work)
    elif message.text == 'Так':
        bot.send_message(message.chat.id,'Будь ласка, надішліть мені додатковий файл або фотографію для домашнього завдання:',reply_markup=None)
        bot.register_next_step_handler(message, save_homework_and_file, subject=subject, text_work=text_work)

def save_homework(message: types.Message, subject, text_work):
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

    if user_grypa is not None:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM login_id WHERE grypa = ?", (user_grypa,))
            rows = cursor.fetchall()
            for row in rows:
                bot.send_message(row[0], f"У вас з'явилося нове домашнє завдання у предметі {subject}. Будь ласка, перегляньте його. (Надіслано від @{message.chat.username})")


def save_homework_and_file(message: types.Message, subject, text_work):
    user_id = message.from_user.id
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT grypa FROM login_id WHERE id = {user_id}")
    user_grypa = cursor.fetchone()[0]

    if message.photo:
        # якщо користувач надіслав фото, то зберігаємо його в папку "photos" на сервері
        photo_file = message.photo[-1].file_id
        photo_path = bot.get_file(photo_file).file_path
        photo_name = f"{user_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        urllib.request.urlretrieve(f"https://api.telegram.org/file/bot{TELEGRAM_API_KEY}/{photo_path}", f"photos/{photo_name}")

        # додаємо запис до бази даних з фото
        insert_query = f"INSERT INTO {user_grypa} (subject, text, photo) VALUES (?, ?, ?)"
        cursor.execute(insert_query, (subject, text_work, photo_name))


    elif message.document:
        # якщо користувач надіслав файл, то зберігаємо його в папку "files" на сервері
        file_name = message.document.file_name
        file_path = bot.get_file(message.document.file_id).file_path
        saved_file_name = f"{user_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_name}"
        urllib.request.urlretrieve(f"https://api.telegram.org/file/bot{TELEGRAM_API_KEY}/{file_path}", f"files/{saved_file_name}")

        # додаємо запис до бази даних з файлом
        insert_query = f"INSERT INTO {user_grypa} (subject, text, file) VALUES (?, ?, ?)"
        cursor.execute(insert_query, (subject, text_work, saved_file_name))

    conn.commit()
    bot.send_message(message.chat.id, "✅ Домашнє завдання збережено та розіслано вашим одногрупникам!")
















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
    chat_id = message.chat.id
    if chat_id != ALLOWED_CHAT_ID:
        bot.send_message(chat_id=chat_id, text='Ви не маєте доступу до цієї команди.')
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


@bot.message_handler(commands=['news'])
def send_news(message):
    # Запит повідомлення, яке потрібно розіслати
    bot.send_message(chat_id=message.chat.id, text='Введіть повідомлення для розсилки:')
    bot.register_next_step_handler(message, news_handler)


def news_handler(message):
    # Отримання повідомлення від користувача та розсилка його всім користувачам бота
    news = message.text
    users = get_all_users()  # Отримання всіх користувачів бота
    for user in users:
        bot.send_message(chat_id=user, text=news)


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


@bot.message_handler(commands=['structure'])
def handle_structure_command(message):
    chat_id = message.chat.id
    if chat_id != ALLOWED_CHAT_ID:
        bot.send_message(chat_id=chat_id, text='Ви не маєте доступу до цієї команди.')
        return

    try:
        # Виклик функції для створення таблиць з користувачами за групами
        create_group_tables()
        bot.send_message(chat_id=chat_id, text='Таблиці створено успішно!')
    except Exception as e:
        bot.send_message(chat_id=chat_id, text=f'Помилка: {e}')


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
            f"CREATE TABLE IF NOT EXISTS {table_name} (subject TEXT, text TEXT NOT NULL, photo BLOB, file BLOB)")
    conn.close()


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Інформація про розробників':
            bot.send_message(message.chat.id, 'Засновник @yura_krykh\nВведіть команду /support якшо виникли проблеми')

        elif message.text == 'Домашка':
            bot.send_message(message.chat.id, 'Функція на днях буде доступна)\nОчікуйте)))')

        elif message.text == '✍️Розклад пар':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            COFI_11 = types.KeyboardButton('COФІ-11')
            COFA_12 = types.KeyboardButton('COФA-12')
            COMI_13 = types.KeyboardButton('COMI-13')
            KM_14 = types.KeyboardButton('КМ-14')
            COIM_15 = types.KeyboardButton('COІМ-15')
            IIP_16 = types.KeyboardButton('ІІП-16')
            DA_17 = types.KeyboardButton('DA-17')
            COFI_21 = types.KeyboardButton('COФІ-21')
            COMI_22 = types.KeyboardButton('COMI-22')
            COIM_23 = types.KeyboardButton('COIM-23')
            COFA_25 = types.KeyboardButton('СОФА-25')
            KH_26 = types.KeyboardButton('КН-26')
            KH_27 = types.KeyboardButton('КН-27')
            COFI_31 = types.KeyboardButton('COФІ-31')
            COМІ_32 = types.KeyboardButton('COМІ-32')
            COIM_33 = types.KeyboardButton('COIM-33')
            COFA_35 = types.KeyboardButton('СОФА-35')
            KH_36 = types.KeyboardButton('КН-36')
            mCOF_11 = types.KeyboardButton('мСОФ-11')
            mCOM_12 = types.KeyboardButton('мСОМ-12')
            mCOIH_13 = types.KeyboardButton('мСОІн-13')
            FI_41 = types.KeyboardButton('ФІ-41')
            MI_42 = types.KeyboardButton('МІ-42')
            MI_43 = types.KeyboardButton('МІ-43')
            COIHCK_24 = types.KeyboardButton('СОІнск-24')

            back = types.KeyboardButton('🔙Назад')
            markup.add(back)
            markup.add(back, COFI_11, COFA_12, COMI_13, KM_14, COIM_15, IIP_16, DA_17, COFI_21, COMI_22, COIM_23,
                       COFA_25, KH_26, KH_27, COFI_31, COМІ_32, COIM_33, COFA_35, KH_36, mCOF_11, mCOM_12, mCOIH_13,
                       FI_41, MI_42, MI_43, COIHCK_24)

            bot.send_message(message.chat.id, 'Виберіть вашу групу:', reply_markup=markup)
        elif message.text in ['COIM-23', 'СОФА-25', 'COФІ-11', 'COФA-12', 'COMI-13', 'КМ-14', 'COІМ-15', 'ІІП-16',
                              'DA-17', 'COФІ-21', 'COФІ-21', 'COMI-22', 'КН-26', 'КН-27', 'COФІ-31', 'COМІ-32',
                              'COIM-33', 'СОФА-35', 'КН-36', 'мСОФ-11', 'мСОМ-12', 'ФІ-41', 'МІ-42', 'ІМ-43',
                              'СОІнск-24', 'мСОІн-13']:
            group = message.text  # Оновлюємо значення змінної group на основі вибраної групи
            if group == 'COIM-23':
                schedule = "Понеділок:\n8:00-9:20 1. Аналіз алгоритмів\n9:35-10:55 2. Аналіз алгоритмів\n11:10-12:30 3. Іноземна мова\n12:45-14:05 4. Фізичне виховання\n\nВівторок:\n8:00-9:20 1. -\n9:35-10:55 2. Дискретна математика\n11:10-12:30 3. Дискретна математика\n12:45-14:05 4. Основи теорії графів\n\nСереда:\n8:00-9:20 1. Комп'ютерні мережі\n9:35-10:55 2. Комп'ютерні мережі\n11:10-12:30 3. Комп'ютерна графіка\n12:45-14:05 4. Комп'ютерна графіка\n\nЧетвер:\n8:00-9:20 1. Комп'ютерна математика\n9:35-10:55 2. Комп'ютерна математика\n11:10-12:30 3. Програмування\n12:45-14:05 4. Програмування\n\nП'ятниця:\n8:00-9:20 1. Диференціальні рівняння\n9:35-10:55 2. Диференціальні рівняння\n11:10-12:30 3. Етика і естетика\n12:45-14:05 4. Етика і естетика"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'СОФА-25':
                schedule = "Понеділок:\n8:00-9:20 1. Елементарна фізика \n9:35-10:55 2. Елементарна фізика\n11:10-12:30 3. Фізичне виховання \n12:45-14:05 4. -\nВівторок:\n8:00-9:20 1. Практичний курс англійської мови\n9:35-10:55 2. Практичний курс англійської мови\n11:10-12:30 3. -\n12:45-14:05 4. -\nСереда:\n8:00-9:20 1.  Практична граматика і практична фонетика)\n9:35-10:55 2. Практична граматика і практична фонетика\n11:10-12:30 3. Загальна фізика\n12:45-14:05 4. -\nЧетвер:\n8:00-9:20 1.  Загальна фізика\n9:35-10:55 2.  ПРФЗ\n11:10-12:30 3.  Цифрові технології в освітньому процесі\n12:45-14:05 4.  Цифрові технології в освітньому процесі \nП’ятниця:\n8:00-9:20 1.  Методика навчання англійської мови\n9:35-10:55 2.  Методика навчання англійської мови\n11:10-12:30 3.  Основи права\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'COФІ-11':
                schedule = "Понеділок:\n8:00-9:20 1. Математичний аналіз\n9:35-10:55 2.Математичний аналіз\n11:10-12:30 3.Алгебра та геометрія\n12:45-14:05 4. -\n\nВівторок:\n8:00-9:20 1. Загальна фізика\n9:35-10:55 2. Загальна фізика\n11:10-12:30 3. Іноземна мова\n12:45-14:05 4. Психологія\n\nСереда:\n8:00-9:20 1. Фізичне виховання\n9:35-10:55 2. Психологія\n11:10-12:30 3. Алгебра та геометрія\n12:45-14:05 4. -\n\nЧетвер:\n8:00-9:20 1. Загальна фізика\n9:35-10:55 2. ПРФЗ\n11:10-12:30 3.Педагогіка\n12:45-14:05 4. Педагогіка\n\nП'ятниця:\n8:00-9:20 1. Елементарна фізика\n9:35-10:55 2. Елементарна фізика\n11:10-12:30 3. -\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'COФA-12':
                schedule = "Понеділок:\n8:00-9:20 1. Практичний курс англійської мови\n9:35-10:55 2. Практичний курс англійської мови\n11:10-12:30 3.-\n12:45-14:05 4. -\n\nВівторок:\n8:00-9:20 1. Загальна фізика\n9:35-10:55 2. Загальна фізика\n11:10-12:30 3.-\n12:45-14:05 4. Психологія\n\nСереда:\n8:00-9:20 1. Фізичне виховання\n9:35-10:55 2. Психологія\n11:10-12:30 3. Вища математика\n12:45-14:05 4. Вища математика\n\nЧетвер:\n8:00-9:20 1. Загальна фізика\n9:35-10:55 2. ПРФЗ\n11:10-12:30 3.Педагогіка\n12:45-14:05 4. Педагогіка\n\nП'ятниця:\n8:00-9:20 1. Елементарна фізика\n9:35-10:55 2. Елементарна фізика\n11:10-12:30 3. Практична граматика і практична фонетика\n12:45-14:05 4. Практична граматика і практична фонетика"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'COMI-13':
                schedule = "Понеділок:\n8:00-9:20 1. -\n9:35-10:55 2. Елементарна математика\n11:10-12:30 3. Аналітична геометрія\n12:45-14:05 4. Аналітична геометрія\n\nВівторок:\n8:00-9:20 1. -\n9:35-10:55 2. Математичний аналіз\n11:10-12:30 3. Фізичне виховання\n12:45-14:05 4. Психологія\n\nСереда:\n8:00-9:20 1. -\n9:35-10:55 2. Математичний аналіз\n11:10-12:30 3. Психологія\n12:45-14:05 4. Педагогіка\n\nЧетвер:\n8:00-9:20 1. -\n9:35-10:55 2. Математичний аналіз\n11:10-12:30 3. Іноземна мова\n12:45-14:05 4. Педагогіка\n\nП'ятниця:\n8:00-9:20 1. Лінійна алгебра\n9:35-10:55 2. Лінійна алгебра\n11:10-12:30 3. Лінійна алгебра\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'КМ-14':
                schedule = "Понеділок:\n8:00-9:20 1. Математичний аналіз\n9:35-10:55 2. Математичний аналіз\n11:10-12:30 3. Аналітична геометрія\n12:45-14:05 4. Аналітична геометрія\n\nВівторок:\n8:00-9:20 1. Рекреаційна математика\n9:35-10:55 2. Рекреаційна математика\n11:10-12:30 3. -\n12:45-14:05 4. Психологія\n\nСереда:\n8:00-9:20 1. Фізичне виховання\n9:35-10:55 2. Англійська мова\n11:10-12:30 3. Психологія\n12:45-14:05 4. Педагогіка\n\nЧетвер:\n8:00-9:20 1. -\n9:35-10:55 2. Програмування\n11:10-12:30 3. Обчислювальна математика\n12:45-14:05 4. Педагогіка\n\nП'ятниця:\n8:00-9:20 1. Лінійна алгебра\n9:35-10:55 2. Лінійна алгебра\n11:10-12:30 3. Лінійна алгебра\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'COІМ-15':
                schedule = "Понеділок:\n8:00-9:20 1. Математичний аналіз\n9:35-10:55 2. Математичний аналіз\n11:10-12:30 3. Алгебра та геометрія\n12:45-14:05 4. -\n\nВівторок:\n8:00-9:20 1. Програмне забезпечення КС\n9:35-10:55 2. Програмне забезпечення КС\n11:10-12:30 3. Англійська мова (13 ст.)\n12:45-14:05 4. Психологія\n\nСереда:\n8:00-9:20 1. -\n9:35-10:55 2. Педагогіка \n11:10-12:30 3. Алгебра та геометрія (13 ст.)\n12:45-14:05 4. Психологія\n\nЧетвер:\n8:00-9:20 1. Програмування \n9:35-10:55 2. -\n11:10-12:30 3. Елементарна математика\n12:45-14:05 4. Педагогіка\n\nП'ятниця:\n8:00-9:20 1. Операційні системи\n9:35-10:55 2. Операційні системи (15 ст.)\n11:10-12:30 3. Операційні системи (15 ст.)\n12:45-14:05 4. Фізичне виховання"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'ІІП-16':
                schedule = " Понеділок:\n8:00-9:20 1. Анімація та відеомонтаж\n9:35-10:55 2. Анімація та відеомонтаж\n11:10-12:30 3. Комп'ютерна графіка\n12:45-14:05 4. Комп'ютерна графіка\n\nВівторок:\n8:00-9:20 1. Математичні основи комп'ютерної графіки\n9:35-10:55 2. Дискретна математика\n11:10-12:30 3. Дискретна математика\n12:45-14:05 4. -\n\nСереда:\n8:00-9:20 1. Фізичне виховання\n9:35-10:55 2. Іноземна мова\n11:10-12:30 3.Вища математика\n12:45-14:05 4. Вища математика\n\nЧетвер:\n8:00-9:20 1. Програмування\n9:35-10:55 2. -\n11:10-12:30 3. Психологія ігор\n12:45-14:05 4. Психологія ігор\n\nП'ятниця:\n8:00-9:20 1. Операційні системи\n9:35-10:55 2. Операційні системи \n11:10-12:30 3. Операційні системи \n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'DA-17':
                schedule = "Понеділок:\n8:00-9:20 1. -\n9:35-10:55 2. -\n11:10-12:30 3. Комп'ютерна графіка\n12:45-14:05 4. Комп'ютерна графіка\n\nВівторок:\n8:00-9:20 1. Аналітична діяльність в інформаційних процесах\n9:35-10:55 2. Дискретна математика\n11:10-12:30 3. Дискретна математика\n12:45-14:05 4. -\n\nСереда:\n8:00-9:20 1. Фізичне виховання\n9:35-10:55 2. Іноземна мова\n11:10-12:30 3.Вища математика\n12:45-14:05 4. Вища математика\n\nЧетвер:\n8:00-9:20 1. -\n9:35-10:55 2. Програмування\n11:10-12:30 3. Економічна теорія\n12:45-14:05 4. Економічна теорія\n\nП'ятниця:\n8:00-9:20 1. Операційні системи\n9:35-10:55 2. Операційні системи \n11:10-12:30 3. Операційні системи \n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'COФІ-21':
                schedule = "Понеділок:\n8:00-9:20 1. Елементарна фізика\n9:35-10:55 2. Елементарна фізика\n11:10-12:30 3. Фізичне виховання\n12:45-14:05 4. Іноземна мова\n\nВівторок:\n8:00-9:20 1. Комп'ютерні мережі\n9:35-10:55 2. Комп'ютерні мережі\n11:10-12:30 3. Програмування\n12:45-14:05 4. Програмування\n\nСереда:\n8:00-9:20 1. Диференціальні та інтегральні рівняння\n9:35-10:55 2. Диференціальні та інтегральні рівняння\n11:10-12:30 3. Загальна фізика\n12:45-14:05 4. Загальна фізика\n\nЧетвер:\n8:00-9:20 1. Загальна фізика\n9:35-10:55 2. ПРФЗ\n11:10-12:30 3. -\n12:45-14:05 4. -\n\nП'ятниця:\n8:00-9:20 1. -\n9:35-10:55 2. -\n11:10-12:30 3. Основи права \n12:45-14:05 4. Основи права"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'COМI-22':
                schedule = "Понеділок:\n8:00-9:20 1. Фізичне виховання\n9:35-10:55 2. Іноземна мова\n11:10-12:30 3. Основи геометрії\n12:45-14:05 4.Основи геометрії\n\nВівторок:\n8:00-9:20 1. Математичний аналіз\n9:35-10:55 2. Математичний аналіз\n11:10-12:30 3. Програмування\n12:45-14:05 4. Програмування\n\nСереда:\n8:00-9:20 1. Основи кібербезпеки\n9:35-10:55 2. Основи кібербезпеки\n11:10-12:30 3. -\n12:45-14:05 4. -\n\nЧетвер:\n8:00-9:20 1. Математичний аналіз\n9:35-10:55 2. Алгебра і теорія чисел\n11:10-12:30 3. Алгебра і теорія чисел\n12:45-14:05 4. Елементарна математика\n\nП'ятниця:\n8:00-9:20 1. Диференціальна геометрія та топологія\n9:35-10:55 2. Диференціальна геометрія та топологія\n11:10-12:30 3. Основи права \n12:45-14:05 4. Основи права"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'КН-26':
                schedule = "Понеділок:\n8:00-9:20 1. Аналіз алгоритмів\n9:35-10:55 2.Аналіз алгоритмів\n11:10-12:30 3. Фізичне виховання\n12:45-14:05 4. Іноземна мова\n\nВівторок:\n8:00-9:20 1. -\n9:35-10:55 2. -\n11:10-12:30 3. Motion-дизайн\n12:45-14:05 4. Motion-дизайн\n\nСереда:\n8:00-9:20 1. Комп'ютерні мережі\n9:35-10:55 2. Комп'ютерні мережі\n11:10-12:30 3. Інструментальтні засоби розробки ігрових додатків\n12:45-14:05 4. Інструментальтні засоби розробки ігрових додатків\n\nЧетвер:\n8:00-9:20 1. -\n9:35-10:55 2. -\n11:10-12:30 3. -\n12:45-14:05 4. -\n\nП'ятниця:\n8:00-9:20 1. Об'єктно-орієнтовне програмування\n9:35-10:55 2. Об'єктно-орієнтовне програмування\n11:10-12:30 3. Наратологія \n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'КН-27':
                schedule = "Понеділок:\n8:00-9:20 1. Економіко-математичні методи та моделі\n9:35-10:55 2. Економіко-математичні методи та моделі\n11:10-12:30 3. Фізичне виховання\n12:45-14:05 4. Іноземна мова\n\nВівторок:\n8:00-9:20 1. Digital-аналітика\n9:35-10:55 2. Digital-аналітика\n11:10-12:30 3. Фінанси, гроші і кредит\n12:45-14:05 4. Фінанси, гроші і кредит\n\nСереда:\n8:00-9:20 1. Комп'ютерні мережі\n9:35-10:55 2. Комп'ютерні мережі\n11:10-12:30 3. Економіко-математичні методи та моделі\n12:45-14:05 4. Економіко-математичні методи та моделі\n\nЧетвер:\n8:00-9:20 1. Комп'ютерна математика\n9:35-10:55 2. Комп'ютерна математика\n11:10-12:30 3. Етика та психологія бізнесу\n12:45-14:05 4. Етика та психологія бізнесу\n\nП'ятниця:\n8:00-9:20 1. Економіка підприємств\n9:35-10:55 2. Економіка підприємств\n11:10-12:30 3. Логістичний аутсорсинг\n12:45-14:05 4. Логістичний аутсорсинг"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'COФІ-31':
                schedule = "Понеділок:\n8:00-9:20 1. -\n9:35-10:55 2. -\n11:10-12:30 3. Загальна фізика\n12:45-14:05 4. Загальна фізика\n\nВівторок:\n8:00-9:20 1. Соціологія\n9:35-10:55 2. МНФ\n11:10-12:30 3. МНФ\n12:45-14:05 4. -\n\nСереда:\n8:00-9:20 1. Чисельні методи\n9:35-10:55 2. Чисельні методи\n11:10-12:30 3. МНФ\n12:45-14:05 4. МНФ\n\nЧетвер:\n8:00-9:20 1. Освітні технології\n9:35-10:55 2. Освітні технології\n11:10-12:30 3. Загальна фізика\n12:45-14:05 4. ПРФЗ\n\nП'ятниця:\n8:00-9:20 1. Теоретична фізика\n9:35-10:55 2. Теоретична фізика\n11:10-12:30 3. Основи сучасної електроніки\n12:45-14:05 4. Основи сучасної електроніки"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'COМІ-32':
                schedule = " Понеділок:\n8:00-9:20 1. Диференціальні рівняння\n9:35-10:55 2.Диференціальні рівняння\n11:10-12:30 3. МНМ\n12:45-14:05 4. МНМ\n\nВівторок:\n8:00-9:20 1. Математична логіка\n9:35-10:55 2. Математична логіка\n11:10-12:30 3. Соціологія\n12:45-14:05 4. Загальна фізика\n\nСереда:\n8:00-9:20 1. Чисельні методи\n9:35-10:55 2. Чисельні методи\n11:10-12:30 3. МНМ\n12:45-14:05 4. Елементарна математика\n\nЧетвер:\n8:00-9:20 1. Освітні технології\n9:35-10:55 2. Функціональний аналіз\n11:10-12:30 3. Функціональний аналіз\n12:45-14:05 4. Освітні технології\n\nП'ятниця:\n8:00-9:20 1. Загальна фізика\n9:35-10:55 2. Загальна фізика\n11:10-12:30 3. Загальна фізика\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'COIM-33':
                schedule = "Понеділок:\n8:00-9:20 1. Методи оптимізації та дослідження операцій\n9:35-10:55 2. Методи оптимізації та дослідження операцій\n11:10-12:30 3. Основи сучасної електроніки\n12:45-14:05 4. Основи сучасної електроніки\n\nВівторок:\n8:00-9:20 1. -\n9:35-10:55 2. Соціологія\n11:10-12:30 3. Математична логіка і теорія алгоритмів\n12:45-14:05 4. Математична логіка і теорія алгоритмів\n\nСереда:\n8:00-9:20 1. -\n9:35-10:55 2. -\n11:10-12:30 3. Методи оптимізації та дослідження операцій\n12:45-14:05 4. Методи оптимізації та дослідження операцій\n\nЧетвер:\n8:00-9:20 1. Освітні технології\n9:35-10:55 2. Адміністрування комп'ютерних мереж\n11:10-12:30 3. Освітні технології\n12:45-14:05 4. Адміністрування комп'ютерних мереж\n\nП'ятниця:\n8:00-9:20 1. Web-програмування\n9:35-10:55 2. Web-програмування\n11:10-12:30 3. -\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'СОФА-35':
                schedule = "Понеділок:\n8:00-9:20 1. Теоретична граматика і теоретична фонетика\n9:35-10:55 2. Методика навчання англійської мови\n11:10-12:30 3. Загальна фізика\n12:45-14:05 4. Загальна фізика\n\nВівторок:\n8:00-9:20 1.Соціологія\n9:35-10:55 2. МНФ\n11:10-12:30 3. МНФ\n12:45-14:05 4. Методика навчання англійської мови\n\nСереда:\n8:00-9:20 1. Лексикологія\n9:35-10:55 2. Лексикологія\n11:10-12:30 3. МНФ\n12:45-14:05 4.МНФ\n\nЧетвер:\n8:00-9:20 1. Освітні технології\n9:35-10:55 2. Освітні технології\n11:10-12:30 3. Загальна фізика\n12:45-14:05 4. ПРФЗ\n\nП'ятниця:\n8:00-9:20 1. Практичний курс англійської мови\n9:35-10:55 2. Практичний курс англійської мови\n11:10-12:30 3. -\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'КН-36':
                schedule = "Понеділок:\n8:00-9:20 1. -\n9:35-10:55 2. Теорія ігор\n11:10-12:30 3. Основи робототехніки\n12:45-14:05 4. Основи робототехніки\n\nВівторок:\n8:00-9:20 1. -\n9:35-10:55 2. -\n11:10-12:30 3. -\n12:45-14:05 4. -\n\nСереда:\n8:00-9:20 1. Правові основи Game-індустрії\n9:35-10:55 2. Правові основи Game-індустрії\n11:10-12:30 3. Технології розробки комп'ютерних ігор\n12:45-14:05 4. Технології розробки комп'ютерних ігор\n\nЧетвер:\n8:00-9:20 1. -\n9:35-10:55 2. Адміністрування комп'ютерних мереж\n11:10-12:30 3. Адміністрування комп'ютерних мереж\n12:45-14:05 4. -\n\nП'ятниця:\n8:00-9:20 1. Web-програмування\n9:35-10:55 2. -\n11:10-12:30 3. Web-програмування\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'мСОФ-11':
                schedule = "Понеділок:\n8:00-9:20 1. Лабораторний практикум з комп'ютерної математики\n9:35-10:55 2. Проєктна практика\n11:10-12:30 3. Методика підготовки учнів до ЗНО з фізики\n12:45-14:05 4. Методика підготовки учнів до ЗНО з фізики\n\nВівторок:\n8:00-9:20 1. -\n9:35-10:55 2. -\n11:10-12:30 3. МНМ\n12:45-14:05 4. МНМ\n14:20-15:40 5. Англійська мова\n\nСереда:\n8:00-9:20 1. -\n9:35-10:55 2. Проєктна практика\n11:10-12:30 3. Фундаментальні фізичні експерименти\n12:45-14:05 4. Фундаментальні фізичні експерименти\n\nЧетвер:\n8:00-9:20 1. -\n9:35-10:55 2. МНФ\n11:10-12:30 3. МНФ\n12:45-14:05 4. Лабораторний практикум з комп'ютерної математики\n14:20-15:40 5. Німецька мова\n\nП'ятниця:\n8:00-9:20 1. -\n9:35-10:55 2. -\n11:10-12:30 3. -\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'мСОМ-12':
                schedule = "Понеділок:\n8:00-9:20 1. Лабораторний практикум з комп'ютерної математики\n9:35-10:55 2. Лабораторний практикум з комп'ютерної математики\n11:10-12:30 3. Вибрані питання вищої математики\n12:45-14:05 4. Вибрані питання вищої математики\n\nВівторок:\n8:00-9:20 1. МНФ\n9:35-10:55 2. МНФ\n11:10-12:30 3. МНФ\n12:45-14:05 4. Англійська мова\n14:20-15:40 5. -\n\nСереда:\n8:00-9:20 1. Нестандартні задачі з математики\n9:35-10:55 2. Нестандартні задачі з математики\n11:10-12:30 3. МНМ\n12:45-14:05 4. МНМ\n\nЧетвер:\n8:00-9:20 1. Новітні досягнення у математиці\n9:35-10:55 2. Новітні досягнення у математиці\n11:10-12:30 3. Проєктна практика\n12:45-14:05 4. Проєктна практика\n14:20-15:40 5. Німецька мова\n\nП'ятниця:\n8:00-9:20 1. -\n9:35-10:55 2. -\n11:10-12:30 3. -\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'мСОІн-13':
                schedule = "Понеділок:\n8:00-9:20 1. Сучасні Web-технології\n9:35-10:55 2. Сучасні Web-технології\n11:10-12:30 3. Вибрані питання вищої математики та математичної статистики\n12:45-14:05 4. Вибрані питання вищої математики та математичної статистики\n\nВівторок:\n8:00-9:20 1. -\n9:35-10:55 2. -\n11:10-12:30 3. Основи хмарних технологій\n12:45-14:05 4. Основи хмарних технологій\n14:20-15:40 5. Англійська мова\n\nСереда:\n8:00-9:20 1. МНІ\n9:35-10:55 2. МНІ\n11:10-12:30 3. Основи робототехніки\n12:45-14:05 4. Основи робототехніки\n\nЧетвер:\n8:00-9:20 1. Вибрані питання вищої математики та математичної статистики\n9:35-10:55 2. Вибрані питання вищої математики та математичної статистики\n11:10-12:30 3. Технології  електронного навчання\n12:45-14:05 4. Технології  електронного навчання\n14:20-15:40 5. Німецька мова\n\nП'ятниця:\n8:00-9:20 1. -\n9:35-10:55 2. -\n11:10-12:30 3. -\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'ФІ-41':
                schedule = "Понеділок:\n8:00-9:20 1. Теоретична фізика\n9:35-10:55 2. Теоретична фізика\n11:10-12:30 3. Захоплююча фізика\n12:45-14:05 4. -\n\nВівторок:\n8:00-9:20 1. -\n9:35-10:55 2. Іноземна мова у фаховій комунікації\n11:10-12:30 3. -\n12:45-14:05 4. -\n\nСереда:\n8:00-9:20 1. Політологія\n9:35-10:55 2. Політологія\n11:10-12:30 3. -\n12:45-14:05 4. -\n\nЧетвер:\n8:00-9:20 1. -\n9:35-10:55 2. МНФ\n11:10-12:30 3. МНФ\n12:45-14:05 4. МНФ\n\nП'ятниця:\n8:00-9:20 1. ПРФЗ\n9:35-10:55 2. ПРФЗ\n11:10-12:30 3. -\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'МІ-42':
                schedule = "Понеділок:\n8:00-9:20 1. Загальна фізика\n9:35-10:55 2. Загальна фізика\n11:10-12:30 3. Аналіз алгоритмів\n12:45-14:05 4. Аналіз алгоритмів\n\nВівторок:\n8:00-9:20 1. -\n9:35-10:55 2. Іноземна мова у фаховій комунікації\n11:10-12:30 3. МНМ\n12:45-14:05 4. МНМ\n\nСереда:\n8:00-9:20 1. Політологія\n9:35-10:55 2. Політологія\n11:10-12:30 3. Проектно-технологічна практика\n12:45-14:05 4. Проектно-технологічна практика\n\nЧетвер:\n8:00-9:20 1. -\n9:35-10:55 2. МНМ\n11:10-12:30 3. МНМ\n12:45-14:05 4. -\n\nП'ятниця:\n8:00-9:20 1. -\n9:35-10:55 2. -\n11:10-12:30 3. -\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'МІ-43':
                schedule = "Понеділок:\n8:00-9:20 1. -\n9:35-10:55 2. -\n11:10-12:30 3. -\n12:45-14:05 4. -\n\nВівторок:\n8:00-9:20 1. -\n9:35-10:55 2. Іноземна мова у фаховій комунікації\n11:10-12:30 3. МНІ\n12:45-14:05 4. МНІ\n\nСереда:\n8:00-9:20 1. Політологія\n9:35-10:55 2. -\n11:10-12:30 3. Політологія\n12:45-14:05 4. -\n\nЧетвер:\n8:00-9:20 1. -\n9:35-10:55 2. -\n11:10-12:30 3. -\n12:45-14:05 4. Проектно-технологічна практика\n14:20-15:40 5. Проектно-технологічна практика \n\nП'ятниця:\n8:00-9:20 1. -\n9:35-10:55 2. Комп'ютерне моделювання\n11:10-12:30 3. Комп'ютерне моделювання\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'СОІнск-24':
                schedule = "Понеділок:\n8:00-9:20 1. -\n9:35-10:55 2. -\n11:10-12:30 3. -\n12:45-14:05 4. -\n\nВівторок:\n8:00-9:20 1. -\n9:35-10:55 2. Іноземна мова у фаховій комунікації\n11:10-12:30 3. МНІ\n12:45-14:05 4. МНІ\n\nСереда:\n8:00-9:20 1. Політологія\n9:35-10:55 2. -\n11:10-12:30 3. Політологія\n12:45-14:05 4. -\n\nЧетвер:\n8:00-9:20 1. -\n9:35-10:55 2. -\n11:10-12:30 3. -\n12:45-14:05 4. Проектно-технологічна практика\n14:20-15:40 5. Проектно-технологічна практика \n\nП'ятниця:\n8:00-9:20 1. -\n9:35-10:55 2. Комп'ютерне моделювання\n11:10-12:30 3. Комп'ютерне моделювання\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)

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
            bot.send_message(message.chat.id, "Введіть нову групу:")
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
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('📜Профіль')
            item2 = types.KeyboardButton('✍️Розклад пар')
            item3 = types.KeyboardButton('Контакти викладачів')
            item4 = types.KeyboardButton('Журнал')
            item5 = types.KeyboardButton('Інформація про розробників')
            item6 = types.KeyboardButton('Домашка')
            markup.add(item1, item2, item3, item4, item5, item6)
            bot.send_message(message.chat.id, "👇".format(message.from_user), reply_markup=markup)


def update_email(message):
    new_email = message.text
    user_id = message.from_user.id

    # Перевірка чи введений email закінчується на "@fizmat.tnpu.edu.ua"
    if new_email.endswith("@fizmat.tnpu.edu.ua"):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE login_id SET email=? WHERE id=?", (new_email, user_id))
        conn.commit()

        conn.close()
        bot.send_message(message.chat.id, "🦦Пошту успішно оновлено!")
    else:
        # Надсилання повідомлення про неправильний формат email
        bot.send_message(message.chat.id,
                         "🙅Введена email адреса не є фізматівською. Будь ласка, введіть ще раз свою email адресу")
        # Повернення до функції get_email для очікування наступного вводу від користувача

        bot.register_next_step_handler(message, update_email)


def update_grypa(message):
    new_grypa = message.text.upper()
    user_id = message.from_user.id
    # Встановлення підключення до бази даних
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Виконання запиту для оновлення групи користувача
    cursor.execute("UPDATE login_id SET grypa=? WHERE id=?", (new_grypa, user_id))
    conn.commit()
    # Відправлення повідомлення з питанням про нове прізвище та ім'я
    bot.send_message(message.chat.id, "🦦Група оновлена успішно!")
    # Закриття підключення до бази даних
    conn.close()


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
