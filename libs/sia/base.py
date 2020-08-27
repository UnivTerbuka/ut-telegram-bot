from requests import Session
from logging import Logger


class BaseSia:
    logger: Logger = None
    session: Session = None
