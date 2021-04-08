# -*- coding:utf-8 -*-
#  2020/12/10 
#  raids.py
#  
# author:gyl
from django.conf import settings
import redis
class redis_h(object):
    def __init__(self,host,port,db,decode_responses=False):
        self.host = host
        self.port = port
        self.db = db
        self._registry = []
        self.decode_responses=decode_responses
    def connect_redis(self):
        pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db,decode_responses=self.decode_responses)
        # pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db,decode_responses=True)
        red = redis.Redis(connection_pool=pool)
        return red

# rehis_h = redis_h(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB).connect_redis()
host=settings.REDIS_HOST
port=settings.REDIS_PORT
rehis_h = redis_h(host=host, port=port, db=1,decode_responses=True).connect_redis()
rehis_zero_pic = redis_h(host=host, port=port, db=0, decode_responses=True).connect_redis()
rehis_zero = redis_h(host=host, port=port, db=0).connect_redis()