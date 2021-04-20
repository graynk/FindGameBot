#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import Updater, CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import InlineQueryHandler
from telegram.error import TimedOut
from telegram import Update
from telegram import InlineQueryResultArticle
import os

import formatters
from rawg.games import Games
from rawg.stores import Stores
from rawg.game import Game
import requests

TOKEN = os.getenv('RAWG_BOT_TOKEN')
ADMIN_CHAT_ID = int(os.getenv('RAWG_ADMIN_ID'))
RAWG_API_KEY = os.getenv('RAWG_API_KEY')
RAWG_API_BASE_URL = 'https://api.rawg.io/api'
RAWG_API_GAMES_URL = RAWG_API_BASE_URL + '/games'
RAWG_API_GAME_URL = RAWG_API_GAMES_URL + '/{}'
RAWG_API_STORES_URL = RAWG_API_GAMES_URL + '/{}/stores'
PORT = int(os.environ.get('PORT', '5002'))
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

key_param = {
    'key': RAWG_API_KEY,
}


def start(update: Update, context: CallbackContext) -> None:
    me = context.bot.get_me().username
    text = 'This is as an inline bot, try searching with "@{} GTA 5", or something like that'.format(me)
    update.effective_message.reply_text(text)


def inline_search(update: Update, context: CallbackContext) -> None:
    params = {
        'search': update.inline_query.query,
        'key': RAWG_API_KEY,
        'page_size': 5,
    }
    games = Games.from_dict(
        requests.get(
            RAWG_API_GAMES_URL,
            params=params
        ).json()
    )
    queries = []
    for result in games.results:
        if not result.stores:
            continue
        stores = Stores.from_dict(
            requests.get(
                RAWG_API_STORES_URL.format(result.id),
                params=key_param
            ).json()
        )
        if not stores.results:
            continue

        game = Game.from_dict(
            requests.get(
                RAWG_API_GAME_URL.format(result.id),
                params=key_param
            ).json()
        )
        text = formatters.format_text(game)
        buttons = formatters.format_links([store.store for store in result.stores], stores.results)

        article = InlineQueryResultArticle(id=result.id, title=game.name, description=game.released or 'TBA',
                                           input_message_content=text, reply_markup=buttons,
                                           thumb_url=result.background_image)
        queries.append(article)

    update.inline_query.answer(queries)


def ping_me(update: Update, context: CallbackContext) -> None:
    if context.error is not TimedOut:
        err = str(context.error)
        print(err)
        if len(err) > 4000:
            return
        context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=err)


if __name__ == '__main__':
    start_handler = CommandHandler('start', start)
    inline_handler = InlineQueryHandler(inline_search, run_async=True)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(inline_handler)
    dispatcher.add_error_handler(ping_me)

    updater.start_polling()
    updater.idle()
