import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

import urllib
import json
import datetime
import time

from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        qurty = self.get_argument('q')
        url = 'https://api.github.com/search/repositories?q=%s+language:python&sort=stars&order=desc' % qurty

        client = tornado.httpclient.AsyncHTTPClient()
        request = tornado.httpclient.HTTPRequest(url=url,
                                                 method='GET',
                                                 headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'},
                                                 request_timeout=10)
        client.fetch(request, callback=self.on_response)


    def on_response(self, response):
        json_data = json.loads(response.body)

        self.write('''
                <div style="text-align: center">
                    <div style="font-size: 72px">search %s</div>
                    <div style="font-size: 144px">%d</div>
                    <div style="font-size: 24px">total_count</div>
                </div>
                ''' % (self.get_argument('q'), json_data['total_count']))
        self.finish()


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r'/', IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()