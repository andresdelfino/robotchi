import logging

from telegram import Update
from telegram.ext import CallbackContext


logger = logging.getLogger(__name__)


async def handle_start_command(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    await update.message.reply_text("This is the start function")
    logger.info("User %s called the start command", user.first_name)
