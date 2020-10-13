import os
from telegram.ext import PicklePersistence

if "TOKEN" not in os.environ:
    from dotenv import load_dotenv

    load_dotenv()


def get_script_path():
    return os.path.dirname(__file__)


ROOT_PATH = get_script_path()
STATIC_PATH = os.path.join(ROOT_PATH, "static")
IMG_PATH = os.path.join(STATIC_PATH, "images")
RES_PATH = os.path.join(STATIC_PATH, "resources")
PERSISTENCE = PicklePersistence("data.persist", store_user_data=False)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0"  # NOQA
}
CALLBACK_SEPARATOR = "|"
USERNAME_RBV = "mahasiswa"
PASSWORD_RBV = "utpeduli"
NAME = os.environ.get("NAME")
TOKEN = os.environ.get("TOKEN")
POLR_KEY = os.environ.get("POLR")
BASE_URL = "https://{}.herokuapp.com/".format(NAME)
IMG_URL = BASE_URL + "images/"
DOMAIN = "https://{}.herokuapp.com/".format(NAME)
WEBHOOK_URL = DOMAIN + str(TOKEN)
URL_LOGO = "https://upload.wikimedia.org/wikipedia/en/2/21/Universitas-terbuka-logo.jpg"  # NOQA
BOT_USERNAME = os.environ.get("BOT_USERNAME", "UniversitasTerbukaBot")
DEVS = [529004070]
BLEACH_CONFIG = {
    "tags": ["a", "b", "i", "u"],
    "attributes": {"a": ["href"]},
    "strip": True,
}
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.sqlite")
MOODLE_D = "https://elearning.ut.ac.id/"
MOODLE_URL = "https://elearning.ut.ac.id/webservice/rest/server.php"
PUSTAKA_URL = "http://www.pustaka.ut.ac.id/"
