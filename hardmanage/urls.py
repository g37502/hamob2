# -*- coding:utf-8 -*-
#  2020/12/9 
#  urls.py
#  
# author:gyl
from django.conf.urls import url
from hardmanage.views import hardfind,test
from hardmanage.views import test as hard_test


urlpatterns = [
url(r'^list/$', hardfind.hardfind_hamob, name='hardfind_hamob'),
url(r'^list/hard/save/(?P<pk>(\w*\.*)*)$', hardfind.hard_save, name='hardfind_save'),
url(r'^list/hard/del/(?P<pk>(\w*\.*)*)$', hardfind.hard_del, name='harddel_del'),
url(r'^list/hard/multip/$', hardfind.hard_multip, name='harddel_multip'),

# url(r'test/$', hard_test.Cbv.as_view(),),
# url(r'test/$', hardfind.test),
# url(r'test1/$', test.test),
# url(r'test/test/(?P<host>\*+)$', hardfind.test,),
]