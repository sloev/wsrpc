import threading
import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer
import time
import logging
from handler import WsRPCHandler
from auth import authenticator
import tornado.options
from tornado.log import enable_pretty_logging
enable_pretty_logging()
logging.getLogger().setLevel(logging.INFO)

def create_app(application_settings=None):
    settings = {
            'authenticator' : authenticator
            }
    #if given for example a new auth function then override existing
    if isinstance(application_settings, dict):
        settings.update(application_settings)

    application=tornado.web.Application([
        (r'/',WsRPCHandler),
        ],
        **settings
        )
    return application

def create_server(app, port=8888):
    server = HTTPServer(app)
    server.listen(port)
    return server

def start_ioloop():
    logging.info("ws_rpc ioloop started")
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()
    logging.info("ws_rpc ioloop stopped")

def stop_ioloop():
    logging.info("stopping ws_rpc ioloop")
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.add_callback(ioloop.stop)

def main():
    tornado.options.parse_command_line()
    print "ws_rpc main is running, exit with ctrl+c"
    logging.info("creating application")
    app = create_app()
    logging.info("creating server")
    server = create_server(app)
    logging.info("starting ioloop thread")
    thread  = threading.Thread(target=start_ioloop)
    thread.start()
    try:
        while(True):
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()
        stop_ioloop()
        thread.join()

if __name__ == "__main__":
    logging.info("running main")
    main()
