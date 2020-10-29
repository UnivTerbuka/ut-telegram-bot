import logging
from dotenv import load_dotenv
from flask import Flask, redirect, request
from flask_cors import CORS
from werkzeug.routing import BaseConverter

from libs.pustaka import pustaka

from core import UniversitasTerbukaBot
from config import NAME, TOKEN

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

app = Flask(__name__, static_url_path="", static_folder="static")
CORS(app, methods=["GET"])


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters["regex"] = RegexConverter

app.register_blueprint(pustaka, url_prefix="/pustaka")

bot = UniversitasTerbukaBot(TOKEN, NAME)
bot.start_dispatcher_thread()


@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    bot.process_update(update)
    return ""


@app.route("/")
def index():
    return redirect("index.html")


if __name__ == "__main__":
    app.run()
