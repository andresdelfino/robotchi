import pprint
import random
from memes import memes
from telegram import InlineQueryResultPhoto
from telegram.error import BadRequest
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, MessageHandler, Filters
from config import BOT_TOKEN
from os import environ, getcwd, path, listdir
from tags import tag_dict
import urllib.request
from bs4 import BeautifulSoup
import re
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):  # Update is an object that represents an incoming update sent via a chat
    user = update.message.from_user
    context.bot.send_message(  # This is the send_message method from class meme_bot.py. This method is used to send
        # text messages. We are passing two arguments: chat_id, which is the unique identifier for the target chat or
        # username of the target channel, and text, which is the text of the message to be sent (max 4096 characters)
        chat_id=update.effective_chat.id,  # We get the unique id of the chat from where the user sent the command
        text="This is the start function"
    )
    logger.info("User %s called the start command", user.first_name)
    # All infomation about user (as username, id, first/last name
    # and profile photos) available from telegram.User object. You can easily get it using telegram.Message


def echo(update, context):
    user = update.message.from_user
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text  # We are sending back the same message that the user send to the bot
    )
    logger.info("User %s called the echo command", user.first_name)


def get_meme(update, context):
    user = update.message.from_user
    user_tag = ' '.join(context.args)
    if user_tag.lower() in tag_dict.keys():
        logger.info("User %s used a matching tag", user.first_name)
        chosen_meme = random.choice(tag_dict[user_tag.lower()]) + ".jpg"
    else:
        logger.info("User %s didn\'t use a tag or it didn\'t match", user.first_name)
        memes = [meme for meme in listdir(path.join(getcwd(), 'memes'))]  # issue #2, may need testing.
        chosen_meme = random.choice(memes)
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(path.join(getcwd(), "memes", chosen_meme), 'rb')  # agnostic import
    )
    logger.info("User %s called the get_meme command", user.first_name)


def get_wiki(update, context):
    url = "https://es.wikipedia.org/wiki/"
    user = update.message.from_user
    element = ' '.join(context.args)
    route = f"wiki/{element}.html"  # "path" coflicts with the module of the same name
    message = download_wiki(element, route, url)
    try:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message
        )
    except BadRequest:
        logger.info("There was an issue with the message")
    logger.info("User %s called the get_wiki command", user.first_name)


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
    user = update.message.from_user
    query = update.inline_query.query
    logger.info("User %s is making an inline query", user.first_name)
    logger.info("The query is: %s ", query)

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
