import logging
import os
import cherrypy
from core import SimpleWebsite, UniversitasTerbukaBot

if __name__ == "__main__":
    # Set these variable to the appropriate values
    NAME = os.environ.get('NAME')
    TOKEN = os.environ.get('TOKEN')

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up the cherrypy configuration
    cherrypy.config.update({'server.socket_host': '0.0.0.0', })
    cherrypy.config.update({'server.socket_port': int(PORT), })
    cherrypy.tree.mount(SimpleWebsite(), "/")
    cherrypy.tree.mount(UniversitasTerbukaBot(TOKEN, NAME),
                        "/{}".format(TOKEN),
                        {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})
    cherrypy.engine.start()
