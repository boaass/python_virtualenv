from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import RequestHandler, asynchronous, Application
from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)


class MainHandler(RequestHandler):
    def get(self):
        cookie = self.get_secure_cookie('count')
        count = int(cookie) + 1 if cookie else 1

        countString = '1 time' if count == 1 else '%d times' % count
        self.set_secure_cookie('count', str(count))

        self.write(
            "<html><head><title>Cookie Counter</title></head>"
            "<body><h1>You've viewed this page %s times.</h1>" % countString +
            "</body></html>"
        )


if __name__ == '__main__':
    options.parse_command_line()

    settings = dict(cookie_secret='dzoRTcIETsil0pef3Ot8HwCFUUh/c0G8srmzs4UM2Kc=')
    http_server = HTTPServer(Application(
        handlers=[(r'/', MainHandler)],
        **settings
    ))
    http_server.listen(options.port)
    IOLoop.instance().start()
