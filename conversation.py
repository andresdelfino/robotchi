from telegram import ReplyKeyboardRemove, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
SUBJECT, PHOTO, LOCATION, BIO = range(4)


def talk(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s wants to talk", user.first_name)
    update.message.reply_text(
        'Hello. I am a bot. What do you want to talk about?',
        reply_markup=ReplyKeyboardRemove(),
    )
    return SUBJECT

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('talk', talk)],
    states={
        SUBJECT: [
            MessageHandler(Filters.text, subject),
            CommandHandler('skip', skip_subject)
        ],
        PHOTO: [
            MessageHandler(Filters.photo, photo),
            CommandHandler('skip', skip_photo)
        ],
        LOCATION: [
            MessageHandler(Filters.location, location),
            CommandHandler('skip', skip_location),
        ],
        BIO: [
            MessageHandler(Filters.text & ~ Filters.command, bio)
        ],
    },
    fallbacks= [CommandHandler('cancel', cancel)]
)