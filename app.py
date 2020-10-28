import logging
from dataclasses import asdict
from dotenv import load_dotenv
from flask import Flask, redirect, request, abort, make_response, jsonify
from werkzeug.routing import BaseConverter

from core import UniversitasTerbukaBot
from config import NAME, TOKEN

from libs.rbv.buku import Buku
from libs.rbv.modul import Modul

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

app = Flask(__name__, static_url_path="", static_folder="static")


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters["regex"] = RegexConverter

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


@app.route('/book/<regex("[A-Z]{4}[0-9]{4,6}"):book>', methods=["GET"])
def pustaka_buku(book: str):
    if not Modul.is_valid(book):
        abort(404)
    b = Buku(book)
    if not b:
        abort(404)
    return jsonify(asdict(b))


@app.route(
    '/img/<regex("[A-Z]{4}[0-9]{4,6}"):book>/<regex("[a-zA-Z0-9]+"):modul>/<int:page>',
    methods=["GET"],
)
def pustaka_image(book: str, modul: str, page: int):
    if not Modul.is_valid(book):
        abort(404)
    m = Modul(subfolder=book, doc=modul)
    try:
        s = m.get_page(page)
    except Exception:
        abort(404)
    return redirect("/" + "/".join(s.split("/")[3:]))


@app.route(
    '/txt/<regex("[A-Z]{4}[0-9]{4,6}"):book>/<regex("[a-zA-Z0-9]+"):modul>/<int:page>',
    methods=["GET"],
)
def pustaka_txt(book: str, modul: str, page: int):
    if not Modul.is_valid(book):
        abort(404)
    m = Modul(subfolder=book, doc=modul)
    response = make_response(m.get_page_text(page, header=False), 200)
    response.mimetype = "text/plain"
    return response


@app.route(
    '/json/<regex("[A-Z]{4}[0-9]{4,6}"):book>/<regex("[a-zA-Z0-9]+"):modul>/<int:page>',
    methods=["GET"],
)
def pustaka_json(book: str, modul: str, page: int):
    if not Modul.is_valid(book):
        abort(404)
    m = Modul(subfolder=book, doc=modul)
    return jsonify(m.get_page_json(page))


if __name__ == "__main__":
    app.run()
