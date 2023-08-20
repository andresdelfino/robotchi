import logging
import re
import urllib.request

from bs4 import BeautifulSoup
from telegram import Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext


logger = logging.getLogger(__name__)


def download_wiki(element, url):
    try:
        response = urllib.request.urlopen(url + element)
        soup = BeautifulSoup(response.read(), "html.parser")
        # TODO: check when the term is ambiguous
        message = soup.find("div", id="bodyContent") \
            .find("div", id="mw-content-text") \
            .find("div", {"class": "mw-parser-output"}) \
            .find("p").get_text()
        message = re.sub('\[\d\]', '', message)  # Pycharm me está tirando erroes en este RE
    except urllib.error.HTTPError:
        message = f"Wikipedia has no information about {element}"
    return message


async def handle_wiki_command(update: Update, context: CallbackContext) -> None:
    url = "https://es.wikipedia.org/wiki/"
    user = update.message.from_user
    element = ' '.join(context.args)
    message = download_wiki(element, url)
    try:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message
        )
    except BadRequest:
        logger.info("There was an issue with the message")
    logger.info("User %s called the get_wiki command", user.first_name)
