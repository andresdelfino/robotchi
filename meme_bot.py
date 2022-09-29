import pprint
import random
import uuid
from telegram import InlineQueryResultPhoto
from telegram.error import BadRequest
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, MessageHandler, Filters
from config import BOT_TOKEN
from tools import *
from os import environ, getcwd, path, listdir
from tags import tag_dict
import urllib.request
from bs4 import BeautifulSoup
import re


memes = [
    {
        'id': str(uuid.uuid4()),
        'name': 'aliens',
        'photo_url': 'https://www.meme-arsenal.com/memes/6b8f460f481aa48441d8dc6d88d0a041.jpg',
        'thumb_url': 'https://www.meme-arsenal.com/memes/6b8f460f481aa48441d8dc6d88d0a041.jpg',
        'tags': {
            'aliens',
        }
    },
    {
        'id': str(uuid.uuid4()),
        'name': 'but_it_s_honest_work',
        'photo_url': 'https://www.meme-arsenal.com/memes/333258e655f5d613b7ee4a0663e0506d.jpg',
        'thumb_url': 'https://www.meme-arsenal.com/memes/333258e655f5d613b7ee4a0663e0506d.jpg',
        'tags': {
            *"but it's honest work".split(),
        }
    },
    {
        'id': str(uuid.uuid4()),
        'name': 'not_sure_if',
        'photo_url': 'https://www.meme-arsenal.com/memes/389f398c7bf55ae32a8a326031af2c32.jpg',
        'thumb_url': 'https://www.meme-arsenal.com/memes/389f398c7bf55ae32a8a326031af2c32.jpg',
        'tags': {
            'fry',
            *'not sure if'.split(),
            'futurama',
        },
    },
    {
        'id': str(uuid.uuid4()),
        'name': 'shut_up_and_take_my_money',
        'photo_url': 'https://www.meme-arsenal.com/memes/ed3a49701d7dce8d9d1cb5f74a7f79f8.jpg',
        'thumb_url': 'https://www.meme-arsenal.com/memes/ed3a49701d7dce8d9d1cb5f74a7f79f8.jpg',
        'tags': {
            'fry',
            *'shut up and take my money'.split(),
            'futurama',
        }
    },
    {
        'id': str(uuid.uuid4()),
        'name': 'spider_man_pointing_at_spider_man',
        'photo_url': 'https://www.meme-arsenal.com/memes/2332a9b45fea20c7f92ea5324dd6be49.jpg',
        'thumb_url': 'https://www.meme-arsenal.com/memes/2332a9b45fea20c7f92ea5324dd6be49.jpg',
        'tags': {
            'spiderman',
            'spider-man',
            'doble',
            'duplicado',
            'igual',
        }
    },
]


def start(update, context):  # Update is an object that represents an incoming update sent via a chat
    print("We are inside start function")
    context.bot.send_message(  # This is the send_message method from class meme_bot.py. This method is used to send
        # text messages. We are passing two arguments: chat_id, which is the unique identifier for the target chat or
        # username of the target channel, and text, which is the text of the message to be sent (max 4096 characters)
        chat_id=update.effective_chat.id,  # We get the unique id of the chat from where the user sent the command
        text="This is the start function"
    )
    log_command("/start", str(update.message.from_user['username']))
    # All infomation about user (as username, id, first/last name
    # and profile photos) available from telegram.User object. You can easily get it using telegram.Message


def echo(update, context):
    print("We are inside echo function")
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text  # We are sending back the same message that the user send to the bot
    )


def get_meme(update, context):
    print("We are inside get_meme function")
    user_tag = ' '.join(context.args)
    if user_tag.lower() in tag_dict.keys():
        print("User used a tag and it matches")
        chosen_meme = random.choice(tag_dict[user_tag.lower()]) + ".jpg"
    else:
        print("User didn't used a tag or the tag didn't matched")
        memes = [meme for meme in listdir(path.join(getcwd(), 'memes'))]  # issue #2, may need testing.
        chosen_meme = random.choice(memes)
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(path.join(getcwd(), "memes", chosen_meme), 'rb')  # agnostic import
    )
    log_command("/meme", str(update.message.from_user['username']))


def get_wiki(update, context):
    url = "https://es.wikipedia.org/wiki/"
    print("We are inside get_wiki function")
    element = ' '.join(context.args)
    route = f"wiki/{element}.html"  # "path" coflicts with the module of the same name
    message = download_wiki(element, route, url)
    try:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message
        )
    except BadRequest:
        print("There was an issue with the message")
    log_command("/wiki", str(update.message.from_user['username']))


def download_wiki(element, route, url):
    try:
        urllib.request.urlretrieve(url + element, route)
        with open(route, "r", encoding="utf8") as f:
            page = f.read()
        soup = BeautifulSoup(page, "html.parser")
        # TODO: check when the term is ambiguous
        message = soup.find("div", id="bodyContent") \
            .find("div", id="mw-content-text") \
            .find("div", {"class": "mw-parser-output"}) \
            .find("p").get_text()
        message = re.sub('\[\d\]', '', message)  # Pycharm me está tirando erroes en este RE
    except urllib.error.HTTPError:
        message = f"Wikipedia has no information about {element}"
    except FileNotFoundError:
        message = f"File {route} does not exist"
    return message


def inline_query(update, context):  # parameter context is not used.
    # https://core.telegram.org/bots/api#inlinequeryresultphoto

    # https://docs.python-telegram-bot.org/en/v13.14/telegram.ext.inlinequeryhandler.html
    # https://docs.python-telegram-bot.org/en/v13.14/telegram.inlinequery.html
    # https://docs.python-telegram-bot.org/en/v13.14/telegram.inlinequeryresultphoto.html

    print('We are inside inline_query function')

    query = update.inline_query.query

    print('User:', update.inline_query.from_user.username)
    print('Query:', query)

    if query == '':
        return

    results = []

    tags = set(query.lower().split())

    print('Memes matched:')

    for meme in memes:
        if query == 'all' or tags <= meme['tags']:
            print('*', meme['name'])
            results.append(
                InlineQueryResultPhoto(
                    id=meme['id'],
                    photo_url=meme['photo_url'],
                    thumb_url=meme['thumb_url'],
                ),
            )

    if not results:
        print('None')

    update.inline_query.answer(results, cache_time=0)


start_handler = CommandHandler('start', start)  # CommandHandler is a class that defines what happens when a user
# executes a command (/command). In this case, when user sends "start" command, the start function will be called
echo_handler = MessageHandler(Filters.text & (~ Filters.command), echo)  # MessageHandler is a class used when we
# need to handle telegram messages. They might contain text, media or status updates
meme_handler = CommandHandler('meme', get_meme)
wiki_handler = CommandHandler('wiki', get_wiki)

inline_handler = InlineQueryHandler(inline_query)

if __name__ == "__main__":
    bot_token = environ.get('BOT_TOKEN', BOT_TOKEN)
    updater = Updater(token=bot_token)  # Updater class, which employs the class Dispatcher, provides a frontend to the
    # class Bot to the programmer, so they can focus on coding the bot. Its purpose is to receive the updates from
    # Telegram and to deliver them to said dispatcher. It also runs in a separate thread, so the user can interact with
    # the bot, for example on the command line.
    dispatcher = updater.dispatcher  # This class dispatches all kinds of updates to its registered handlers. The
    # dispatcher supports handlers for different kinds of data: Updates from Telegram, basic text commands and even
    # arbitrary types.
    dispatcher.add_handler(start_handler, 0)  # Register a handler to the dispatcher. Order and priority counts.
    dispatcher.add_handler(echo_handler, 0)
    dispatcher.add_handler(meme_handler, 0)
    dispatcher.add_handler(wiki_handler, 0)
    dispatcher.add_handler(inline_handler)
    updater.start_polling()
