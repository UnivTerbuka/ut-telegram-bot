import logging
import os
import cherrypy
from core import SimpleWebsite, UniversitasTerbukaBot

BASE_PATH = os.path.dirname(__file__)
PATH = os.path.abspath(os.path.join(BASE_PATH, 'static'))


class Root(object):
    pass


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
    # cherrypy.tree.mount(SimpleWebsite(), "/")
    cherrypy.tree.mount(Root, '/', config={
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': PATH,
            'tools.staticdir.index': 'index.html',
        }
    })
    cherrypy.tree.mount(UniversitasTerbukaBot(TOKEN, NAME),
                        "/{}".format(TOKEN),
                        {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})
    cherrypy.engine.start()
