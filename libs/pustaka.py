from dataclasses import asdict
from flask import Blueprint, abort, jsonify, make_response, redirect
from flask_cors import CORS
from libs.rbv.buku import Buku
from libs.rbv.modul import Modul

pustaka = Blueprint("pustaka", __name__)
CORS(pustaka)


@pustaka.route('/book/<regex("[A-Z]{4}[0-9]{4,6}"):book>', methods=["GET"])
def pustaka_buku(book: str):
    if not Modul.is_valid(book):
        abort(404)
    b = Buku(book)
    if not b:
        abort(404)
    return jsonify(asdict(b))


@pustaka.route(
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


@pustaka.route(
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


@pustaka.route(
    '/json/<regex("[A-Z]{4}[0-9]{4,6}"):book>/<regex("[a-zA-Z0-9]+"):modul>/<int:page>',
    methods=["GET"],
)
def pustaka_json(book: str, modul: str, page: int):
    if not Modul.is_valid(book):
        abort(404)
    m = Modul(subfolder=book, doc=modul)
    return jsonify(m.get_page_json(page))
