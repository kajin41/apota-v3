__author__ = 'Madness'

from APP import app

from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application
import tornado.options


class MainHandler(RequestHandler):
    def get(self):
        tornado.options.define_logging_options()

tr = WSGIContainer(app)

application = Application(
    [
        (r"/tornado", MainHandler),
        (r".*", FallbackHandler, dict(fallback=tr)),
    ]
)

if __name__ == "__main__":
    application.listen(8000)
    IOLoop.instance().start()

