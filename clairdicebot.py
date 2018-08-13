#!/usr/bin/python3.5
import telebot
import re
import traceback
import sys
import random

token = '260104236:AAF9vWtho15vJfaj8xqrOGcxkUPgLGiPtYE'

bot = telebot.TeleBot(token)
CMD = ['/roll - введите сколько d10  мне нужно кинуть и зачем, а я кину и выведу. \nФормат: /roll <число кубов> <сложность> <текст>\nПример:\n/roll 12 7 Джен Эллиот стреляет в голову.\nСложность можно не вводить',
       '/roll1 - тут не вычитаются единички',
       '/r - тоже, что и roll, но если лень набирать',
       '/dice - Чтобы просто кинуть кубик с другим количеством граней. По умолчанию - 10\nПример:\n/dice 10d6\n/dice 12',]


@bot.message_handler(commands=['start'])
def send_start(message):
    bot.send_message(message.chat.id, "Hello, "  + message.from_user.first_name)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, 'Я очень маленький бот и пока умею совсем немного. Вот мои команды:\n'+ '\n'.join(CMD))

@bot.message_handler(commands=['hi'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name)

@bot.message_handler(commands=['hello'])
def send_welcome_hello(message):
    print(message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.text)
    bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name)

def roll_dices(count, type = 10):
    count = int(count)
    type = int(type)
    t = []
    for i in range(count):
        t.append(str(random.randint(1, type)))
    t.sort(key=sortByInt)
    return t



@bot.message_handler(commands=['dice'])
def send_dice(message):
    try:
        print(message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.text)
        m = message.text.split()
        if len(m)>1 and (local_match('[0-9]+[d][0-9]+', m[1])):
            a = m[1].split('d')
            if len(a)>1:
                t = roll_dices(int(a[0]), int(a[1]))
            bot.send_message (message.chat.id, message.from_user.first_name + ' rolled:\n' + ' '.join(t))
        elif len(m)>1 and m[1].isdigit():
            t = roll_dices(m[1])
            bot.send_message(message.chat.id, message.from_user.first_name + ' rolled:\n' + ' '.join(t))
    except:
        print (''.join(traceback.format_exception(*sys.exc_info())))
        bot.send_message(message.chat.id, 'ooooops')


@bot.message_handler(commands=['roll', 'r'])
def send_roll(message):
    try:
        print(message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.text)
        m = message.text.split()
        t = []
        count = 0
        if len(m) > 1 and m[1].isdigit():
            t = roll_dices(m[1])
            odin = t.count('1')
            if len(m) > 2 and m[2].isdigit() and t:
                for i in range(len(t)):
                    if (int(t[i]) >= int(m[2])):
                        count += 1
                count -= odin
                if (count < 0):
                    bot.send_message(message.chat.id,
                                 message.from_user.first_name + ' rolled:\n' +
                                 ' '.join(t) + ' ' + ' '.join(m[3:]) +
                                 '\n' + 'Упс! Это БОТЧ!')
                else:
                    bot.send_message(message.chat.id,
                                     message.from_user.first_name + ' rolled:\n' +
                                     ' '.join(t) + ' ' + ' '.join(m[3:]) +
                                     '\n' + str(count) + ' успехов по сложности ' + str(m[2]))

            elif(len(m) > 2):
                bot.send_message(message.chat.id, message.from_user.first_name + ' rolled:\n' + ' '.join(t) + ' ' + ' '.join(m[2:]))
            else:
                bot.send_message(message.chat.id, message.from_user.first_name + ' rolled:\n' + ' '.join(t))
        else:
            bot.send_message(message.chat.id, 'После команды введи число, сколько кубов кидать!')

    except:
        print (''.join(traceback.format_exception(*sys.exc_info())))
        bot.send_message(message.chat.id, 'ooooops')

@bot.message_handler(commands=['roll1'])
def send_roll1(message):
    try:
        print(message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.text)
        m = message.text.split()
        t = []
        count = 0
        if len(m) > 1 and m[1].isdigit():
            t = roll_dices(m[1])
            if len(m) > 2 and m[2].isdigit() and t:
                for i in range(len(t)):
                    if (int(t[i]) >= int(m[2])):
                        count += 1
                bot.send_message(message.chat.id,
                                     message.from_user.first_name + ' rolled:\n' +
                                     ' '.join(t) + ' ' + ' '.join(m[3:]) +
                                     '\n' + str(count) + ' успехов по сложности ' + str(m[2]) + '\nЕдиницы не вычитаются!')

            elif(len(m) > 2):
                bot.send_message(message.chat.id, message.from_user.first_name + ' rolled:\n' + ' '.join(t) + ' ' + ' '.join(m[2:]))
            else:
                bot.send_message(message.chat.id, message.from_user.first_name + ' rolled:\n' + ' '.join(t))
        else:
            bot.send_message(message.chat.id, 'После команды введи число, сколько кубов кидать!')

    except:
        print (''.join(traceback.format_exception(*sys.exc_info())))
        bot.send_message(message.chat.id, 'ooooops')

def local_match(pattern, string):
    if ';' in string:
        string.replace(';', '\;')
    if ')' in string:
        string.replace(')', '\)')
    return re.match(pattern, string)
def local_search(pattern, string):
    if ';' in string:
        string.replace(';', '\;')
    if ')' in string:
        string.replace(')', '\)')
    return re.search(pattern, string)

def sortByInt(inputStr):
    return int(inputStr)

bot.polling(none_stop=True, interval=0)
