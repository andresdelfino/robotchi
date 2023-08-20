import logging

from telegram import (
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)


logger = logging.getLogger(__name__)
SUBJECT, PHOTO, LOCATION, COMMENT = range(4)


async def talk(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s wants to talk", user.first_name)
    await update.message.reply_text(
        'Hello. I am a bot. What do you want to talk about?',
        reply_markup=ReplyKeyboardRemove(),
    )
    return SUBJECT


async def subject(update: Update, context: CallbackContext):
    user = update.message.from_user
    chosen_subject = update.message.text
    logger.info("User %s chose to talk about %s", user.first_name, chosen_subject)
    # url = "https://es.wikipedia.org/wiki/"
    # route = f"wiki/{chosen_subject}.html"  # "path" coflicts with the module of the same name
    # message = download_wiki(chosen_subject, route, url)
    await update.message.reply_text(
        'Here is some info about ' + chosen_subject + ':' + '\n\n'
    )
    return PHOTO


async def skip_subject(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s does not want to talk", user.first_name)
    await update.message.reply_text(
        'Ok, no problem. Please send me your picture so I can know you, or send /skip if you don\'t want to'
    )
    return PHOTO


async def photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s is called: %s", user.first_name, 'user_photo.jpg')
    await update.message.reply_text(
        'Nice picture. Please send me your location, or send /skip if you don\'t want to'
    )
    return LOCATION


async def skip_photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s did not send a photo", user.first_name)
    await update.message.reply_text(
        'ok, no problem. Please send me your location please or send /skip if you don\'t want to'
    )
    return LOCATION


async def location(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of user %s is latitude %f / longitude %f", user.first_name,
                user_location.latitude, user_location.longitude)
    await update.message.reply_text(
        'Hey, that is a nice place. Is there anything else you want to tell me?'
    )
    return COMMENT


async def skip_location(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s did not send a location", user.first_name)
    await update.message.reply_text(
        'Ok, no problem. Is there anything else you want to tell me?'
    )
    return COMMENT


async def comment(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("Comment by %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        'Ok, I will take that into consideration. Bye!'
    )
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s cancelled the conversation", user.first_name)
    await update.message.reply_text(
        'Ok, I hope you have a nice day', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('talk', talk)],
    states={
        SUBJECT: [
            MessageHandler(filters.TEXT, subject),
            CommandHandler('skip', skip_subject)
        ],
        PHOTO: [
            MessageHandler(filters.PHOTO, photo),
            CommandHandler('skip', skip_photo)
        ],
        LOCATION: [
            MessageHandler(filters.LOCATION, location),
            CommandHandler('skip', skip_location),
        ],
        COMMENT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, comment)
        ],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
