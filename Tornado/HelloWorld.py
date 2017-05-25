import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        raise tornado.web.HTTPError(400)

application = tornado.web.Application([
    (r"/",MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()