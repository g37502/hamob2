# -*- coding:utf-8 -*-
#  2020/12/10 
#  raids.py
#  
# author:gyl
from django.conf import settings
import redis
class redis_h(object):
    def __init__(self,host,port,db):
        self.host = host
        self.port = port
        self.db = db
        self._registry = []
    def connect_redis(self):
        pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db,decode_responses=True)
        red = redis.Redis(connection_pool=pool)
        return red

# rehis_h = redis_h(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB).connect_redis()
rehis_h = redis_h(host='112.13.92.136', port=6379, db=1).connect_redis()