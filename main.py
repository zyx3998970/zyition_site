import os
import re
import tornado.httpserver
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url

location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)

def is_mobile(request):
	ua = request.headers.get('User-Agent')
    return is_mobile = bool(re.search(r'android|ipad|iphone', ua, re.I))

class PageNotFoundHandler(RequestHandler):
	def get(self):
		self.set_status(404)
		self.render('404.html', is_mobile=is_mobile(self.request))


class IndexHandler(RequestHandler):
    def get(self):
        self.render("index.html", is_mobile=is_mobile(self.request))

def make_app():
    settings = {
        "template_path": location('templates'),
        "compress_response": True,
        "default_handler_class": PageNotFoundHandler,
    }

    return Application([
        url(r"/", IndexHandler),
        ], **settings)

def main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8888)
    server.start(0)  # forks one process per cpu
    IOLoop.current().start()


if __name__ == '__main__':
    main()
