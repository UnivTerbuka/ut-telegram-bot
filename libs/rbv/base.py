from requests import Session
from ..base import BaseRequests

DOMAIN = "http://pustaka.ut.ac.id"
INDEX_URL = "https://pustaka.ut.ac.id/reader/index.php"
READER_URL = "https://pustaka.ut.ac.id/reader/"
SESSION: Session = BaseRequests()
USERNAME = "mahasiswa"
PASSWORD = "utpeduli"
RETRY = 10
