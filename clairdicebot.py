#!/usr/bin/python3.7
import telebot
import re
import random
from token_name import token
from path_buttons import *

bot = telebot.TeleBot(token)


class MyError(Exception):
    def __init__(self, code, chat_id):
        if code == 'NoRollNumber':
            self.txt = 'Напишите сколько кубов кидать!'
        elif code == 'ZeroNum':
            self.txt = 'Количество кубов или сложность не должны быть нулевыми!'
        elif code == 'NoMod':
            self.txt = 'Напишите модификатор!'
        elif code == 'NoDate':
            self.txt = 'Неверно введена дата!'
        elif code == 'HungerNum':
            self.txt = 'Бросайте 1 или 2 кубика голода'
        self.chat_id = chat_id

@bot.message_handler(commands=['start'])
def send_start(message):
    bot.send_message(message.chat.id, "Hello, " + message.from_user.first_name)


@bot.message_handler(commands=['help'])
def send_help(message):
    mtext = 'Иcпользуйте одну из команд: /r, /roll, /dice\n' \
            + 'Через пробел введите количество кубиков, сложность, комментарий\n' \
            + 'Если нужен кубик не d10, напишите: /r 5d6\n' \
            + 'Пример:\n /r 10 6 Джен Эллиот стреляет в голову\n' \
            + 'Для бросков без вычитания единиц: /soak, /dmg, /s, /d\n' \
            + 'Для бросков со специализацией(удвоение 10): /spec, /w, /sp'
    bot.send_message(message.chat.id, mtext)


def roll_dices(dice_count, typedice):
    dice_count = int(dice_count)
    typedice = int(typedice)
    t = []
    for i in range(dice_count):
        t.append(random.randint(1, typedice))
    t.sort()
    return t


def count_success(roll_list, diff, one=True, spec=False, legendary=False):
    if not diff:
        diff = 6
    suc = 0
    ones = roll_list.count(1)
    ten = roll_list.count(10)

    for result in roll_list:
        if result >= diff:
            suc += 1
    if one:
        suc = suc - ones

    if spec:
        suc = suc + ten 

    if legendary:
        nine = roll_list.count(9)
        eight = roll_list.count(8)
        suc = suc + ten + nine + eight

    return suc

def hunger_parse(m):
    for t in m:
        if local_match('[h][1-5]', t):
            h = int(t.split('h')[1])
            m.remove(t)
            return m, h
    return  m, False


def message_parse(msg):
    type = 10
    diff = False
    hunger = False
    comment = ''
    m = msg.text.split()
    if len(m) < 2:
        raise MyError('NoRollNumber', msg.chat.id)
    
    m, hunger = hunger_parse(m)

    if local_match('[0-9]+[d][0-9]+', m[1]):
        type = int(m[1].split('d')[1])
        dice_count = int(m[1].split('d')[0])
    else:
        if not m[1].isdigit():
            raise MyError('NoRollNumber', msg.chat.id)
        elif m[1] == '0':
            raise MyError('ZeroNum', msg.chat.id)
        else:
            dice_count = int(m[1])

    if len(m) > 2:
        if m[2].isdigit():
            if m[2] == '0':
                raise MyError('ZeroNum', msg.chat.id)
            else:
                diff = int(m[2])
                if len(m) > 3:
                    comment = ' '.join(m[3:])
        else:
            comment = ' '.join(m[2:])
    return dice_count, type, diff, hunger, comment


def form_text(dices, res, diff, comment):
    dices = [str(d) for d in dices]

    if not diff:
        return ' '.join(dices) + ' ' + comment
    if res < 0:
        mess_text = ' '.join(dices) + ' ' + comment + '\n' + 'Упс! Это БОТЧ!'
    else:
        mess_text = ' '.join(dices) + ' ' + comment + '\n' + str(res) + ' успехов по сложности ' + str(diff)
    return mess_text

def form_text_hunger(dices, res, diff, hunger, comment):

    if not diff:
        diff = 6

    if hunger > len(dices):
        hunger = len(dices)
    
    hd = random.sample(dices, hunger)
    hd.sort()
    
    dices = [str(d) for d in dices]
    hd = [str(d) for d in hd]

    if res < 0:
        mess_text = ' '.join(dices) + ' {}\nУпс! Это БОТЧ! \nHunger dices: {}'.format(comment, ' '.join(hd))
        if '1' in hd:
            mess_text += '\nКровавый провал!'
    else:
        mess_text = ' '.join(dices) + ' {} \n{} успехов по сложности {}\nHunger dices: {}'.format(comment,str(res), str(diff), ' '.join(hd)) 
        if ('10' in hd) and (res > 0):
            mess_text += '\nКровавый триумф!'

    return mess_text


@bot.message_handler(commands=['dmg', 'soak', 's', 'd'])
def roll_dam(message):
    try:
        dice_count, type, diff, hunger, comment = message_parse(message)
        dices = roll_dices(dice_count, type)
        if not diff:
            diff = 6
        res = count_success(dices, diff, one=False)
        mess_text = form_text(dices, res, diff, comment)
        bot.send_message(message.chat.id,
                         message.from_user.first_name + ' rolled:\n' + mess_text)
    except MyError as e:
        bot.send_message(e.chat_id, e.txt)
    except Exception as e:
        bot.send_message(message.chat.id, 'ooooops')


@bot.message_handler(commands=['r', 'roll', 'dice'])
def roll(message):
    try:
        dice_count, type, diff, hunger, comment = message_parse(message)

        dices = roll_dices(dice_count, type)
        res = count_success(dices, diff)
        if hunger:
            mess_text = form_text_hunger(dices, res, diff, hunger, comment)
        else:
            mess_text = form_text(dices, res, diff, comment)
        bot.send_message(message.chat.id,
                         message.from_user.first_name + ' rolled:\n' + mess_text)
    except MyError as e:
        bot.send_message(e.chat_id, e.txt)
    except Exception as e:
        bot.send_message(message.chat.id, 'ooooops')


@bot.message_handler(commands=['spec', 'sp', 'w'])
def roll_spec(message):
    try:
        dice_count, type, diff, hunger, comment = message_parse(message)

        dices = roll_dices(dice_count, type)
        res = count_success(dices, diff, spec=True)
        if hunger:
            mess_text = form_text_hunger(dices, res, diff, hunger, comment)
        else:
            mess_text = form_text(dices, res, diff, comment)
        bot.send_message(message.chat.id,
                         message.from_user.first_name + ' rolled:\n' + mess_text)
    except MyError as e:
        bot.send_message(e.chat_id, e.txt)
    except Exception as e:
        bot.send_message(message.chat.id, 'ooooops')


@bot.message_handler(commands=['event', 'e'])
def roll_event(message):
    text = ' '.join(message.text.split()[1:])

    d1 = roll_dices(1, 6)[0]
    d2 = roll_dices(1, 20)[0]

    mess_text = '{} {} {}'.format(d1, d2, text)
    bot.send_message(message.chat.id,
                     message.from_user.first_name + ' rolled:\n' + mess_text)


def local_match(pattern, string):
    if ';' in string:
        string.replace(';', '\;')
    if ')' in string:
        string.replace(')', '\)')
    return re.match(pattern, string)

mess_for_path = 'Точка пути: {}\n' \
                    'Мы сделаем это за {} раундов\n' \
                    'Сложность будет: {}'

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    params = re.findall('\d+', call.message.text)
    p, r, diff = int(params[0]), int(params[1]), int(params[2])
    if call.data == "test1":
        diff = diff - 1
        mess_text = mess_for_path.format(p, r, diff)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mess_text,
                              reply_markup=gen_markup_po())
    elif call.data == "test2":
        diff = diff - 2
        mess_text = mess_for_path.format(p, r, diff)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mess_text,
                              reply_markup=gen_markup_vs())
    elif call.data == "test3":
        diff = diff - 2
        mess_text = mess_for_path.format(p, r, diff)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mess_text)
    elif call.data == "test4":
        diff = diff - 1
        mess_text = mess_for_path.format(p, r, diff)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mess_text)


@bot.message_handler(commands=['path'])
def path(message):
    try:
        params = re.findall('\d+', message.text)
        if len(params) < 1:
            bot.send_message(message.chat.id, 'Введите точку пути и за сколько раундов хотите кастовать!')
            return
        elif len(params) == 1:
            p = int(params[0])
            r = p
        else:
            p = int(params[0])
            r = int(params[1])

        if p > 6:
            bot.send_message(message.chat.id, 'Это ты типа такой могучий чародей?')
            return
        if r > p:
            bot.send_message(message.chat.id, 'Это не имеет никакого смысла')
            return

        diff = 4 + p + (p - r) - 1
        mess_text = mess_for_path.format(p, r, diff)

        bot.send_message(message.chat.id, mess_text, reply_markup=gen_markup_start())
    except Exception as e:
        bot.send_message(message.chat.id, 'ooooops')

@bot.message_handler(commands=["rules"])
def rules_choose(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Боевка", url="http://serial-wod.ru/article/1125"))
    keyboard.add(InlineKeyboardButton(text="Пути чародеев", url="http://serial-wod.ru/article/816"))
    keyboard.add(InlineKeyboardButton(text="Компендиум по вампирам", url="http://serial-wod.ru/article/861"))
    bot.send_message(message.chat.id, "Правила", reply_markup=keyboard)


@bot.message_handler(commands=['h'])
def roll_hunger(message):
    try:
        dice_count, type, diff, hunger, comment = message_parse(message)
        diff = 6
        if dice_count not in [1, 2]:
            raise MyError('HungerNum', message.chat.id)
        dices = roll_dices(dice_count, type)
        res = count_success(dices, diff, one=False)

        # message text forming 
        dices = [str(d) for d in dices]
        if res > 0:
            mess_text = ' '.join(dices) + ' ' + comment + '\n' + 'Твой голод не увеличился'
        else:
            mess_text = ' '.join(dices) + ' ' + comment + '\n' + '+1 голод'
        bot.send_message(message.chat.id,
                         message.from_user.first_name + ' rolled:\n' + mess_text)
    except MyError as e:
        bot.send_message(e.chat_id, e.txt)
    except Exception as e:
        bot.send_message(message.chat.id, 'ooooops')

@bot.message_handler(commands=["step"])
def step_count(message):
    try:
        dt = re.findall('\d{2}.\d{2}.\d{4}', message.text)
        if dt == []:
            raise MyError('NoDate', 1)
        dt = dt[0]
        l1 = int(dt[0]) + int(dt[1]) + int(dt[3]) + int(dt[4]) + int(dt[6]) + int(dt[7]) + int(dt[8]) + int(dt[9])
        l2 = l1 // 10 + l1 % 10
        n = int(dt[0]) if dt[0] != '0' else int(dt[1])
        l3 = l1 - 2 * n
        l4 = l3 // 10 + l3 % 10

        res = ''.join(sorted((dt + '{}{}{}{}'.format(l1, l2, l3, l4)).replace('.', '')))
        result = 'Первое рабочее число: {}\n' \
                 'Второе рабочее число: {}\n' \
                 'Третье рабочее число: {}\n' \
                 'Четвертое рабочее число: {}\n\n' \
                 '{}'.format(l1, l2, l3, l4, res)
        bot.send_message(message.chat.id, result)

    except MyError as e:
        bot.send_message(e.chat_id, e.txt)
    except Exception as e:
        bot.send_message(message.chat.id, e)

@bot.message_handler(commands=['l'])
def roll_legendary(message):
    try:
        dice_count, type, diff, hunger, comment = message_parse(message)

        dices = roll_dices(dice_count, type)
        res = count_success(dices, diff, legendary=True)
        if hunger:
            mess_text = form_text_hunger(dices, res, diff, hunger, comment)
        else:
            mess_text = form_text(dices, res, diff, comment)
        bot.send_message(message.chat.id,
                         message.from_user.first_name + ' rolled:\n' + mess_text)
    except MyError as e:
        bot.send_message(e.chat_id, e.txt)
    except Exception as e:
        bot.send_message(message.chat.id, 'ooooops')

bot.infinity_polling()
