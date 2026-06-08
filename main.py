import telebot
import os
from botlogic import generate_password
from botlogic import smash_bash
from dotenv import load_dotenv

load_dotenv()

dictionary = {'info':
              u'Bot\'s name is {name}\n'
              u'Bot\'s command list:\n{comlist}\n'
              }

API_TOKEN=os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")
    
@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id, dictionary['info'].format(name=bot.get_me().first_name, comlist="\n".join(['/help', '/start', '/info', '/password', '/mix', '/heh'])))

@bot.message_handler(commands=['password'])
def send_password(message):
    words = message.text.split()
    length = int(words[1]) if len(words)>=2 else 5
    bot.reply_to(message, generate_password(length))

@bot.message_handler(commands=['mix'])
def send_newPassword(message):
    result=smash_bash(message)
    bot.reply_to(message, result)

@bot.message_handler(commands=['heh'])
def send_heh(message):
    count_heh = int(message.text.split()[1]) if len(message.text.split()) > 1 else 5
    bot.reply_to(message, "he" * count_heh)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)



bot.infinity_polling()
