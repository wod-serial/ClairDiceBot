#!/usr/bin/python3.5
import telebot
import re
import random

token = '260104236:AAF9vWtho15vJfaj8xqrOGcxkUPgLGiPtYE'

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_start(message):
    bot.send_message(message.chat.id, "Hello, "  + message.from_user.first_name)

@bot.message_handler(commands=['help'])
def send_help(message):
    mtext = 'Иcпользуйте одну из команд: /r, /roll, /dice\n' \
            + 'Через пробел введите количество кубиков, сложность, комментарий\n'\
            + 'Если нужен кубик не d10, напишите: /r 5d6\n'\
            + 'Пример:\n /r 10 6 Джен Эллиот стреляет в голову'
    bot.send_message(message.chat.id, mtext)

def roll_dices(dice_count, typedice):
    dice_count = int(dice_count)
    typedice = int(typedice)
    t = []
    for i in range(dice_count):
        t.append(str(random.randint(1, typedice)))
    t.sort(key=sortByInt)
    return t


@bot.message_handler(commands=['r', 'roll', 'dice'])
def roll(message):
    type = 10
    dice_count = 1
    diff = ''
    comment = ''
    try:
        m = message.text.split()
        if len(m) <= 1:
            bot.send_message(message.chat.id, 'Напишите сколько кубов кидать!')
            return
        if local_match('[0-9]+[d][0-9]+', m[1]):
            type = int(m[1].split('d')[1])
            dice_count = int(m[1].split('d')[0])
        elif m[1].isdigit() and m[1] != '0':
            dice_count = int(m[1])
        else:
            bot.send_message(message.chat.id, 'Напишите сколько кубов кидать!')
            return
        if (len(m) > 2):
            if m[2].isdigit():
                diff = int(m[2])
                if len(m)>3:
                    comment = ' '.join(m[3:])
            else:
                comment = ' '.join(m[2:])
        mess_text = form_text(dice_count, type, diff, comment)
        bot.send_message(message.chat.id,
                         message.from_user.first_name + ' rolled:\n' + mess_text)

    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'ooooops')

def form_text(dice_count, type, diff, comment):
    dices = roll_dices(dice_count, type)
    odin = dices.count('1')
    success = 0
    if diff == '':
        return ' '.join(dices) + ' ' + comment
    for i in dices:
        if int(i) >= int(diff):
            success +=1
    if success - odin < 0:
        mess_text = ' '.join(dices) + ' ' + comment + '\n' + 'Упс! Это БОТЧ!'
    else:
        mess_text = ' '.join(dices) + ' ' + comment + '\n' + str(success - odin) + ' успехов по сложности ' + str(diff)
    return mess_text


def local_match(pattern, string):
    if ';' in string:
        string.replace(';', '\;')
    if ')' in string:
        string.replace(')', '\)')
    return re.match(pattern, string)


def sortByInt(inputStr):
    return int(inputStr)


bot.infinity_polling()
