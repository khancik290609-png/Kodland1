import telebot
import os
import random
from labyrinth import create_zone
from labyrinth import render_area
from botlogic import generate_password
from botlogic import smash_bash
from dotenv import load_dotenv
from telebot import types

load_dotenv()

dictionary = {'info':
              u'Bot\'s name is {name}\n'
              u'Bot\'s command list:\n{comlist}\n'
              }

symbols = {
    0: ' ',
    1: '\u2B1B',
    2: '🙂'
}

API_TOKEN=os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

def get_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    markup.row("⬅", "➡")
    markup.row("⬇", "🔄")

    return markup

# Handle '/start' and '/help'
print("Bot is starting...")
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")

print("Bot is ready to receive messages...")
players = {}

@bot.message_handler(commands=['labyrinth'])
def structure(message):
    words = message.text.split()
    rows = int(words[1]) if len(words) >= 2 else 10
    cols = int(words[2]) if len(words) >= 2 else 10
    area = create_zone(rows, cols)
    start = None
    for c in range(cols):
        if area[0][c] == 0:
            start = (0, c)
            break
    if start is None:
        bot.reply_to(message, "Не удалось найти вход.")
        return
    players[message.chat.id] = {
        "area": area,
        "pos": start,
        "rows": rows,
        "cols": cols
    }

    bot.send_message(message.chat.id, "Лабиринт создан! Используй кнопки для перемещения." + render_area(area, start), reply_markup=get_keyboard())

@bot.message_handler(func=lambda m: m.text == "🔄")
def restart(message):
    chat_id = message.chat.id
    if chat_id not in players:
        bot.reply_to(message, "Сначала создай лабиринт командой /labyrinth")
        return
    area = players[chat_id]["area"]
    rows = players[chat_id]["rows"]
    cols = players[chat_id]["cols"]
    new_area = create_zone(rows, cols)
    start = None
    for c in range(cols):
        if new_area[0][c] == 0:
            start = (0, c)
            break
    if start is None:
        bot.reply_to(message, "Не удалось найти вход.")
        return
    players[chat_id] = {
        "area": new_area,
        "pos": start,
        "rows": rows,
        "cols": cols
    }
    bot.send_message(chat_id, "Лабиринт перезапущен!" + render_area(new_area, start), reply_markup=get_keyboard())

print("Bot is ready to handle labyrinth commands...")
@bot.message_handler(func=lambda m: m.text in ["⬅", "➡", "⬇"])
def labyrinth_move(message):
    chat_id = message.chat.id
    if chat_id not in players:
        bot.reply_to(message, "Сначала создай лабиринт командой /labyrinth")
        return
    data = players[chat_id]
    area = data["area"]
    row, col = data["pos"]
    move = message.text.lower()
    new_row, new_col = row, col
    if move == "⬅":
        new_col -= 1
    elif move == "➡":
        new_col += 1
    elif move == "⬇":
        new_row += 1
    rows = len(area)
    cols = len(area[0])
    if not (0 <= new_row < rows and 0 <= new_col < cols):
        bot.reply_to(message, "Нельзя выйти за границы!")
        return
    if area[new_row][new_col] == 1:
        bot.reply_to(message, "Там стена!")
        return
    players[chat_id]["pos"] = (new_row, new_col)
    if new_row == rows - 1:
        bot.send_message(message.chat.id, "WIN!\n\n" + render_area(area, (new_row, new_col)), reply_markup=types.ReplyKeyboardRemove())
        del players[chat_id]
        return
    
    bot.send_message(message.chat.id, render_area(area, (new_row, new_col)), reply_markup=get_keyboard())


print("Bot is ready to handle info, password, mix, heh, and mem commands...")
@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id, dictionary['info'].format(name=bot.get_me().first_name, comlist="\n".join(['/help', '/start', '/info', '/password', '/mix', '/heh', '/mem', '/labyrinth', 'private commands: left, right, down'])))

print("Bot is ready to handle password command...")
@bot.message_handler(commands=['password'])
def send_password(message):
    words = message.text.split()
    length = int(words[1]) if len(words) >= 2 else 5
    bot.reply_to(message, generate_password(length))

print("Bot is ready to handle mix command...")
@bot.message_handler(commands=['mix'])
def send_newPassword(message):
    words = message.text.split(maxsplit=1)
    if len(words) < 2:
        bot.reply_to(message, "Usage: /mix <text>")
        return
    result = smash_bash(words[1])
    bot.reply_to(message, result)

print("Bot is ready to handle heh command...")
@bot.message_handler(commands=['heh'])
def send_heh(message):
    count_heh = int(message.text.split()[1]) if len(message.text.split()) > 1 else 5
    bot.reply_to(message, "he" * count_heh)

print("Bot is ready to handle mem command...")
@bot.message_handler(commands=['mem'])
def send_mem(message):
    images = os.listdir("images")
    with open(f"images/{random.choice(images)}", 'rb') as f:  
        bot.send_photo(message.chat.id, f)  

print("Bot is ready to handle all other text messages...")
# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)
bot.delete_webhook()
print("Bot is running...")

bot.infinity_polling()
