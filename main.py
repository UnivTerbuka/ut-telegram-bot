import os
import logging
from core.bot import UniversitasTerbukaBot
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    # Set these variable to the appropriate values
    TOKEN = os.environ.get('TOKEN')
    ut_bot = UniversitasTerbukaBot(TOKEN)
    ut_bot.polling()
