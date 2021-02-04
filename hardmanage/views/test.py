# -*- coding:utf-8 -*-
#  2020/12/23 
#  test.py
#  
# author:gyl
from django.views import View
from django.shortcuts import HttpResponse,render
# from
# def test(request):
#     obj = mo
class MyBaseView(object):
    def dispatch(self, request, *args, **kwargs):
        print('before')
        ret = super(MyBaseView,self).dispath(request, *args, **kwargs)
        print('after')
        return ret
class Cbv(View):
    # def dispatch(self, request, *args, **kwargs):
    #     #     # print('before')
    #     #     ret = super(Cbv,self).dispatch(request, *args, **kwargs)
    #     #     # print('after')
    #     #     return ret
    def get(self,request):
        return render(request, 'hardmanage/cvb.html')
    def post(self,request):
        return HttpResponse('i am post')
    def put(self,request):
        print('i am put')
        return HttpResponse('i am put')
    def delete(self,request):
        print('delete')
        return HttpResponse('i am delete')
from django.db import models
from hardmanage.models import *
# from app01.models import *
# def test(request):
#     person = Person.objects.first()
#     book = person.person_book.first()
#     print(book.title,type(person))
#     return HttpResponse('book')