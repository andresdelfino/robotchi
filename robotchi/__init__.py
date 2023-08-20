import logging
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    InlineQueryHandler,
    MessageHandler,
    filters,
)

from .handlers.echo import echo_message
from .handlers.inline_query import handle_inline_query
from .handlers.meme import handle_meme_command
from .handlers.start import handle_start_command
from .handlers.wiki import handle_wiki_command


logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    bot_token = os.environ['BOT_TOKEN']

    application = Application.builder().token(bot_token).build()

    start_handler = CommandHandler('start', handle_start_command)
    echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message)
    meme_handler = CommandHandler('meme', handle_meme_command)
    wiki_handler = CommandHandler('wiki', handle_wiki_command)
    inline_query_handler = InlineQueryHandler(handle_inline_query)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(meme_handler)
    application.add_handler(wiki_handler)
    application.add_handler(inline_query_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
