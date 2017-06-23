import tornado.web
from tornado.web import RequestHandler, asynchronous, HTTPError
from tornado.httpserver import HTTPServer
from tornado.options import define, options
from tornado.ioloop import IOLoop
from tornado.auth import *
from functools import *

define('port', default=8000, help='run on the given port', type=int)


class TwitterHandler(RequestHandler, TwitterMixin):
    @asynchronous
    def get(self, *args, **kwargs):
        oAuthToken = self.get_secure_cookie('oauth_token')
        oAuthSecret = self.get_secure_cookie('oauth_secret')
        userID = self.get_secure_cookie('user_id')

        if self.get_argument('oauth_token', None):
            self.get_authenticated_user(partial(self._twitter_on_auth))
            return
        elif oAuthToken and oAuthSecret:
            accessToken = {
                'key' : oAuthToken,
                'secret' : oAuthSecret
            }

            self.twitter_request('/users/show',
                                 access_token=accessToken,
                                 user_id=userID,
                                 callback=partial(self._twitter_on_user()))
            return

        self.authenticate_redirect()


    def _twitter_on_auth(self, user):
        if not user:
            self.clear_all_cookies()
            raise HTTPError(500, 'Twitter authentication failed')


        self.set_secure_cookie('user_id', str(user['id']))
        self.set_secure_cookie('oauth_token', user['access_token']['key'])
        self.set_secure_cookie('oauth_secret', user['access_token']['secret'])

        self.redirect('/')


    def _twitter_on_user(self, user):
        if not user:
            self.clear_all_cookies()
            raise HTTPError(500, "Couldn't retrieve user information")

        self.render('home.html', user=user)


class LogoutHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.clear_all_cookies()
        self.render('logout.html')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', TwitterHandler),
            (r'/logout', LogoutHandler)
        ]

        settings = {
            'twitter_consumer_key' : 'cWc3 ... d3yg',
            'twitter_consumer_secret' : 'nEoT ... cCXB4',
            'cookie_secret' : 'dzoRTcIETsil0pef3Ot8HwCFUUh/c0G8srmzs4UM2Kc=',
            'template_path' : 'templates',
        }

        tornado.web.Application.__init__(self, handlers=handlers, **settings)


if __name__ == '__main__':
    options.parse_command_line()
    http_server = HTTPServer(Application())
    http_server.listen(options.port)
    IOLoop.instance().start()
