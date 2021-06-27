import json
import datetime
from collections import defaultdict
from copy import deepcopy
from math import sin, cos, sqrt, atan2, radians
import telebot


MY_TOKEN = 'token'
USER_FTT_ID = 278119967
START, ADD_NAME, ADD_POS, ADD_PHOTO, LIST_LOC = range(5)

LOCATION_TEMPLATE = {'name': '', 'lat': 0, 'lon': 0, 'photo_exists': False, 'photo': None}
USER_STATE = defaultdict(lambda: START)
LOCATIONS = defaultdict(lambda: [])
NEW_LOCATION = defaultdict(lambda: deepcopy(LOCATION_TEMPLATE))

NO_PHOTO = f"Без фото"
HELP_STRING = f'Этот бот позволяет сохранять список локаций и просматривать их.\nОтправьте /add и следуйте указаниям,' \
              f'чтобы добавить новую локацию.\nОтправьте /list, чтобы посмотреть список сохраненных локаций.\n' \
              f'Отправьте /reset, чтобы удалить все сохраненные локации.\nОтправьте Вашу текущую локацию, чтобы ' \
              f'получить список сохраненных локаций в радиусе 500 метров.'

EMOJI = {
    "CORRECT": u'\U00002705',
    "INCORRECT": u'\U0000274C',
    "MESSAGE_IN": u'\U00002709',
    "MESSAGE_OUT": u'\U000021AA',
    "NAME_ICON": u'\U0000262A',
    "STAT": u'\U0001F4CA',
    "PROFILE": u'\U0001F464',
    "LEVEL": u'\U0001F530',
    "EXPERIENCE": u'\U0001F4A0',
    "ENERGY": u'\U000026A1',
    "COINS": u'\U0001F4B0',
    "TEST_PROGRESS": u'\U0001F518',
    "CERTIFICATE": u'\U0001F4C3',
    "TESTS": u'\U0001F4DD',
    "BOOKS": u'\U0001F4DA',
    "MODULE": u'\U000024C2',
    "SHOP": u'\U0001F3EC',
    "HELP": u'\U00002754',
    "EXIT": u'\U0000274E',
}

keyboard_hider = telebot.types.ReplyKeyboardRemove()
bot = telebot.TeleBot(MY_TOKEN, threaded=False)


# ======================================== 1. Чтение и запись данных
def save_data():
    try:
        with open('saved_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(LOCATIONS, json_file, ensure_ascii=False)
    except BaseException:
        pass


def load_data():
    global LOCATIONS
    try:
        with open('saved_data.json', encoding='utf-8') as json_file:
            loaded_locations = json.load(json_file)
            for k, v in loaded_locations.items():
                LOCATIONS[int(k)] = v
        print("now ", LOCATIONS)
    except FileNotFoundError:
        pass


# ======================================== 2. Вспомогательные функции
def is_nearby(lat1, lon1, lat2, lon2, d):
    return get_distance(lat1, lon1, lat2, lon2) <= d


def get_distance(lat1, lon1, lat2, lon2):
    r = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = r * c
    return distance


def generate_markup(arr: list):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    for element in arr:
        markup.add(element)
    return markup


def get_state(message):
    return USER_STATE[message.chat.id]


def update_state(message, state):
    USER_STATE[message.chat.id] = state


# ======================================== 3. Логирование
def log_to_ftt_in(message, message_type='text'):
    if message.from_user.id != USER_FTT_ID:
        user_nick = message.from_user.username
        dt = datetime.datetime.fromtimestamp(int(message.date)).strftime('%Y-%m-%d %H:%M:%S')
        emoji = EMOJI["MESSAGE_IN"]
        if message_type == 'text':
            log_text = f"{emoji} {dt}\n{message.from_user.id} (@{user_nick}) send message\n>>>>>>>>>>>>>>>>>>>>\n{message.text}"
            bot.send_message(USER_FTT_ID, text=log_text)
        elif message_type == 'location':
            log_text = f"{emoji} {dt}\n{message.from_user.id} (@{user_nick}) send location\n>>>>>>>>>>>>>>>>>>>>\n{message.location.latitude}, {message.location.longitude}"
            bot.send_message(USER_FTT_ID, text=log_text)
        elif message_type == 'photo':
            log_text = f"{emoji} {dt}\n{message.from_user.id} (@{user_nick}) send photo\n>>>>>>>>>>>>>>>>>>>>\n"
            file_id = message.photo[-1].file_id
            bot.send_photo(USER_FTT_ID, photo=file_id, caption=log_text)


def log_to_ftt_out(user_id: int, send_text: str):
    if user_id != USER_FTT_ID:
        dt = datetime.datetime.fromtimestamp(int(datetime.datetime.now().timestamp())).strftime('%Y-%m-%d %H:%M:%S')
        emoji = EMOJI["MESSAGE_OUT"]
        log_text = f"{emoji} {dt}\nREPLY TO {user_id}:\n{send_text}"
        bot.send_message(USER_FTT_ID, text=log_text)


def send_message_from_bot(chat_id: int, text: str, reply_markup=None):
    user_id, send_text, markup = chat_id, text, reply_markup
    log_to_ftt_out(user_id, send_text)
    #if user_id == 438483608:
    #    return
    if not markup:
        bot.send_message(user_id, text=send_text)
    else:
        bot.send_message(user_id, text=send_text, reply_markup=markup)


# ======================================== 4. Main
@bot.message_handler(commands=['help'])
def handle_message_start(message):
    log_to_ftt_in(message)
    send_message_from_bot(chat_id=message.chat.id, text=HELP_STRING)
    update_state(message, START)


@bot.message_handler(func=lambda message: get_state(message) in [START, LIST_LOC], commands=['start', 'add', 'reset'])
def handle_message_start(message):
    log_to_ftt_in(message)
    if message.text == '/start':
        send_message_from_bot(chat_id=message.chat.id, text=f'Приветствую! Для добавления новой локации отправьте /add. Для получения справки отправьте /help')
        update_state(message, START)
    elif message.text == '/add':
        send_message_from_bot(chat_id=message.chat.id, text=f'Добавление новой локации')
        send_message_from_bot(chat_id=message.chat.id, text=f'Введите название')
        update_state(message, ADD_NAME)
    elif message.text == '/reset':
        LOCATIONS[message.chat.id] = []
        send_message_from_bot(chat_id=message.chat.id, text=f'Все локации удалены')
        save_data()


@bot.message_handler(func=lambda message: get_state(message) == ADD_NAME, content_types=['text'])
def handle_message_add_name(message):
    log_to_ftt_in(message)
    NEW_LOCATION[message.chat.id]['name'] = message.text
    send_message_from_bot(chat_id=message.chat.id, text=f'Теперь отправьте геопозицию, чтобы сохранить координаты (только с моб. приложения: нажмите на скрепку и выберите геоданные)')
    update_state(message, ADD_POS)


@bot.message_handler(func=lambda message: get_state(message) == ADD_POS, content_types=['location'])
def handle_message_add_pos(message):
    log_to_ftt_in(message, message_type='location')
    keyboard = generate_markup([NO_PHOTO])
    lat, lon = message.location.latitude, message.location.longitude
    NEW_LOCATION[message.chat.id]['lat'], NEW_LOCATION[message.chat.id]['lon'] = lat, lon
    send_message_from_bot(chat_id=message.chat.id, text=f'Полученные координаты: {lat}, {lon}')
    send_message_from_bot(
        chat_id=message.chat.id, text=f'Отправьте фотографию или нажмите "{NO_PHOTO}"', reply_markup=keyboard)
    update_state(message, ADD_PHOTO)


@bot.message_handler(func=lambda message: get_state(message) == ADD_PHOTO, content_types=['text'])
def handle_no_photo_message(message):
    log_to_ftt_in(message)
    if message.text == NO_PHOTO:
        NEW_LOCATION[message.chat.id]['photo_exists'] = False
        NEW_LOCATION[message.chat.id]['photo'] = None
        LOCATIONS[message.chat.id].append(NEW_LOCATION[message.chat.id])
        NEW_LOCATION[message.chat.id] = deepcopy(LOCATION_TEMPLATE)

        send_message_from_bot(chat_id=message.chat.id, text=f'Локация сохранена (без фото)', reply_markup=keyboard_hider)
        send_message_from_bot(chat_id=message.chat.id, text=f'Всего сохраненных локаций: {len(LOCATIONS[message.chat.id])}', reply_markup=keyboard_hider)
        update_state(message, START)
        print(LOCATIONS)
        save_data()


@bot.message_handler(func=lambda message: get_state(message) == ADD_PHOTO, content_types=['photo'])
def handle_photo(message):
    log_to_ftt_in(message, message_type='photo')
    file_id = message.photo[-1].file_id
    NEW_LOCATION[message.chat.id]['photo_exists'] = True
    NEW_LOCATION[message.chat.id]['photo'] = file_id
    LOCATIONS[message.chat.id].append(NEW_LOCATION[message.chat.id])
    NEW_LOCATION[message.chat.id] = deepcopy(LOCATION_TEMPLATE)

    send_message_from_bot(chat_id=message.chat.id, text=f'Локация сохранена', reply_markup=keyboard_hider)
    send_message_from_bot(chat_id=message.chat.id, text=f'Всего сохраненных локаций: {len(LOCATIONS[message.chat.id])}', reply_markup=keyboard_hider)
    update_state(message, START)
    print(LOCATIONS)
    save_data()


@bot.message_handler(commands=['list'])
def handle_message_start(message):
    log_to_ftt_in(message)
    loc_count = len(LOCATIONS[message.chat.id])
    if loc_count == 0:
        send_message = f"Нет сохраненных локаций"
    else:
        send_message = f"Всего сохраненных локаций: {loc_count}\n\n\n"
        for i, location in enumerate(LOCATIONS[message.chat.id][-1: -11: -1]):
            send_message += f"{i + 1}. {location['name']}\nКоординаты: {location['lat']}, {location['lon']}"
            if location['photo_exists']:
                send_message += " (есть фото)"
            send_message += "\n\n"
        send_message += "Чтобы открыть фотографию локации, отправьте ее номер"
        update_state(message, LIST_LOC)
    send_message_from_bot(chat_id=message.chat.id, text=send_message, reply_markup=keyboard_hider)


@bot.message_handler(func=lambda message: get_state(message) == LIST_LOC, content_types=['text'])
def handle_get_photo_by_id(message):
    log_to_ftt_in(message)
    try:
        loc_id = -int(message.text)
        file_id = LOCATIONS[message.chat.id][loc_id]['photo']
        loc_name = LOCATIONS[message.chat.id][loc_id]['name']
        if file_id:
            bot.send_photo(message.chat.id, photo=file_id, caption=loc_name)
        else:
            send_message_from_bot(chat_id=message.chat.id, text="Нет фото к локации с таким номером")
    except:
        send_message = f'Неверная команда. Отправьте /help для получения справки'
        send_message_from_bot(chat_id=message.chat.id, text=send_message)


@bot.message_handler(func=lambda message: get_state(message) in [START, LIST_LOC], content_types=['location'])
def handle_current_location(message):
    log_to_ftt_in(message, message_type='location')
    lat, lon = message.location.latitude, message.location.longitude
    loc_count = len(LOCATIONS[message.chat.id])
    loc_nearby = 0
    if loc_count == 0:
        send_message = f"Нет сохраненных локаций"
    else:
        send_message = ''
        for i, location in enumerate(LOCATIONS[message.chat.id][-1: -loc_count - 1: -1]):
            if is_nearby(lat, lon, location['lat'], location['lon'], 0.5):
                dist = get_distance(lat, lon, location['lat'], location['lon'])
                dist = str(int(dist * 1000))
                send_message += f"{i + 1}. {location['name']} - в {dist}м от Вас.\nКоординаты: {location['lat']}, {location['lon']}"
                if location['photo_exists']:
                    send_message += " (есть фото)"
                send_message += "\n\n"
                loc_nearby += 1
        send_message = f"Всего сохраненных локаций: {loc_count}. Из них поблизости: {loc_nearby}\n\n\n" + send_message
        send_message += "Чтобы открыть фотографию локации, отправьте ее номер"
    send_message_from_bot(chat_id=message.chat.id, text=send_message, reply_markup=keyboard_hider)
    update_state(message, LIST_LOC)


@bot.message_handler(content_types=['text'])
def handle_random_message(message):
    log_to_ftt_in(message, message_type='text')
    send_message = f'Неверная команда. Отправьте /help для получения справки'
    send_message_from_bot(chat_id=message.chat.id, text=send_message)


@bot.message_handler(content_types=['photo'])
def handle_random_message(message):
    log_to_ftt_in(message, message_type='photo')
    send_message = f'Неверная команда. Отправьте /help для получения справки'
    send_message_from_bot(chat_id=message.chat.id, text=send_message)


load_data()
try:
    bot.polling()
except telebot.apihelper.ApiException:
    pass


