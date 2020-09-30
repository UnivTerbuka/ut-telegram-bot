from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Job
from typing import List, Optional, Tuple, Union

from config import CALLBACK_SEPARATOR


def make_button(
    text, callback_data: str = None, url: str = None
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text=text, callback_data=callback_data, url=url)]]
    )


def build_menu(
    buttons: Optional[List[InlineKeyboardButton]] = None,
    n_cols: int = 1,
    header_buttons: Union[List[InlineKeyboardButton], InlineKeyboardButton] = None,
    footer_buttons: Union[List[InlineKeyboardButton], InlineKeyboardButton] = None,
) -> List[List[InlineKeyboardButton]]:
    menu = list()
    if buttons:
        menu = [buttons[i : i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        if type(header_buttons) is list:
            menu.insert(0, header_buttons)
        else:
            menu.insert(0, [header_buttons])
    if footer_buttons:
        if type(footer_buttons) is list:
            menu.append(footer_buttons)
        else:
            menu.append([footer_buttons])
    return menu


def cancel_markup(data: str, buttons=None, n_cols=1, text: str = "Batal"):
    assert type(data) == str
    data = data.replace(" ", "_")
    data = data.replace("\n", "_")
    keyboard = [
        InlineKeyboardButton(
            text=text,
            callback_data=data if data.startswith("CANCEL|") else "CANCEL|" + data,
        )
    ]
    menu = build_menu(buttons=buttons, n_cols=n_cols, footer_buttons=keyboard)
    return InlineKeyboardMarkup(menu)


def jobs2markup(jobs: Tuple[Job]) -> InlineKeyboardMarkup:
    keyboard = []
    for job in jobs:
        button = InlineKeyboardButton(
            str(job.name), callback_data="CANCEL|{}".format(job.name)
        )
        keyboard.append(button)
    menu = build_menu(keyboard, 2)
    return InlineKeyboardMarkup(menu)


def make_data(*args: Union[str, int], sep: str = CALLBACK_SEPARATOR) -> str:
    return sep.join(map(str, args))
