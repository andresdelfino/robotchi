import importlib.resources
import logging
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
    MEMES_DIR = 'meme'

    user = update.message.from_user
    user_tag = ' '.join(context.args)

    if user_tag.lower() in tag_dict.keys():
        logger.info("User %s used a matching tag", user.first_name)
        chosen_meme = random.choice(tag_dict[user_tag.lower()]) + ".jpg"
    else:
        logger.info("User %s didn't use a tag or it didn't match", user.first_name)
        memes = list(resource.name for resource in importlib.resources.files('robotchi').joinpath(MEMES_DIR).iterdir())
        chosen_meme = random.choice(memes)

    with importlib.resources.files('robotchi').joinpath(MEMES_DIR, chosen_meme).open('rb') as f:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=f,
        )

    logger.info("User %s called the get_meme command", user.first_name)
