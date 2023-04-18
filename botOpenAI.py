import telebot
import sqlite3
from telebot import types



# Отримання API ключів для Telegram та OpenAI
TELEGRAM_API_KEY = '5646599316:AAFVGWqEAgPmlvpUByhFwmbDjB-1UFY7LWY'
OPENAI_API_KEY = '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'

bot = telebot.TeleBot(TELEGRAM_API_KEY)

def get_user_data(user_id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT grypa, email, first_last FROM login_id WHERE id = {user_id}")
    data = cursor.fetchone()
    connect.close()
    return data





# Функції, для редагування профілю



@bot.message_handler(commands=['start'])
def start(message: types.Message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        grypa TEXT NOT NULL,
        first_last TEXT NOT NULL)""")

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

    # Перевірка чи введений email закінчується на "@fizmat.tnpu.edu.ua"
    if email.endswith("@fizmat.tnpu.edu.ua"):
        # Запит групи
        bot.send_message(message.chat.id, "Будь ласка, введіть свою групу:\nназву групи вводьте на українській мові)")
        bot.register_next_step_handler(message, get_group, email)
    else:
        # Надсилання повідомлення про неправильний формат email
        bot.send_message(message.chat.id, "Введена email адреса не є фізматівською. Будь ласка, введіть правильну email адресу, закінчуєму на '@fizmat.tnpu.edu.ua'.")
        # Повернення до функції get_email для очікування наступного вводу від користувача
        bot.register_next_step_handler(message, get_email)
def get_group(message: types.Message, email):
    group = message.text.upper()

    # Запит імені та прізвища
    bot.send_message(message.chat.id, "Будь ласка, введіть своє ім'я та прізвище:")
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

    bot.send_message(message.chat.id, f"Ти, {message.chat.username} успішно зареєстрований(-на)!")
@bot.message_handler(commands=['functions'])
def message_handler_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('📜Профіль')
    item2 = types.KeyboardButton('✍️Розклад пар')
    item3 = types.KeyboardButton('Контакти викладачів')
    item4 = types.KeyboardButton('Аудиторії')
    item5 = types.KeyboardButton('Інформація про розробників')
    markup.add(item1, item2,item3, item4, item5)
    bot.send_message(message.chat.id, "👇".format(message.from_user), reply_markup=markup)
@bot.message_handler(commands=['homework'])
def message_handler_homework(message):
    homework = ""
    def save_homework(message):
        nonlocal homework
        homework = message.text
        bot.send_message(message.chat.id, f"✅ Домашнє завдання збережено: {homework}")
        user_grypa = None
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT grypa FROM login_id WHERE id = ?", (message.from_user.id,))
            user_grypa = cursor.fetchone()[0]
        if user_grypa is not None:
            with sqlite3.connect('users.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM login_id WHERE grypa = ?", (user_grypa,))
                rows = cursor.fetchall()
                for row in rows:
                    bot.send_message(row[0], f"📚 Домашнє завдання: {homework} \n(Надіслано від @{message.chat.username} )")

    # Виклик функції для запиту домашнього завдання
    msg = bot.send_message(message.chat.id, "📚 Домашнє завдання - Будь ласка, напиши домашнє завдання, яке задали вашій групі. Наступне твоє повідомлення буде надіслано усім твоїм одногрупникам 😉\nТому дивися, що пишеш це всі побачать)")
    bot.register_next_step_handler(msg, save_homework)



@bot.message_handler(commands=['support'])
def message_handler_support(message):    # Відправка автоматичного повідомлення користувачу
    bot.send_message(message.chat.id, 'пішов нахуй Степан')
    bot.send_message(628446966, f'Користувач звернувся за допомогою:\nАйді: {message.chat.id}\nНік: {message.chat.username}\nТекст: {message.text}')

@bot.message_handler(commands=['yura'])
def _yura(message):
    # Відправлення повідомлення
    bot.send_message(message.chat.id, "Найсексуальніший чоловік на цій планеті")

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Інформація про розробників':
            bot.send_message(message.chat.id, 'Засновник @yura_krykh\nВведіть команду /support якшо виникли проблеми')
        elif message.text == '✍️Розклад пар':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            COFI_11 = types.KeyboardButton('COФІ-11')
            COFA_12 = types.KeyboardButton('COФA-12')
            COMI_13 = types.KeyboardButton('COMI-13')
            KH_14   = types.KeyboardButton('КН-14')
            COIM_15 = types.KeyboardButton('COІМ-15')
            IIP_16  = types.KeyboardButton('ІІП-16')
            DA_17   = types.KeyboardButton('DA-17')
            COFI_21 = types.KeyboardButton('COФІ-21')
            COMI_22 = types.KeyboardButton('COMI-22')
            COIM_23 = types.KeyboardButton('COIM-23')
            COFA_25 = types.KeyboardButton('СОФА-25')
            KH_26   = types.KeyboardButton('КН-26')
            KH_27   = types.KeyboardButton('КН-27')
            COFI_31 = types.KeyboardButton('COФІ-31')
            COIM_32 = types.KeyboardButton('COIM-32')
            COIM_33 = types.KeyboardButton('COIM-33')
            COFA_35 = types.KeyboardButton('СОФА-35')
            KH_36   = types.KeyboardButton('КН-36')
            back    = types.KeyboardButton('🔙Назад')
            markup.add(back,COFI_11,COFA_12,COMI_13,KH_14,COIM_15,IIP_16,DA_17,COFI_21,COMI_22,COIM_23, COFA_25, KH_26,KH_27,COFI_31,COIM_32,COIM_33,COFA_35,KH_36)
            bot.send_message(message.chat.id, 'Виберіть вашу групу:', reply_markup = markup)
        elif message.text in ['COIM-23', 'СОФА-25','COФІ-11','COФA-12','COMI-13','КН-14','COІМ-15','ІІП-16','DA-17','COФІ-21','COФІ-21','COMI-22','КН-26','КН-27','COФІ-31','COIM-32','COIM-33','СОФА-35','КН-36']:
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
            elif group == 'КН-14':
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
            elif group == 'COIM-32':
                schedule = " Понеділок:\n8:00-9:20 1. Диференціальні рівняння\n9:35-10:55 2.Диференціальні рівняння\n11:10-12:30 3. МНМ\n12:45-14:05 4. МНМ\n\nВівторок:\n8:00-9:20 1. Математична логіка\n9:35-10:55 2. Математична логіка\n11:10-12:30 3. Соціологія\n12:45-14:05 4. Загальна фізика\n\nСереда:\n8:00-9:20 1. Чисельні методи\n9:35-10:55 2. Чисельні методи\n11:10-12:30 3. МНМ\n12:45-14:05 4. Елементарна математика\n\nЧетвер:\n8:00-9:20 1. Освітні технології\n9:35-10:55 2. Функціональний аналіз\n11:10-12:30 3. Функціональний аналіз\n12:45-14:05 4. Освітні технології\n\nП'ятниця:\n8:00-9:20 1. Загальна фізика\n9:35-10:55 2. Загальна фізика\n11:10-12:30 3. Загальна фізика\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'COIM-33':
                schedule = "Понеділок:\n8:00-9:20 1. Методи оптимізації та дослідження операцій\n9:35-10:55 2. Методи оптимізації та дослідження операцій\n11:10-12:30 3. Основи сучасної електроніки\n12:45-14:05 4. Основи сучасної електроніки\n\nВівторок:\n8:00-9:20 1. -\n9:35-10:55 2. Соціологія\n11:10-12:30 3. Математична логіка і теорія алгоритмів\n12:45-14:05 4. Математична логіка і теорія алгоритмів\n\nСереда:\n8:00-9:20 1. -\n9:35-10:55 2. -\n11:10-12:30 3. Методи оптимізації та дослідження операцій\n12:45-14:05 4. Методи оптимізації та дослідження операцій\n\nЧетвер:\n8:00-9:20 1. Освітні технології\n9:35-10:55 2. Адміністрування комп'ютерних мереж\n11:10-12:30 3. Освітні технології\n12:45-14:05 4. Адміністрування комп'ютерних мереж\n\nП'ятниця:\n8:00-9:20 1. Web-програмування\n9:35-10:55 2. Web-програмування\n11:10-12:30 3. -\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'СОФА-35':
                schedule = "Понеділок:\n8:00-9:20 1. Теоретична граматика і теоретична фонетика\n9:35-10:55 2. Методика навчання англійської мови\n11:10-12:30 3. Загальна фізика\n12:45-14:05 4. Загальна фізика\n\nВівторок:\n8:00-9:20 1.Соціологія\n9:35-10:55 2. МНФ\n11:10-12:30 3. МНФ\n12:45-14:05 4. Методика навчання англійської мови\n\nСереда:\n8:00-9:20 1. Лексикологія\n9:35-10:55 2. Лексикологія\n11:10-12:30 3. МНФ\n12:45-14:05 4.МНФ\n\nЧетвер:\n8:00-9:20 1. Освітні технології\n9:35-10:55 2. Освітні технології\n11:10-12:30 3. Загальна фізика\n12:45-14:05 4. ПРФЗ\n\nП'ятниця:\n8:00-9:20 1. Практичний курс англійської мови\n9:35-10:55 2. Практичний курс англійської мови\n11:10-12:30 3. -\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
            elif group == 'КН-36':
                schedule ="Понеділок:\n8:00-9:20 1. -\n9:35-10:55 2. Теорія ігор\n11:10-12:30 3. Основи робототехніки\n12:45-14:05 4. Основи робототехніки\n\nВівторок:\n8:00-9:20 1. -\n9:35-10:55 2. -\n11:10-12:30 3. -\n12:45-14:05 4. -\n\nСереда:\n8:00-9:20 1. Правові основи Game-індустрії\n9:35-10:55 2. Правові основи Game-індустрії\n11:10-12:30 3. Технології розробки комп'ютерних ігор\n12:45-14:05 4. Технології розробки комп'ютерних ігор\n\nЧетвер:\n8:00-9:20 1. -\n9:35-10:55 2. Адміністрування комп'ютерних мереж\n11:10-12:30 3. Адміністрування комп'ютерних мереж\n12:45-14:05 4. -\n\nП'ятниця:\n8:00-9:20 1. Web-програмування\n9:35-10:55 2. -\n11:10-12:30 3. Web-програмування\n12:45-14:05 4. -"
                bot.send_message(message.chat.id, 'Розклад пар для групи ' + group + ':\n\n' + schedule)
        elif message.text == '📜Профіль':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            update_profile = types.KeyboardButton('🔧Редагувати профіль')
            back = types.KeyboardButton('🔙Назад')
            markup.add(update_profile,back)
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
            up_email =  types.KeyboardButton('🛠📨Email')
            up_grypa = types.KeyboardButton('🛠👥Групу')
            up_firstlast = types.KeyboardButton("🛠🪪ПІБ")
            back = types.KeyboardButton('📜Профіль')
            markup.add(up_email, up_grypa, up_firstlast,back)
            bot.send_message(message.chat.id, "Виберіть, що саме хочете редагувати?🧐", reply_markup=markup)



        elif message.text == '🛠📨Email':

            bot.send_message(message.chat.id, "Введіть фізматівську пошту:")
            bot.register_next_step_handler(message, update_email)



        elif message.text == '🛠👥Групу':
            bot.send_message(message.chat.id, "Введіть нову групу:")
            bot.register_next_step_handler(message, update_grypa)



        elif message.text == "🛠🪪ПІБ":
            bot.send_message(message.chat.id, "Введіть нове прізвище та ім'я:")
            bot.register_next_step_handler(message, update_first_last)










        elif message.text == 'Аудиторії':
            bot.send_message(message.chat.id, "Ця функція покищо недоступна")
        elif message.text == 'Контакти викладачів':
            bot.send_message(message.chat.id, "Ця функція покищо недоступна")






        elif message.text == '🔙Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('📜Профіль')
            item2 = types.KeyboardButton('✍️Розклад пар')
            item3 = types.KeyboardButton('Контакти викладачів')
            item4 = types.KeyboardButton('Аудиторії')
            item5 = types.KeyboardButton('Інформація про розробників')
            markup.add(item1, item2, item3, item4, item5)
            bot.send_message(message.chat.id, "👇".format(message.from_user), reply_markup=markup)




        elif message.text == 'Аудиторії':
            bot.send_message(message.chat.id, "ця функція покищо недоступна")
        elif message.text == 'Контакти викладачів':
            bot.send_message(message.chat.id, "ця функція покищо недоступна")



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
        bot.send_message(message.chat.id, "🙅Введена email адреса не є фізматівською. Будь ласка, введіть ще раз свою email адресу")
        # Повернення до функції get_email для очікування наступного вводу від користувача

        bot.register_next_step_handler(message,update_email)

# Функція для обробки наступного кроку - оновлення групи
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




