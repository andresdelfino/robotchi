import logging
import uuid

from telegram import InlineQueryResultPhoto


logger = logging.getLogger(__name__)


memes = [
    {
        'id': str(uuid.uuid4()),
        'name': 'aliens',
        'photo_url': 'https://www.meme-arsenal.com/memes/6b8f460f481aa48441d8dc6d88d0a041.jpg',
        'thumb_url': 'https://www.meme-arsenal.com/memes/6b8f460f481aa48441d8dc6d88d0a041.jpg',
        'tags': {
            'aliens',
        }
    },
    {
        'id': str(uuid.uuid4()),
        'name': 'but_it_s_honest_work',
        'photo_url': 'https://www.meme-arsenal.com/memes/333258e655f5d613b7ee4a0663e0506d.jpg',
        'thumb_url': 'https://www.meme-arsenal.com/memes/333258e655f5d613b7ee4a0663e0506d.jpg',
        'tags': {
            *"but it's honest work".split(),
        }
    },
    {
        'id': str(uuid.uuid4()),
        'name': 'not_sure_if',
        'photo_url': 'https://www.meme-arsenal.com/memes/389f398c7bf55ae32a8a326031af2c32.jpg',
        'thumb_url': 'https://www.meme-arsenal.com/memes/389f398c7bf55ae32a8a326031af2c32.jpg',
        'tags': {
            'fry',
            *'not sure if'.split(),
            'futurama',
        },
    },
    {
        'id': str(uuid.uuid4()),
        'name': 'shut_up_and_take_my_money',
        'photo_url': 'https://www.meme-arsenal.com/memes/ed3a49701d7dce8d9d1cb5f74a7f79f8.jpg',
        'thumb_url': 'https://www.meme-arsenal.com/memes/ed3a49701d7dce8d9d1cb5f74a7f79f8.jpg',
        'tags': {
            'fry',
            *'shut up and take my money'.split(),
            'futurama',
        }
    },
    {
        'id': str(uuid.uuid4()),
        'name': 'spider_man_pointing_at_spider_man',
        'photo_url': 'https://www.meme-arsenal.com/memes/2332a9b45fea20c7f92ea5324dd6be49.jpg',
        'thumb_url': 'https://www.meme-arsenal.com/memes/2332a9b45fea20c7f92ea5324dd6be49.jpg',
        'tags': {
            'spiderman',
            'spider-man',
            'doble',
            'duplicado',
            'igual',
        }
    },
]


async def handle_inline_query(update, context):
    query = update.inline_query.query
    if update.message and update.message.from_user:
        logger.info("User %s is making an inline query", update.message.from_user.first_name)
    else:
        logger.info("Someone is making an inline query")
    logger.info("The query is: %s ", query)

    if query == '':
        return

    results = []

    tags = set(query.lower().split())

    print('Memes matched:')

    for meme in memes:
        if query == 'all' or tags <= meme['tags']:
            print('*', meme['name'])
            results.append(
                InlineQueryResultPhoto(
                    id=meme['id'],
                    photo_url=meme['photo_url'],
                    thumbnail_url=meme['thumb_url'],
                ),
            )

    if not results:
        print('None')

    await update.inline_query.answer(results, cache_time=0)
