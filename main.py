import telebot
from telebot import types

token = open('token.txt').readline()
bot = telebot.TeleBot(token)

startup = (
    'Here is your startup message'
    '')
links = {
    'Key': [
        ['Post name', 'Post link'],
        ['Post name 2', 'Post link 2'],
    ]
}


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, startup, parse_mode='html')


@bot.message_handler(commands=['update'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("All")
    markup.add(item1)
    for key in links.keys():
        markup.add(types.KeyboardButton(key))
    bot.send_message(message.chat.id, 'Updated, check it!', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def message_reply(message):
    def get_linklist(key):
        linklist = f'<b>{key}</b>\n\n'
        for link in links[key]:
            linklist += f'<a href="{link[1]}">{link[0]}</a>\n'
        return linklist

    if message.text == "All":
        for key in links.keys():
            bot.send_message(message.chat.id, get_linklist(key), parse_mode='html')
    else:
        bot.send_message(message.chat.id, get_linklist(message.text), parse_mode='html')


bot.infinity_polling()
