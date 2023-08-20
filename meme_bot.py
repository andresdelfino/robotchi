import pprint
import random
from memes import memes
from telegram import InlineQueryResultPhoto, Update
from telegram.error import BadRequest
from telegram.ext import Application, CommandHandler, InlineQueryHandler, MessageHandler, filters
from config import BOT_TOKEN
from os import environ, getcwd, path, listdir
from tags import tag_dict
import urllib.request
from bs4 import BeautifulSoup
import re
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update, context):  # Update is an object that represents an incoming update sent via a chat
    user = update.message.from_user
    await context.bot.send_message(  # This is the send_message method from class meme_bot.py. This method is used to send
        # text messages. We are passing two arguments: chat_id, which is the unique identifier for the target chat or
        # username of the target channel, and text, which is the text of the message to be sent (max 4096 characters)
        chat_id=update.effective_chat.id,  # We get the unique id of the chat from where the user sent the command
        text="This is the start function"
    )
    logger.info("User %s called the start command", user.first_name)
    # All infomation about user (as username, id, first/last name
    # and profile photos) available from telegram.User object. You can easily get it using telegram.Message


async def echo(update, context):
    user = update.message.from_user
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text  # We are sending back the same message that the user send to the bot
    )
    logger.info("User %s called the echo command", user.first_name)


async def get_meme(update, context):
    user = update.message.from_user
    user_tag = ' '.join(context.args)
    if user_tag.lower() in tag_dict.keys():
        logger.info("User %s used a matching tag", user.first_name)
        chosen_meme = random.choice(tag_dict[user_tag.lower()]) + ".jpg"
    else:
        logger.info("User %s didn\'t use a tag or it didn\'t match", user.first_name)
        memes = [meme for meme in listdir(path.join(getcwd(), 'memes'))]  # issue #2, may need testing.
        chosen_meme = random.choice(memes)
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(path.join(getcwd(), "memes", chosen_meme), 'rb')  # agnostic import
    )
    logger.info("User %s called the get_meme command", user.first_name)


async def get_wiki(update, context):
    url = "https://es.wikipedia.org/wiki/"
    user = update.message.from_user
    element = ' '.join(context.args)
    route = f"wiki/{element}.html"  # "path" coflicts with the module of the same name
    message = download_wiki(element, route, url)
    try:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message
        )
    except BadRequest:
        logger.info("There was an issue with the message")
    logger.info("User %s called the get_wiki command", user.first_name)


async def download_wiki(element, route, url):
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


async def inline_query(update, context):  # parameter context is not used.
    # https://core.telegram.org/bots/api#inlinequeryresultphoto
    # https://docs.python-telegram-bot.org/en/v13.14/telegram.ext.inlinequeryhandler.html
    # https://docs.python-telegram-bot.org/en/v13.14/telegram.inlinequery.html
    # https://docs.python-telegram-bot.org/en/v13.14/telegram.inlinequeryresultphoto.html
    query = update.inline_query.query
    if update.message and update.message.from_user:
        logger.info("User %s is making an inline query", update.message.from_user.first_name)
    else:
        logger.info("Someone is making an inline query")
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
                    thumbnail_url=meme['thumb_url'],
                ),
            )

    if not results:
        print('None')

    await update.inline_query.answer(results, cache_time=0)


start_handler = CommandHandler('start', start)  # CommandHandler is a class that defines what happens when a user
# executes a command (/command). In this case, when user sends "start" command, the start function will be called
echo_handler = MessageHandler(filters.TEXT & (~ filters.COMMAND), echo)  # MessageHandler is a class used when we
# need to handle telegram messages. They might contain text, media or status updates
meme_handler = CommandHandler('meme', get_meme)
wiki_handler = CommandHandler('wiki', get_wiki)

inline_handler = InlineQueryHandler(inline_query)

if __name__ == "__main__":
    bot_token = environ.get('BOT_TOKEN', BOT_TOKEN)

    application = Application.builder().token(bot_token).build()

    application.add_handler(start_handler, 0)  # Register a handler to the dispatcher. Order and priority counts.
    application.add_handler(echo_handler, 0)
    application.add_handler(meme_handler, 0)
    application.add_handler(wiki_handler, 0)
    application.add_handler(inline_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)
