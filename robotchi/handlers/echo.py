import logging

from telegram import Update
from telegram.ext import CallbackContext


logger = logging.getLogger(__name__)


async def echo_message(update: Update, context: CallbackContext) -> None:
    # Only called when the the user sends the message to the bot in a
    # one-to-one chat

    user = update.message.from_user
    logger.info("Message from user %s is being echoed", user.first_name)
    await update.message.reply_text(update.message.text)
