from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from asyncio import set_event_loop, new_event_loop
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import re

# data for start
data = open('private_data.txt').readlines()
'''
Structure of private_data.txt:
Row 1 - Bot token
Row 2 - ID of your Telegram App
Row 3 - Hash of your Telegram App
Row 4 - Your phone (for Telegram App)
'''


def parsing():
    set_event_loop(new_event_loop())
    client = TelegramClient(data[3], int(data[1]), data[2])
    client.start()
    target_group = '@bluscreendez'
    offset_id = 0
    limit = 100
    all_messages = []
    while True:
        history = client(GetHistoryRequest(
            peer=target_group,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message)
        offset_id = messages[len(messages) - 1].id

    def get_tags(text):
        return list(set([word for word in text[-200:].split() if word[0] == '#']))

    post_name = []
    post_url = []
    post_tags = []
    for message in all_messages:
        if message.message:
            post_name.append(re.split(r'\.|\?|\:|\n', message.message)[0][:45])
            post_url.append('https://t.me/' + target_group[1:] + '/' + str(message.id))
            post_tags.append(get_tags(message.message))
            if post_tags[-1]:
                print(post_tags[-1])
    return post_name, post_url, post_tags


'''
savefile = pd.DataFrame({
    'name': post_name,
    'text': post_text,
    'url': post_url,
    'tags': post_tags
})
savefile.to_excel('chats.xlsx', index=False)
print('Парсинг сообщений группы успешно выполнен.')
'''
