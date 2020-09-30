from requests import Session
from ..base import BaseRequests

DOMAIN = "http://www.pustaka.ut.ac.id"
INDEX_URL = "http://www.pustaka.ut.ac.id/reader/index.php"
READER_URL = "http://www.pustaka.ut.ac.id/reader/"
SESSION: Session = BaseRequests()
USERNAME = "mahasiswa"
PASSWORD = "utpeduli"
RETRY = 10
