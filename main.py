import telebot
from telebot import types
import parser

token = open('private_data.txt').readline()[:-1]
bot = telebot.TeleBot(token)

startup = ' '.join(open('startup.txt', encoding='utf-8').readlines())
links = {
    'Мероприятия': [
        ['МТС True Tech Champ', 'https://t.me/bluscreendez/246'],
        ['DANO', 'https://t.me/bluscreendez/354'],
        ['ОММО', 'https://t.me/bluscreendez/444'],
        ['НТО АБП. 2023-2024', 'https://t.me/bluscreendez/480'],
    ],
    'Куда занесло': [
        ['Яндекс (главный офис)', 'https://t.me/bluscreendez/69'],
        ['Яндекс (Москва-Сити)', 'https://t.me/bluscreendez/140'],
        ['Тинькофф (Водный стадион)', 'https://t.me/bluscreendez/81'],
        ['Т-Space', 'https://t.me/bluscreendez/464'],
        ['VK', 'https://t.me/bluscreendez/431'],
        ['МИСиС', 'https://t.me/bluscreendez/538'],
        ['МТС', 'https://t.me/bluscreendez/666'],
    ],
    'Мемасы': []
}


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
