import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import BOT_TOKEN
from tools import *
from os import getcwd, path, listdir
from tags import tag_dict
import urllib.request
from bs4 import BeautifulSoup


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
        photo=open(path.join(getcwd(), "memes/" + chosen_meme), 'rb')  # agnostic import
    )
    log_command("/meme", str(update.message.from_user['username']))


def get_wiki(update, context):
    url = "https://es.wikipedia.org/wiki/"
    print("We are inside get_wiki function")
    element = ' '.join(context.args)
    path = "wiki/" + element + ".html"
    try:
        urllib.request.urlretrieve(url + element, path)
        with open(path, "r", encoding="utf8") as f:
            page = f.read()
        soup = BeautifulSoup(page, "html.parser")
        message = soup.select("div p")[0].get_text()
    except urllib.error.HTTPError:
        message = "Wikipedia has no information about " + element
    except FileNotFoundError:
        message = "File " + path + " does not exist"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message
    )
    log_command("/wiki", str(update.message.from_user['username']))


start_handler = CommandHandler('start', start)  # CommandHandler is a class that defines what happens when a user
# executes a command (/command). In this case, when user sends "start" command, the start function will be called
echo_handler = MessageHandler(Filters.text & (~ Filters.command), echo)  # MessageHandler is a class used when we
# need to handle telegram messages. They might contain text, media or status updates
meme_handler = CommandHandler('meme', get_meme)
wiki_handler = CommandHandler('wiki', get_wiki)

if __name__ == "__main__":
    updater = Updater(token=BOT_TOKEN)  # Updater class, which employs the class Dispatcher, provides a frontend to the
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
    updater.start_polling()
