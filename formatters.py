from typing import List

from rawg.game import Game
from rawg.genre import Genre
from rawg.developer import Developer
from rawg.store import Store
from rawg.store_brief import StoreBrief
from telegram import InputTextMessageContent
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import ParseMode
from telegram import constants

RAWG_GAME_URL = 'https://rawg.io/games/'
RAWG_DEVELOPERS_URL = 'https://rawg.io/developers/'


def format_developer(developer: Developer) -> str:
    return '<a href="{}{}">{}</a>'.format(RAWG_DEVELOPERS_URL, developer.slug, developer.name)


def format_developers(developers: List[Developer]) -> str:
    return ', '.join([format_developer(developer) for developer in developers])


def format_genres(genres: List[Genre]) -> str:
    return ', '.join([genre.name for genre in genres])


def format_text(game: Game) -> InputTextMessageContent:
    text = '<a href="{}{}"><b>{}</b></a>\n'.format(
        RAWG_GAME_URL,
        game.slug,
        game.name
    )
    if game.alternative_names and len(game.alternative_names) != 0:
        text += '({})\n'.format(' / '.join(game.alternative_names))
    text += '<i>{}</i>\n'.format('TBA' if game.tba or not game.released else game.released)
    text += '{}\n'.format(format_developers(game.developers))
    text += '{}\n\n'.format(format_genres(game.genres))

    description = game.description_raw
    first_paragraph = description.find('\n')
    if first_paragraph == -1 and description != '':
        description = '{}...'.format(description[:200])
    else:
        description = description[:first_paragraph]
    text += description

    text = text[:constants.MAX_MESSAGE_LENGTH]

    return InputTextMessageContent(message_text=text, parse_mode=ParseMode.HTML)


def format_links(brief_stores: List[StoreBrief], stores: List[Store]) -> InlineKeyboardMarkup:
    store_names = {}
    store_buttons = []

    for brief_store in brief_stores:
        store_names[brief_store.id] = brief_store.name

    for store in stores:
        button = InlineKeyboardButton(text=store_names[store.store_id], url=store.url)
        store_buttons.append([button])

    return InlineKeyboardMarkup(store_buttons)
