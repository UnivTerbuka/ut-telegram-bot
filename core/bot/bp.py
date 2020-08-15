from flask import Blueprint, request
from .bot import UniversitasTerbukaBot

bp = Blueprint('bot', __name__)
bot = UniversitasTerbukaBot()


@bp.route(f"/{bot.TOKEN}", methods=['POST'])
def webhook():
    update = request.get_json()
    bot.process_update(update)
    return ''
