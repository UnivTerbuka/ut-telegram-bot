import os
from core import UniversitasTerbukaBot
from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
    # Set these variable to the appropriate values
    NAME = os.environ.get('NAME')
    TOKEN = os.environ.get('TOKEN')
    ut_bot = UniversitasTerbukaBot(TOKEN, NAME)
    ut_bot.polling()
