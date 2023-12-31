# -*- coding: utf-8 -*-

# General Libraries
import telebot
from telebot import types
import time
import os
from datetime import datetime
from urllib3.exceptions import NewConnectionError
from requests.exceptions import ReadTimeout, RequestException
import logging
from config import setupEnv

# Gets the directory path where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Reading configuration variables
cfg_name = script_dir + "/config/user.cfg"
confBot = setupEnv.botConfig(cfg_name)

# Configure logging
logging.basicConfig(format='[ %(asctime)s ]  %(message)s', filename= script_dir + '/logs/notify.log', encoding='utf-8', level=confBot.loggingLevel)

TOKEN = confBot.telebotKey  # token provided by BotFather
ALLOWED_IDS = confBot.allowedUserIds # Chats allowed to interact with the Bot
# LOG_DIR = script_dir + "/logs/msg.log" # directory for log
USERS_DIR = script_dir + "/logs/users.log" # directory for users
knownUsers = []  # temporary user registration

commands = {  
    'start': 'Start messaging with the bot',
    'help': 'Gives information about available commands',
    'cd': 'Change the current directory',
    'ping': 'Ping to an address',
    'exec': 'Run a command',
    'execlist': 'Run a list of commands',
    'reboot': 'Reboot the server'
}

markup = types.ReplyKeyboardMarkup()
markup.row('/start', '/help', '/cd')
markup.row('/ping', '/ping', '/ping')
markup.row('/exec', '/execlist', '/reboot')

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            logging.error(str(m.chat.first_name) + " [" + str(m.chat.id) + "]" + " : " + m.text)
            

            # msgDate = datetime.fromtimestamp(m.json['date'])
            # f = open(LOG_DIR, "a+")
            # f.write(str(m.chat.first_name) + " [" + str(m.chat.id) + "]" + "[" + str(msgDate) + "] : " + m.text + "\n")
            # f.close()

def validate_user_id(cid):
    cid = str(cid)
    if cid in ALLOWED_IDS:
        return True
    else:
        logging.error('Invalid User ID')
        bot.send_message(cid, "I'm sorry, you are not authorized to interact with this bot.")
        return False    

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if validate_user_id(cid) == False: return
    f = open(USERS_DIR, "r")
    content = f.readlines()
    for c in content:
        knownUsers.append(c.split(';')[1].split('\n')[0])
    if str(cid) not in knownUsers:
        knownUsers.append(cid)
        f = open(USERS_DIR, "a+")
        f.write(str(m.chat.first_name) + ";" + str(m.chat.id) +"\n")
        f.close()
        bot.send_message(cid, "¡Welcome!", reply_markup=markup)
        command_help(m)  # handler /help
    else:
        bot.send_message(cid, "You had already started talking to me before. Look for the command symbol and check the available commands.", reply_markup=markup)

@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    if validate_user_id(cid) == False: return
    help_text = "Available commands: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text, reply_markup=markup)

@bot.message_handler(commands=['reboot'])
def command_long_text(m):
    cid = m.chat.id
    if validate_user_id(cid) == False: return
    bot.send_message(cid, "Restarting server...")
    bot.send_chat_action(cid, 'typing') # action "typing"
    time.sleep(1)
    os.system("reboot")

@bot.message_handler(commands=['exec'])
def command_long_text(m):
    cid = m.chat.id
    if validate_user_id(cid) == False: return
    bot.send_message(cid, "Running: " + m.text[len("/exec"):])
    bot.send_chat_action(cid, 'typing') # action "typing"
    time.sleep(1)
    f = os.popen(m.text[len("/exec"):])
    result = f.read()
    bot.send_message(cid,"Result: " +result, reply_markup=markup)

@bot.message_handler(commands=['ping'])
def command_long_text(m):
    cid = m.chat.id
    if validate_user_id(cid) == False: return
    bot.send_message(cid, "Running: " + "ping -c 4 " + m.text[len("/ping"):])
    bot.send_chat_action(cid, 'typing') # action "typing"
    time.sleep(1)
    f = os.popen("ping -c 4 " + m.text[len("/ping"):])
    result = f.read()
    bot.send_message(cid,"Result: " +result, reply_markup=markup)

@bot.message_handler(commands=['cd'])
def command_long_text(m):
    cid = m.chat.id
    if validate_user_id(cid) == False: return
    bot.send_message(cid,"Change to directory: "+m.text[len("/cd"):])
    bot.send_chat_action(cid, 'typing') # action "typing"
    time.sleep(1)
    os.chdir(m.text[len("/cd"):].strip())
    f = os.popen("pwd")
    result = f.read()
    bot.send_message(cid,"Directory: "+result, reply_markup=markup)

@bot.message_handler(commands=['execlist'])
def command_long_text(m):
    cid = m.chat.id
    if validate_user_id(cid) == False: return
    commands = m.text[len("/execlist\n"):].split('\n')
    for com in commands:
        bot.send_message(cid, "Running: " + com)
        bot.send_chat_action(cid, 'typing') # action "typing"
        time.sleep(1)
        f = os.popen(com)
        result = f.read()
        bot.send_message(cid, "Result: " + result, )
    bot.send_message(cid,"Commands executed", reply_markup=markup)

while True:
    try:
        # Attempt to get updates from the bot
        bot.polling(none_stop=True)

    except (NewConnectionError, ReadTimeout, RequestException) as e:
        # Handle the ReadTimeout exception here
        logging.error(f"Error: {e}")

        # You can try to reconnect or perform some other action
        # You can put a delay before retrying to avoid continuous rapid cycles
        time.sleep(5)  # Wait for 5 seconds before retrying

        continue  # Go back to the beginning of the loop

    except Exception as e:
        # Handle other exceptions here
        logging.error(f"Unexpected error: {e}")
        break  # Break the loop in case of other errors