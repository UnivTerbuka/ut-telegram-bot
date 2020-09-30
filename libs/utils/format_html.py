def code(text: str) -> str:
    return f"<code>{text}</code>"


def href(text: str, href: str) -> str:
    return f'<a href="{href}">{text}</a>'


def italic(text: str) -> str:
    return f"<i>{text}</i>"


def bold(text: str) -> str:
    return f"<b>{text}</b>"


def underline(text: str) -> str:
    return f"<u>{text}</u>"
