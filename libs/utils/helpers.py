from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Job
from typing import Tuple


def build_menu(buttons=None,
               n_cols=1,
               header_buttons=None,
               footer_buttons=None):
    menu = []
    if buttons:
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        if type(header_buttons) == list:
            menu.insert(0, header_buttons)
        else:
            menu.insert(0, [header_buttons])
    if footer_buttons:
        if type(footer_buttons) == list:
            menu.append(footer_buttons)
        else:
            menu.append([footer_buttons])
    return menu


def cancel_markup(data: str, buttons=None, n_cols=1, text: str = 'Batal'):
    assert type(data) == str
    data = data.replace(' ', '_')
    data = data.replace('\n', '_')
    keyboard = [
        InlineKeyboardButton(
            text=text,
            callback_data=data if data.startswith('CANCEL|') else 'CANCEL|' +
            data)
    ]
    menu = build_menu(buttons=buttons, n_cols=n_cols, footer_buttons=keyboard)
    return InlineKeyboardMarkup(menu)


def jobs2markup(jobs: Tuple[Job]) -> InlineKeyboardMarkup:
    keyboard = []
    for job in jobs:
        button = InlineKeyboardButton(
            str(job.name),
            callback_data='CANCEL|{}'.format(job.name)
        )
        keyboard.append(button)
    menu = build_menu(keyboard, 2)
    return InlineKeyboardMarkup(menu)
