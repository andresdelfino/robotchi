import logging


logger = logging.getLogger(__name__)


async def echo_message(update, context):
    # Only called when the the user sends the message to the bot in a
    # one-to-one chat

    user = update.message.from_user
    logger.info("Message from user %s is beding echoed", user.first_name)
    await update.message.reply_text(update.message.text)
