import logging
import os
import random


logger = logging.getLogger(__name__)


tag_dict = dict()
tag_dict["surprise"] = ["andy_dwyer_surprise"]
tag_dict["angry"] = ["angry_bob"]
tag_dict["handshake"] = ["epic_handshake"]
tag_dict["old"] = ["old_lady"]
tag_dict["simply"] = ["one_does_not_simply"]
tag_dict["doubt"] = ["philosoraptor"]
tag_dict["suspicious"] = ["suspicious_fry"]
tag_dict["sarcasm"] = ["that_would_be_great"]
tag_dict["calculus"] = ["trigonometry"]
tag_dict["unsettled"] = ["unsettled_tom"]


async def handle_meme_command(update, context):
    MEMES_DIR = os.path.join(os.getcwd(), 'meme')

    user = update.message.from_user
    user_tag = ' '.join(context.args)

    if user_tag.lower() in tag_dict.keys():
        logger.info("User %s used a matching tag", user.first_name)
        chosen_meme = random.choice(tag_dict[user_tag.lower()]) + ".jpg"
    else:
        logger.info("User %s didn\'t use a tag or it didn\'t match", user.first_name)
        memes = [meme for meme in os.listdir(MEMES_DIR)]
        chosen_meme = random.choice(memes)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(os.path.join(MEMES_DIR, chosen_meme), 'rb'),
    )

    logger.info("User %s called the get_meme command", user.first_name)
