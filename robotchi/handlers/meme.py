import logging
import os
import random

from telegram import Update
from telegram.ext import CallbackContext


logger = logging.getLogger(__name__)


tag_dict = {
    "angry": ["angry_bob"],
    "calculus": ["trigonometry"],
    "doubt": ["philosoraptor"],
    "handshake": ["epic_handshake"],
    "old": ["old_lady"],
    "sarcasm": ["that_would_be_great"],
    "simply": ["one_does_not_simply"],
    "surprise": ["andy_dwyer_surprise"],
    "suspicious": ["suspicious_fry"],
    "unsettled": ["unsettled_tom"],
}


async def handle_meme_command(update: Update, context: CallbackContext) -> None:
    MEMES_DIR = os.path.join(os.getcwd(), 'meme')

    user = update.message.from_user
    user_tag = ' '.join(context.args)

    if user_tag.lower() in tag_dict.keys():
        logger.info("User %s used a matching tag", user.first_name)
        chosen_meme = random.choice(tag_dict[user_tag.lower()]) + ".jpg"
    else:
        logger.info("User %s didn't use a tag or it didn't match", user.first_name)
        memes = [meme for meme in os.listdir(MEMES_DIR)]
        chosen_meme = random.choice(memes)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(os.path.join(MEMES_DIR, chosen_meme), 'rb'),
    )

    logger.info("User %s called the get_meme command", user.first_name)
