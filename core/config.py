import os
import sys


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


ROOT_PATH = get_script_path()
STATIC_PATH = os.path.join(ROOT_PATH, 'static')
IMG_PATH = os.path.join(STATIC_PATH, 'images')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'
}
CALLBACK_SEPARATOR = '|'
USERNAME_RBV = 'mahasiswa'
PASSWORD_RBV = 'utpeduli'