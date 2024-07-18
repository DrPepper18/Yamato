import telebot
from telebot import types

token = open('token.txt').readline()
bot = telebot.TeleBot(token)

startup = (
    'Привет, на связи Димон, он же Димас, он же Димыч, он же ДИМОООООНТУРУРУРУРУРУ.\n\n'
    'Увлекаюсь вебом и data science. Всегда рад отправиться в неизведанные мне места и попробовать что-то новое.'
    'Потихоньку вот играю на гитаре, в последнее время читаю и смотрю всякое про саморазвитие.\n\n'
    'Про что этот канал? Сложно сказать. Люблю сюда выложить свои мысли, мемчики, красивые фото и просто поделиться'
    'похождениями и рандомными интересными моментами из повседневности.\n\n'
    'Предупреждаю, возможен передоз кринжом. Но если вам нужен теплый уютный уголок, то welcome. '
    'По крайней мере, я таким постараюсь его сделать.\n\n'
    '/update')
roadmap = (
    'Роудмап:\n'
    '1. Сделать ссылки внутри текста (DONE!)\n'
    '2. Автоматизировать добавление и группировку постов (хэштеги/NLP)\n'
    '3. Премиум-эмодзи внутри бота\n'
    '4. Сделать удобным для использования в ЛЮБОМ телеграм-канале.\n')
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
    bot.send_message(message.chat.id, roadmap, parse_mode='html')


@bot.message_handler(commands=['update'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Скинь всё, что есть")
    markup.add(item1)
    for key in links.keys():
        markup.add(types.KeyboardButton(key))
    bot.send_message(message.chat.id, 'Группы постов обновлены, выбирайте!', reply_markup=markup)


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
