from telegram import ReplyKeyboardRemove, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
SUBJECT, PHOTO, LOCATION, COMMENT = range(4)


def talk(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s wants to talk", user.first_name)
    update.message.reply_text(
        'Hello. I am a bot. What do you want to talk about?',
        reply_markup=ReplyKeyboardRemove(),
    )
    return SUBJECT


def subject(update: Update, context: CallbackContext):
    user = update.message.from_user
    chosen_subject = update.message.text
    logger.info("User %s chose to talk about %s", user.first_name, chosen_subject)
    # url = "https://es.wikipedia.org/wiki/"
    # route = f"wiki/{chosen_subject}.html"  # "path" coflicts with the module of the same name
    # message = download_wiki(chosen_subject, route, url)
    update.message.reply_text(
        'Here is some info about ' + chosen_subject + ':' + '\n\n'
    )
    return PHOTO


def skip_subject(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s does not want to talk", user.first_name)
    update.message.reply_text(
        'Ok, no problem. Please send me your picture so I can know you, or send /skip if you don\'t want to'
    )
    return PHOTO


def photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s is called: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text(
        'Nice picture. Please send me your location, or send /skip if you don\'t want to'
    )
    return LOCATION


def skip_photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s did not send a photo", user.first_name)
    update.message.reply_text(
        'ok, no problem. Please send me your location please or send /skip if you don\'t want to'
    )
    return LOCATION


def location(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of user %s is latitude %f / longitude %f", user.first_name,
                user_location.latitude, user_location.longitude)
    update.message.reply_text(
        'Hey, that is a nice place. Is there anything else you want to tell me?'
    )
    return COMMENT


def skip_location(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s did not send a location", user.first_name)
    update.message.reply_text(
        'Ok, no problem. Is there anything else you want to tell me?'
    )
    return COMMENT


def comment(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("Comment by %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Ok, I will take that into consideration. Bye!'
    )
    return ConversationHandler.END


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
        COMMENT: [
            MessageHandler(Filters.text & ~ Filters.command, comment)
        ],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
