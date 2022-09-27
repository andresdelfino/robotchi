from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import BOT_TOKEN


def start(update, context):  # Update is an object that represents an incoming update sent via a chat
    print("We are inside start function")
    context.bot.send_message(  # This is the send_message method from class meme_bot.py. This method is used to send
        # text messages. We are passing two arguments: chat_id, which is the unique identifier for the target chat or
        # username of the target channel, and text, which is the text of the message to be sent (max 4096 characters)
        chat_id=update.effective_chat.id,  # We get the unique id of the chat from where the user sent the command
        text="This is the start function"
    )


def echo(update, context):
    print("We are inside echo function")
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text  # We are sending back the same message that the user send to the bot
    )


start_handler = CommandHandler('start', start)  # CommandHandler is a class that defines what happens when a user
# executes a command (/command). In this case, when user sends "start" command, the start function will be called
echo_handler = MessageHandler(Filters.text & (not Filters.command), echo)  # MessageHandler is a class used when we
# need to handle telegram messages. They might contain text, media or status updates


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
    updater.start_polling()