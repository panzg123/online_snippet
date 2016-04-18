#encoding:utf-8
import motor
from tornado.gen import coroutine,Return
from time import time
from uuid import uuid1

class SnipetManager:
    def __init__(self,db=None):
        self.db =db or motor.MotorClient().code

    def generate_key(self):
        return uuid1().get_hex()

    @coroutine
    def post_new_code(self,author,title,content):
        snippet={}
        snippet['author']=author
        snippet['time'] = 111
        snippet['title'] = title
        snippet['content'] = content
        snippet_id = self.generate_key()
        snippet['snippet_id'] = snippet_id#暂时定100，需要唯一
        yield self.db.snippet.insert(snippet)
        raise Return(snippet_id)

    @coroutine
    def query_by_id(self,snippet_id):
        ret = yield  self.db.snippet.find_one({"snippet_id":snippet_id},{"_id":0})
        if ret:
            raise Return(ret)
        else:
            raise Return(None)
