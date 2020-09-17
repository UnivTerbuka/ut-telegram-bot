import os
import logging
from core.bot import UniversitasTerbukaBot
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    # Set these variable to the appropriate values
    TOKEN = os.environ.get('TOKEN')
    ut_bot = UniversitasTerbukaBot(TOKEN)
    ut_bot.polling()
