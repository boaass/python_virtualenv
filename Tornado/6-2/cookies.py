from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, authenticated
from tornado.options import define, options
import os.path


define('port', default=8000, help='run on the given port', type=int)


class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('username')


class LoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('login.html')


    def post(self, *args, **kwargs):
        self.set_secure_cookie('username', self.get_argument('username'))
        self.redirect('/')


class WelcomeHandler(BaseHandler):
    @authenticated
    def get(self, *args, **kwargs):
        self.render('index.html', user=self.current_user)


class LogoutHandler(BaseHandler):
    def get(self, *args, **kwargs):
        if self.get_argument('logout', None):
            self.clear_cookie('username')
            self.redirect('/')


if __name__ == '__main__':
    options.parse_command_line()

    settings = {
        'template_path' : os.path.join(os.path.dirname(__file__), 'templates'),
        'cookie_secret' : 'dzoRTcIETsil0pef3Ot8HwCFUUh/c0G8srmzs4UM2Kc=',
        'xsrf_cookies': True,
        'login_url' : '/login'
    }

    application = Application([
        (r'/', WelcomeHandler),
        (r'/login', LoginHandler),
        (r'/logout', LoginHandler)
    ], **settings)

    http_server = HTTPServer(application)
    http_server.listen(options.port)
    IOLoop.instance().start()

