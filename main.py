# -*- coding: utf-8 -*-

# General Libraries
import telebot
from telebot import types
import time
import os
from datetime import datetime
import logging
from config import setupEnv

# Gets the directory path where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Reading configuration variables
cfg_name = script_dir + "/config/user.cfg"
confBot = setupEnv.botConfig(cfg_name)

# Configure logging
logging.basicConfig(format='[ %(asctime)s ]  %(message)s', filename='logs/logSystem.log', encoding='utf-8', level=confBot.loggingLevel)

TOKEN = confBot.telebotKey  # token brindado por BotFather
LOG_DIR = script_dir + "/logs/logBot.log" # directorio para log
USERS_DIR = script_dir + "/logs/users.log" # directorio para usuarios
knownUsers = []  # registro temporal de usuarios

commands = {  
    'start': 'Empezar a mensajear con el bot',
    'ayuda': 'Da información sobre los comandos disponibles',
    'cd': 'Cambia el directorio actual',
    'exec': 'Ejecuta un comando',
    'execlist': 'Ejecuta una lista de comandos',
    'reboot': 'Reinicia el servidor'
}

markup = types.ReplyKeyboardMarkup()
markup.row('/start', '/ayuda', '/cd')
markup.row('/exec', '/execlist', '/reboot')

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            fecha = datetime.fromtimestamp(m.json['date'])
            f = open(LOG_DIR, "a+")
            f.write(str(m.chat.first_name) + " [" + str(m.chat.id) + "]" + "[" + str(fecha) + "] : " + m.text + "\n")
            f.close()

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    f = open(USERS_DIR, "r")
    content = f.readlines()
    for c in content:
        knownUsers.append(c.split(';')[1].split('\n')[0])
    if str(cid) not in knownUsers:
        knownUsers.append(cid)
        f = open(USERS_DIR, "a+")
        f.write(str(m.chat.first_name) + ";" + str(m.chat.id) +"\n")
        f.close()
        bot.send_message(cid, "¡Bienvenido!", reply_markup=markup)
        command_help(m)  # presenta al usuario el handler /ayuda
    else:
        bot.send_message(cid, "Ya habías empezado a hablar conmigo anteriormente. Busca el símbolo de comandos y revisa los comandos disponibles.", reply_markup=markup)

@bot.message_handler(commands=['ayuda'])
def command_help(m):
    cid = m.chat.id
    help_text = "Comandos disponibles: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text, reply_markup=markup)

@bot.message_handler(commands=['reboot'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "Reiniciando servidor...")
    bot.send_chat_action(cid, 'typing') # acción "escribiendo"
    time.sleep(3)
    os.system("reboot")

@bot.message_handler(commands=['exec'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "Ejecutando: " + m.text[len("/exec"):])
    bot.send_chat_action(cid, 'typing') # acción "escribiendo"
    time.sleep(2)
    f = os.popen(m.text[len("/exec"):])
    result = f.read()
    bot.send_message(cid,"Resultado: " +result, reply_markup=markup)

@bot.message_handler(commands=['cd'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid,"Cambio a directorio:"+m.text[len("/cd"):])
    bot.send_chat_action(cid, 'typing') # acción "escribiendo"
    time.sleep(2)
    os.chdir(m.text[len("/cd"):].strip())
    f = os.popen("pwd")
    result = f.read()
    bot.send_message(cid,"Directorio :"+result, reply_markup=markup)

@bot.message_handler(commands=['execlist'])
def command_long_text(m):
    cid = m.chat.id
    comandos = m.text[len("/execlist\n"):].split('\n')
    for com in comandos:
        bot.send_message(cid, "Ejecutando: " + com)
        bot.send_chat_action(cid, 'typing') # acción "escribiendo"
        time.sleep(2)
        f = os.popen(com)
        result = f.read()
        bot.send_message(cid, "Resultado: " + result, )
    bot.send_message(cid,"Comandos ejecutados", reply_markup=markup)

bot.polling()