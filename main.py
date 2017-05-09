import os
import random
import re

import tornado.httpserver
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler as OriginalRequestHandler
from tornado.web import Application, url

location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)


def is_mobile(request):
    ua = request.headers.get('User-Agent')
    return bool(re.search(r'android|ipad|iphone', ua, re.I))

class RequestHandler(OriginalRequestHandler):
    """Make some hack."""
    def get_template_namespace(self):
        namespace = super(RequestHandler, self).get_template_namespace()
        customized_context = dict(is_mobile=is_mobile(self.request))
        namespace.update(customized_context)
        return namespace


class PageNotFoundHandler(RequestHandler):
    def get(self):
        self.set_status(404)
        self.render('404.html')


class IndexHandler(RequestHandler):
    def get(self):
        self.render("index.html")


class LotteryHandler(RequestHandler):
    RED_BALL_RANGE = tuple(range(1, 34))
    RED_BALL_COUNT = 6
    BLUE_BALL_RANGE = tuple(range(1, 17))

    def get(self):
        red_balls = sorted(random.sample(self.RED_BALL_RANGE, self.RED_BALL_COUNT))
        blue_ball = random.choice(self.BLUE_BALL_RANGE)
        context = dict(red_balls=red_balls, blue_ball=blue_ball)
        self.render("lottery.html", **context)


def make_app():
    settings = {
        "template_path": location('templates'),
        "static_path": location('static'),
        "compress_response": True,
        "default_handler_class": PageNotFoundHandler,
    }

    return Application([
        url(r"/", IndexHandler),
        url(r"/lottery/double-color-ball/", LotteryHandler),
        ], **settings)

def main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8888)
    if app.settings.get('debug'):
        server.start() # if debug, does not use multi-process
    else:
        server.start(0)  # forks one process per cpu
    IOLoop.current().start()


if __name__ == '__main__':
    main()
