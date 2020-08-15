import os
import sys


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

HTML_PARSER = 'lxml'
ROOT_PATH = get_script_path()
STATIC_PATH = os.path.join(ROOT_PATH, 'static')
IMG_PATH = os.path.join(STATIC_PATH, 'images')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'
}
CALLBACK_SEPARATOR = '|'
USERNAME_RBV = 'mahasiswa'
PASSWORD_RBV = 'utpeduli'
NAME = os.environ.get('NAME', 'universitas-terbuka-bot')
TOKEN = os.environ.get('TOKEN')
BASE_URL = "https://{}.herokuapp.com/".format(NAME)
IMG_URL = BASE_URL + 'images/'
WEBHOOK_URL = "https://{}.herokuapp.com/{}".format(NAME, TOKEN)
URL_LOGO = 'https://upload.wikimedia.org/wikipedia/en/2/21/Universitas-terbuka-logo.jpg'
BOT_USERNAME = os.environ.get('BOT_USERNAME', 'UniversitasTerbukaBot')