import datetime
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
import re

RAWG_GAME_URL = 'https://rawg.io/games/'
RAWG_DEVELOPERS_URL = 'https://rawg.io/developers/'
ELLIPSIS_FORMAT = '{}...'
ARBITRARY_PRETTY_LENGTH_LIMIT = 550
html_cleanup = re.compile('<.*?>')


def format_developer(developer: Developer) -> str:
    return '<a href="{}{}">{}</a>'.format(RAWG_DEVELOPERS_URL, developer.slug, developer.name)


def format_developers(developers: List[Developer]) -> str:
    if not developers or len(developers) == 0:
        return ''
    joined = ', '.join([format_developer(developer) for developer in developers])
    return '{}\n'.format(joined)


def format_released(released: datetime.date, tba: bool) -> str:
    return '<i>{}</i>\n'.format('TBA' if tba or not released else released)


def format_alternative_names(alternative_names: List[str]) -> str:
    if not alternative_names or len(alternative_names) == 0:
        return ''

    return '({})\n'.format(' / '.join(alternative_names))


def format_genres(genres: List[Genre]) -> str:
    if not genres or len(genres) == 0:
        return '\n\n'
    joined = ', '.join([genre.name for genre in genres])
    return '{}\n\n'.format(joined)


def format_description(description: str) -> str:
    if not description:
        return ''

    description = re.sub(html_cleanup, ' ', description)
    first_paragraph = description.find('\n')
    if first_paragraph == -1 and description != '' and len(description) > ARBITRARY_PRETTY_LENGTH_LIMIT:
        description = ELLIPSIS_FORMAT.format(description[:ARBITRARY_PRETTY_LENGTH_LIMIT])
    else:
        description = description[:first_paragraph]
    description = description.replace('<3', '❤️')\
        .replace('<', '')\
        .replace('>', '')
    return description


def format_text(game: Game) -> InputTextMessageContent:
    text = '<a href="{}{}"><b>{}</b></a>\n'.format(
        RAWG_GAME_URL,
        game.slug,
        game.name
    )
    text += format_alternative_names(game.alternative_names)
    text += format_released(game.released, game.tba)
    text += format_developers(game.developers)
    text += format_genres(game.genres)
    text += format_description(game.description_raw)

    if len(text) > constants.MAX_MESSAGE_LENGTH:
        text = ELLIPSIS_FORMAT.format(text[:constants.MAX_MESSAGE_LENGTH-4])

    return InputTextMessageContent(message_text=text, parse_mode=ParseMode.HTML)


def format_links(brief_stores: List[StoreBrief], stores: List[Store]) -> InlineKeyboardMarkup:
    store_names = {}
    store_buttons = []

    for brief_store in brief_stores:
        store_names[brief_store.id] = brief_store.name

    for index, store in enumerate(stores):
        button = InlineKeyboardButton(text=store_names[store.store_id], url=store.url.replace('http://', 'https://'))
        if index % 2 == 0:
            store_buttons.append([button])
        else:
            store_buttons[-1].append(button)

    return InlineKeyboardMarkup(store_buttons)
