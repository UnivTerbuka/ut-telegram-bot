from flask import Blueprint, jsonify, abort
from requests import get
from ujson import loads

covid = Blueprint("covid", __name__)
COVID_API_URL = "https://data.covid19.go.id/public/api/update.json"


@covid.route('/')
def get_update():
    res = get(COVID_API_URL)
    if not res.ok:
        abort()
    return jsonify(loads(res.text))
