#!/usr/bin/env python
# coding=utf-8
'''
@auhor: gyl
@file: .py
@data: 2021/3/17 
@desc:
'''
# import lib
from stark.service.stark import StarkConfig,Option
from business_func.models import *
from django.conf.urls import url
from django.shortcuts import render,HttpResponse,redirect
from stark.service.stark import site
from tool.raids_h import rehis_h,rehis_zero,rehis_zero_pic
from django.utils.safestring import mark_safe
from django.urls import reverse
from stark.utils.pagination import Pagination
import base64,time
from urllib.parse import urlparse

class Row_type(object):
    def __init__(self, data_list,config,query_dict):
        self.data_list= data_list
        self.query_dict = query_dict
        # logger.debug(type(self.data_list))
    def __iter__(self):
        yield '<div class="whole">'
        tatal_query_dict = self.query_dict.copy()
        tatal_query_dict._mutable = True
        origin_value_list = self.query_dict.getlist('type')
        if origin_value_list:
            yield '<a href="#">类型</a>'
        else:
            yield '<a class="active" href="#">类型</a>'
        yield '</div>'
        yield '<div class="others">'
        for item in self.data_list:
            val = 'type'
            text=item.unit
            # logger.debug(text)
            query_dict = self.query_dict.copy()
            query_dict._mutable = True
            if str(text) in origin_value_list:
                query_dict.pop(val)
                yield '<a class="active" href="?%s">%s</a>' %(query_dict.urlencode(),item.filed)
            else:
                query_dict[val]=text
                yield '<a href="?%s">%s</a>' %(query_dict.urlencode(),item.filed)
        yield '</div>'
class ChangeList_type(object):
    def __init__(self,config,query_dict):
        self.config = config
        self.query_dict=query_dict
        self.list_filter = self.config.get_list_filter_type()
        # logger.debug(self.list_filter)
    def gen_list_filter_row(self):
        _field = []
        for option in self.list_filter:
            _field.append(option)
            # logger.debug(_field)
        # logger.debug(_field)
        yield option.get_type(_field,self.config, self.query_dict)
class Option_type(object):
    def __init__(self,unit,filed):
        self.unit = unit
        self.filed = filed
    def get_type(self,_field,config,query_dict):
        row = Row_type(_field,config,query_dict)
        # logger.debug(row)
        return row
class Reptle(StarkConfig):
    def get_list_filter_type(self):
        val=[]
        val.extend(self.list_filter_type)
        return val
    def domain_de(self,row=None,header=False):
        if header:
            return "主机名"
        return mark_safe('<a href="%s" >%s</a>' % (self.reptle_url_details(row), row.domain))
    list_display = [domain_de]
    def reptle_url_details(self, row):
        app_label = self.model_class._meta.app_label
        model_name = self.model_class._meta.model_name
        namespace = site.namespace
        name = '%s:%s_%s_url_details' % (namespace, app_label, model_name)
        url_details = reverse(name, kwargs={'pk': row.pk,'sd':None})
        return url_details
    def extra_url(self):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        s = [
            url(r'^(?P<pk>\d+)/url_details/(?P<sd>\S+)/$', self.url_details, name='%s_%s_url_details' % info),
            url(r'^(?P<pk>\d+)/text_details/(?P<sd>\S+)/$', self.text_details, name='%s_%s_text_details' % info),
            # url(r'^(?P<pk>\W+)/text_details/$', self.text_details, name='%s_%s_text_details' % info)
        ]
        return s

    list_filter_type = [
        Option_type(unit='text', filed='文本'),
        Option_type(unit='pic', filed='图片'),
        Option_type(unit='video', filed='视频'),
    ]
    def url_details(self,request,pk,sd=None):
        obj = Reptile_reg.objects.filter(pk=pk).first()
        if sd != 'None':
            sd = sd[5:]
            url=base64.b64decode(sd).decode('utf-8')
            domain = obj.domain + ':' + 'text'
            body = rehis_zero.hget(domain,url)
            return HttpResponse(body)
        web_type = request.GET.get('type')
        query_params = request.GET.copy()
        query_params._mutable = True
        request.GET._mutable=True
        if not web_type:
            request.GET['type']='pic'
        if request.GET.get('type')=='pic':
            domain = obj.domain + ':' + 'img'
            c2=ChangeList_type(self,request.GET)
            total_count = rehis_zero_pic.hlen(domain)
            total_count = int(total_count)
            page = Pagination(request.GET.get('page'), total_count, request.path_info, query_params, per_page=3)
            s = rehis_zero_pic.hscan(domain, cursor=page.start, count=12)
            return render(request, 'business_func/url_details.html', {'srcs':s,'c2':c2,'page':page})
        elif request.GET.get('type') == 'text':
            domain = obj.domain + ':' + 'text'
            total_count = rehis_zero_pic.hlen(domain)
            total_count = int(total_count)
            page = Pagination(request.GET.get('page'), total_count, request.path_info, query_params, per_page=3)
            s = rehis_zero.hscan(domain,cursor=page.start,count=12)
            s_list=[]
            s_dict={}
            for k in s[1].keys():
                k = str(k,encoding='utf-8')
                # url_base = base64.b64decode(k.encode('utf-8'))
                bm = base64.b64encode(k.encode('utf-8'))
                base_url = str(bm,encoding='utf-8')
                s_dict[k]=base_url
            c2=ChangeList_type(self,request.GET)
            return render(request, 'business_func/url_details.html',{'texts':s_dict,'c2':c2,'page':page})
        elif request.GET.get('type') == 'video':
            domain = obj.domain + ':' + 'video'
            s = rehis_zero.hscan(domain, cursor=0, count=12)
            c2 = ChangeList_type(self, request.GET)
            return render(request, 'business_func/url_details.html', {'video': s, 'c2': c2})
        else:
            return HttpResponse('输入网址有误')
    def add_view(self, request):
        if request.method=='POST':
            re_type = request.POST.get('re_type')
            if re_type == 'scrapy_selenium':
                pass
            else:
                start_url = request.POST.get('start_url')
                rehis_zero.lpush('sunkey',start_url)
                cookie = request.POST.get('cookie')
                domain= urlparse(start_url).netloc
                url_heade=domain + ':' +'header'
                print(cookie)
                rehis_zero.hset(url_heade,'cookie',cookie)
                start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                Reptile_reg.objects.create(domain=domain,url=start_url,FirstReptile=start_time)
                # Reptile_reg.save()
                return redirect('/stark/business_func/reptile_reg/list/')
        return render(request, 'business_func/reptile_add.html')
    def text_details(self,request,pk,sd):
        print(pk,sd)
        return HttpResponse('这是text详情')
site.register(Reptile_reg,Reptle)