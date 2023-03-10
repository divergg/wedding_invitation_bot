import telebot
from telebot import types
import datetime
import time
from telegram import ParseMode
import os


""" Bot token and bot instance"""

token = os.environ['TOKEN']
bot = telebot.TeleBot(token)

"""Dict with users credentials"""
users = {}




""" Main menu items (after referred as MAIN_ITEMS)"""
item_dict = {
    1: "ЗАГС",
    2: "Дресс-код",
    3: "Цветы",
    4: "Подарки",
    5: "Наш хэштег",
    6: "Печатная версия приглашения",
    7: "Дополнительная информация"
}

"""Dicts fot buttons in menus"""
butt_dict = {}
butt_start_dict = {}


"""Dict with codes for guests"""

codes_dict = os.environ['codes_dict']


"""Dict with urls of invitations"""
photos_url_dict = os.environ['photos_url_dict']

"""Buttons for additional menu"""
additional_dict = {
    1: "Про тосты",
    2: "Контакты",
    3: "Возврат в основное меню",
}

"""Dicts fot buttons in menus"""
add_butt_dict = {}



"""Start command"""
@bot.message_handler(commands=['start'])
def start(message):
    users[message.chat.id] = message.chat.id
    code = bot.send_message(users[message.chat.id], 'Введите, пожалуйста, код, который Вы ранее получили')
    logger(message)
    bot.register_next_step_handler(code, get_code)


"""Check of users code"""
def get_code(message):
    code = message.text
    U = 0
    while (U == 0):
        for i in codes_dict:
            if code == codes_dict[i]:
                U = 1
                inv = open(photos_url_dict[i], 'rb')
                men = bot.send_photo(users[message.chat.id], inv)
                inv.close()
                time.sleep(2)
                logger(message)
                menu(men)
        if (U == 0):
            U = 1
            bot.send_message(users[message.chat.id], 'Кажется, вы ошиблись, попробуйте еще разок (нажмите -> /restart)')
            logger(message)


"""Restart of app in case of an errror in users code"""
@bot.message_handler(commands=['restart'])
def err_code(message):
    code = bot.send_message(users[message.chat.id], 'Введите код повторно')
    logger(message)
    bot.register_next_step_handler(code, get_code)


"""Main menu"""
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in item_dict:
        butt_dict[i] = types.KeyboardButton(item_dict[i])
        markup.add(butt_dict[i])
    reply = bot.send_message(users[message.chat.id], 'Пройдите, пожалуйста, по всем пунктам меню', reply_markup=markup)
    logger(reply)
    # Проверка выбора юзера
    bot.register_next_step_handler(reply, check_message_text)


"""Check users choice in menu"""
def check_message_text(message):
    reply = message.text
    if reply == item_dict[1]:
        reply_2 = bot.send_message(users[message.chat.id], "Планируете ли Вы присутствовать на торжественной церемонии во Дворце бракосочетания?")
        logger(message)
        zags_querry(reply_2)
    elif reply == item_dict[2]:
        clothes(message)
        logger(message)
    elif reply == item_dict[3]:
        flowers(message)
        logger(message)
    elif reply == item_dict[4]:
         gift(message)
         logger(message)
    elif reply == item_dict[5]:
         hashtag(message)
         logger(message)
    elif reply == item_dict[6]:
         reply_2 = bot.send_message(users[message.chat.id], "Хотите ли бы Вы получить распечатанное приглашение?")
         logger(message)
         invite(reply_2)
    elif reply == item_dict[7]:
         ad_info(message)
         logger(message)
    else:
        bot.send_message(users[message.chat.id], 'ОШИБКА')
        logger(message)
        menu(message)


"""Check 1 input in MAIN_ITEMS """
def zags_querry(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("Да")
    markup.add(item1)
    item2 = types.KeyboardButton("Нет")
    markup.add(item2)
    bot.send_message(users[message.chat.id], 'Выберите один вариант ответа', reply_markup=markup)
    logger(message)
    # Проверка выбора юзера по загсу
    bot.register_next_step_handler(message, zags_answer)


""" Check answer """""
def zags_answer(message):
    reply = message.text
    if reply == "Да":
        reply_2 = bot.send_message(users[message.chat.id], 'Ждем Вас во Дворце Бракосочетания №4.\n'
                                                           '<u>Сбор гостей в 14:40</u>', parse_mode=ParseMode.HTML)
        time.sleep(2)
        bot.send_message(users[message.chat.id], 'https://yandex.ru/maps/-/CCUJVUshkD',
                         parse_mode=ParseMode.HTML)
        time.sleep(1)
        logger(message)
    elif reply == "Нет":
        reply_2 = bot.send_message(users[message.chat.id], 'Жаль, что вы не разделите с нами этот момент 😔. \nНо нам будет очень приятно видеть Вас на праздничном фуршете в <u>17:00</u>!',
                                   parse_mode=ParseMode.HTML)
        time.sleep(3)
        bot.send_message(users[message.chat.id], 'https://yandex.ru/maps/-/CCUJVUgHdB',
                         parse_mode=ParseMode.HTML)
        time.sleep(1)
        logger(message)
    else:
        bot.send_message(users[message.chat.id], 'ОШИБКА')
        logger(message)
        zags_querry(message)
    menu(reply_2)

"""2 input in MAIN_ITEMS """
def clothes(message):
    CLOTHES = open("Clothes.png", 'rb')
    bot.send_photo(users[message.chat.id], CLOTHES)
    CLOTHES.close()
    time.sleep(2)
    menu(message)


"""Check 3 input in MAIN_ITEMS"""
def flowers(message):
    bot.send_message(users[message.chat.id],
                     "Мы очень любим цветы и считаем, что они должны быть украшением нашего праздника 🌸. "
                     "\n\nК сожалению, срезанные цветы мы не сможем обеспечить необходимым количеством воды.\n\nПоэтому будем очень рады, если Вы отдадите предпочтение небольшой композиции во флористической губке "
                     "таких вариантов:")
    Flower_1 = open("Flower_1.jpg", 'rb')
    Flower_2 = open("Flower_2.jpg", 'rb')
    Flower_3 = open("Flower_3.jpg", 'rb')
    time.sleep(8)
    bot.send_photo(users[message.chat.id], Flower_1, "В коробке")
    time.sleep(1)
    bot.send_photo(users[message.chat.id], Flower_2, "В деревянном ящике")
    time.sleep(1)
    bot.send_photo(users[message.chat.id], Flower_3, "В плайм-пакете")
    Flower_1.close()
    Flower_2.close()
    Flower_3.close()
    time.sleep(1)
    menu(message)



"""Check 4 input in MAIN_ITEMS"""
def gift(message):
    bot.send_message(users[message.chat.id], "Мы не хотим утруждать Вас выбором подарка, поэтому будем рады Вашему вкладу в бюджет нашей молодой семьи ✨")
    time.sleep(3)
    bot.send_sticker(users[message.chat.id], sticker='CAACAgIAAxkBAAIEk2KnSkDQhFI_q81Ee23WXsWY4veHAAIDAQACVp29CgLl0XiH5fpPJAQ')
    time.sleep(1)
    menu(message)


"""Check 5 input in MAIN_ITEMS"""
def hashtag(message):
    bot.send_message(users[message.chat.id], "При публикации фотографий в социальных сетях используйте хэштег #взрослыйвопрос🙈.\nДа, именно с обезьянкой)", parse_mode=ParseMode.HTML)
    time.sleep(2)
    menu(message)


"""Check 6 input in MAIN_ITEMS"""
def invite (message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("Да")
    markup.add(item1)
    item2 = types.KeyboardButton("Нет")
    markup.add(item2)
    bot.send_message(users[message.chat.id], 'Выберите один вариант ответа', reply_markup=markup)
    logger(message)
    # Проверка выбора юзера по приглашению
    bot.register_next_step_handler(message, invite_answer)



"""Answer on 6 input in MAIN_ITEMS"""
def invite_answer(message):
    reply = message.text
    if reply == "Да":
        reply_2 = bot.send_message(users[message.chat.id], 'При первой встрече мы его Вам вручим 💌')
        time.sleep(1)
        logger(message)
    elif reply == "Нет":
        reply_2 = bot.send_message(users[message.chat.id], 'Рады, что вы бережете экологию 🌎.\n'
                                                           'Но обязательно сохраните электронную версию приглашения\n'
                                                           '(обратитесь к @anstsili за открыткой в хорошем качестве)')
        time.sleep(3)
        logger(message)
    else:
        bot.send_message(users[message.chat.id], 'ОШИБКА')
        logger(message)
        invite(message)
    menu(reply_2)



"""Check 7 input in MAIN_ITEMS"""
""" Additional info"""
def ad_info(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in additional_dict:
        add_butt_dict[i] = types.KeyboardButton(additional_dict[i])
        markup.add(add_butt_dict[i])
    reply = bot.send_message(users[message.chat.id], 'Выберите, пожалуйста, пункт', reply_markup=markup)
    # Проверка выбора юзера
    bot.register_next_step_handler(reply, check_ad_info)


"""Check additional info dict choice"""
def check_ad_info(message):
    reply = message.text
    if reply == additional_dict[1]:
        bot.send_message(users[message.chat.id], "https://www.psychologies.ru/wellbeing/pozdravlenie-na-svadbe-chto-i-kak-govorit-molodozhenam")
        time.sleep(1.5)
        bot.send_message(users[message.chat.id], "🥂")
        time.sleep(1.5)
        logger(message)
        ad_info(message)
    elif reply == additional_dict[2]:
        bot.send_message(users[message.chat.id], "По всем вопросам обращайтесь к @anstsili 🤗.\n\nВ том числе за помощью в выборе нарядов нашей цветовой палитры "
                                                 "👗(уже нашла десятки магазинов)")
        time.sleep(1.5)
        logger(message)
        ad_info(message)
    else:
        logger(message)
        menu(message)

"""Message logging"""
def logger(message):
    dtn = datetime.datetime.now()
    botlogfile = open('TestBot.log', 'a')
    print(dtn.strftime("%d-%m-%Y %H:%M"), 'Пользователь ' + message.from_user.first_name, message.from_user.id,
          'написал следующее: ' + str(message.text), file=botlogfile)
    botlogfile.close()


# Запускаем бота
while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except:
        continue





