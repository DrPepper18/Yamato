import telebot
from telebot import types
import parser

token = open('private_data.txt').readline()[:-1]
bot = telebot.TeleBot(token)

startup = ' '.join(open('startup.txt', encoding='utf-8').readlines())
links = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, startup, parse_mode='html')


@bot.message_handler(commands=['update'])
def button_message(message):
    bot.send_message(message.chat.id, 'Подождите, идёт загрузка. . .')
    def update_groups():
        bot.send_message(message.chat.id, 'Парсинг...')
        post_name, post_url, post_tags = parser.parsing()
        bot.send_message(message.chat.id, 'Группировка...')
        for i in range(len(post_tags)):
            for tag in post_tags[i]:
                if tag not in links.keys():
                    links[tag] = []
                links[tag].append([post_name[i], post_url[i]])
        return

    update_groups()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Скинь всё, что есть"))
    for key in links.keys():
        markup.add(types.KeyboardButton(key))
    bot.send_message(message.chat.id, 'Группы постов обновлены, выбирайте!', reply_markup=markup)
    print(links)


@bot.message_handler(content_types=['text'])
def message_reply(message):
    def get_linklist(key):
        linklist = f'<b>{key}</b>\n\n'
        for link in links[key]:
            linklist += f'<a href="{link[1]}">{link[0]}</a>\n'
        return linklist

    if message.text == "Скинь всё, что есть":
        for key in links.keys():
            bot.send_message(message.chat.id, get_linklist(key), parse_mode='html')
    else:
        bot.send_message(message.chat.id, get_linklist(message.text), parse_mode='html')


bot.infinity_polling()
