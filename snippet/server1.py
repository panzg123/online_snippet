#encoding:utf-8
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.gen import coroutine
from manager import SnipetManager
import utils


class MainHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        code_list = yield self.application.db.return_index_code()
        if code_list:
            self.render('list.html',code_list=code_list)
        else:
            self.write('hello world')
class PostHandler(tornado.web.RequestHandler):
    """发布新的代码"""
    @coroutine
    def get(self):
		self.write('''
		    <form method="post">
				<input type="text" name="title">
				<input type="text" name="content">
				<input type="submit">
			</form>''')

    @coroutine
    def post(self):
        title = self.get_argument('title')
        content = self.get_argument('content')
        print title
        print content
        ret_id = yield self.application.db.post_new_code("panzg",title,content)
        self.redirect(utils.get_post_url(ret_id))
        # self.write(ret_id)
        # self.finish()

class QueryHandler(tornado.web.RequestHandler):
    """查询显示发布的代码"""
    @coroutine
    def get(self):
        snippet_id = self.get_argument('id')
        snippet = yield self.application.db.query_by_id(snippet_id)
        if snippet:
            self.write(snippet)
        else:
            self.write('null')
        self.finish()

    def post(self):
        pass


class Application(tornado.web.Application):
    def __init__(self):
        handlers=[
            (r"/", MainHandler),
            (r"/post", PostHandler),
            (r"/query", QueryHandler)
        ]
        tornado.web.Application.__init__(self,handlers)
        self.db = SnipetManager()

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()