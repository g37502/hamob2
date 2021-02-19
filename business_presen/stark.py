# -*- coding:utf-8 -*-
#  2021/1/14 
#  stark.py
#  
# author:gyl
from django.db.models import Q
from django.db.models import Avg,Max,Min,Count,Sum
from stark.service.stark import site, StarkConfig,Option
from  business_presen.models import *
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.urls import reverse
from django.shortcuts import HttpResponse,render,redirect
from stark.utils.log_ctrl import logger
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.pyplot import MultipleLocator
from io import BytesIO
import base64
import datetime
import numpy as np
from django_pandas.io import read_frame
from stark.service.stark import ChangeList
from stark.service.stark import Option,Row
from types import FunctionType
from django.db.models.expressions import RawSQL
from django.http import QueryDict
import re
from stark.utils.pagination import Pagination

class Row_pic(object):
    def __init__(self,data_list,option,query_dict):
        self.data_list = data_list
        self.option = option
        self.query_dict = query_dict
        logger.debug(option.field)
    def __iter__(self):
        '''data_list=（{'bussiness':'Monitor'}, {'bussiness':'reportURLNUM', 'bussiness':'monitorURLNUM'）'''
        '''option = CangeList_pic'''
        ''' query_dict: request dict'''
        # val = self.option.get_value(self.data_list)
        yield '<div class="whole">'
        tatal_query_dict = self.query_dict.copy()
        tatal_query_dict._mutable = True
        origin_value_list = self.query_dict.getlist('bussiness')
        if origin_value_list:
            yield '<a href="#">类型</a>'
        else:
            yield '<a class="active" href="#">类型</a>'
        yield '</div>'
        yield '<div class="others">'
        logger.debug(self.data_list)
        for item in self.data_list:
            val = 'bussiness'
            text=item[val]
            logger.debug(text)
            query_dict = self.query_dict.copy()
            query_dict._mutable = True
            if str(text) in origin_value_list:
                query_dict.pop(val)
                yield '<a class="active" href="?%s">%s</a>' %(query_dict.urlencode(),text)
            else:
                query_dict[val]=text
                yield '<a href="?%s">%s</a>' %(query_dict.urlencode(),text)
        yield '</div>'
class Row_count(object):
    def __init__(self,data_list,option,query_dict):
        self.data_list = data_list
        self.option = option
        self.query_dict = query_dict
        # logger.debug(option.field)
    def __iter__(self):
        '''data_list=（{'bussiness':'Monitor'}, {'bussiness':'reportURLNUM', 'bussiness':'monitorURLNUM'）'''
        '''option = CangeList_pic'''
        ''' query_dict: request dict'''
        # val = self.option.get_value(self.data_list)
        val = 'bussiness'
        yield '<div class="whole">'
        tatal_query_dict = self.query_dict.copy()
        tatal_query_dict._mutable = True
        origin_value_list = self.query_dict.getlist('bussiness')
        if origin_value_list:
            tatal_query_dict.pop(val)
            yield '<a href="?%s">全部</a>' % (tatal_query_dict.urlencode(),)
        else:
            yield '<a class="active" href="?%s">全部</a>' % (tatal_query_dict.urlencode(),)
        yield '</div>'
        yield '<div class="others">'
        # logger.debug(self.data_list)
        for item in self.data_list:

            text=item[val]
            # logger.debug(text)
            query_dict = self.query_dict.copy()
            query_dict._mutable = True
            if not self.option.is_multi:
                if str(text) in origin_value_list:
                    query_dict.pop(val)
                    yield '<a class="active" href="?%s">%s</a>' %(query_dict.urlencode(),text)
                else:
                    query_dict[val]=text
                    yield '<a href="?%s">%s</a>' %(query_dict.urlencode(),text)
            else:
                multi_val_list = query_dict.getlist(val)
                if str(text) in origin_value_list:
                    # 已经选，把自己去掉
                    multi_val_list.remove(str(text))
                    query_dict.setlist(val, multi_val_list)
                    yield '<a class="active" href="?%s">%s</a>' % (query_dict.urlencode(), text)
                else:
                    multi_val_list.append(text)
                    query_dict.setlist(val, multi_val_list)
                    yield '<a href="?%s">%s</a>' % (query_dict.urlencode(), text)
        yield '</div>'
class Row_timeunit(object):
    def __init__(self, data_list,config,query_dict):
        self.data_list= data_list
        self.query_dict = query_dict
        # logger.debug(type(self.data_list))
    def __iter__(self):
        yield '<div class="whole">'
        tatal_query_dict = self.query_dict.copy()
        tatal_query_dict._mutable = True
        origin_value_list = self.query_dict.getlist('timeunit')
        if origin_value_list:
            yield '<a href="#">时长</a>'
        else:
            yield '<a class="active" href="#">时长</a>'
        yield '</div>'
        yield '<div class="others">'
        for item in self.data_list:
            val = 'timeunit'
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

class Option_pic(Option):
    def gen_column(self,_field,query_dict):
        # logger.debug(_field,query_dict)
        row=Row_pic(_field,self,query_dict)
        return row
class Option_count(Option):
    def gen_column(self, _field, query_dict):
        # logger.debug(_field,query_dict)
        row = Row_count(_field, self, query_dict)
        return row
class CangeList_pic(ChangeList):
    def gen_list_filter_rows(self):
        for option in self.list_filter:
            if isinstance(option.field, FunctionType):
                # val = self.config.
                _field = []
                for i in option.field(self.config):
                    _field.append({'bussiness':i})
                yield option.gen_column(_field,self.config.request.GET)
            else:
                _field = self.config.model_class._meta.get_field(option.field)
                yield option.get_queryset(_field, self.config.model_class, self.config.request.GET)
class Option_plt(object):
    def __init__(self,filed,colum_nu,title,unit,explain,colum_func=None,plt_func=None):
        self.filed = filed
        self.colum_nu = colum_nu
        self.title =title
        self.explain = explain
        self.unit =unit
        #获取需要作图数据
        self.colum_func = colum_func
        #对每幅图的数据整形
        self.plt_func = plt_func
class Option_timeunit(object):
    def __init__(self,unit,filed):
        self.unit = unit
        self.filed = filed
    def get_timeunit(self,_field,config,query_dict):
        row = Row_timeunit(_field,config,query_dict)
        # logger.debug(row)
        return row
class ChangeList_count(object):
    def __init__(self,config,queryset,request):
        self.config = config
        self.queryset = queryset
        self.request = request
        self.list_filter = self.config.get_list_filter_count()
    def gen_list_filter_rows(self):
        for option in self.list_filter:
            # print(option.field)
            if isinstance(option.field, FunctionType):
                # val = self.config.
                _field = []
                for i in option.field(self.config):
                    _field.append({'bussiness':i})
                yield option.gen_column(_field,self.request.GET)
            else:
                _field = self.config.model_class._meta.get_field(option.field)
                yield option.get_queryset(_field, self.config.model_class, self.request.GET)
class ChangeList_timeunit(object):
    def __init__(self,config,query_dict):
        self.config = config
        self.query_dict=query_dict
        self.list_filter = self.config.get_list_filter_timeunit()
        # logger.debug(self.list_filter)
    def gen_list_filter_row(self):
        _field = []
        for option in self.list_filter:
            _field.append(option)
            # logger.debug(_field)
        # logger.debug(_field)
        yield option.get_timeunit(_field,self.config, self.query_dict)

class Count_dataConfig(StarkConfig):
    '''日流量'''
    def business(self):
        list_column = self.list_filter_column
        list_column1 = []
        for i in list_column:
            list_column1.append(i.filed)
        return list_column1
    def business_count(self):
        list_column = self.list_filter_count_column
        list_column1 = []
        for i in list_column:
            list_column1.append(i.filed)
        return list_column1
    def text_func(self,option):
        return option.field
    def value_func(self,option):
        return option.colum_nu
    def colum_10g(self,qs_dataframe,bussiness):
        from hardmanage.models import IDC
        queryset_IDC = IDC.objects.all()
        idc_dateframe = read_frame(qs=queryset_IDC)
        qs_dataframe = pd.merge(qs_dataframe,idc_dateframe,left_on='MonitorAddress',right_on='name')
        qs_dataframe[bussiness] = qs_dataframe['Monitor'] // qs_dataframe['desflow']
        qs_dataframe = qs_dataframe[['inserttime', 'MonitorAddress', bussiness, ]]
        return qs_dataframe
    def colum_rate(self,qs_dataframe,bussiness):
        qs_dataframe=qs_dataframe[['inserttime', 'MonitorAddress','monitorURLNUM','reportURLNUM']]
        return qs_dataframe
    def plt_rate(self,j,bussiness):
        j[bussiness] = round(j['reportURLNUM'] / j['monitorURLNUM'],5)
        logger.debug(j[[bussiness]])
        j = j[[bussiness,]]
        return j
    def colum_content(self,qs_dataframe,bussiness):
        qs_dataframe = qs_dataframe[['inserttime', 'MonitorAddress','monitorURLNUM' ,'Monitor' ]]
        return qs_dataframe
    def plt_content(self,j,bussiness):
        j[bussiness] = round(j['monitorURLNUM']/(j['Monitor']/(1024*1024))/100, 0)
        j = j[[bussiness, ]]
        return j
    def colum_size(self,qs_dataframe,bussiness):
        qs_dataframe = qs_dataframe[['inserttime', 'MonitorAddress','monitorURLNUM' ,'Monitor']]
        return qs_dataframe
    def plt_size(self,j, bussiness):
        j[bussiness] = round(j['Monitor']/j['monitorURLNUM'],1)
        j = j.fillna(0)
        logger.debug(j[[bussiness]])
        return j[[bussiness]]
    def get_list_filter_count(self):
        val = []
        val.extend(self.list_filter_count)
        return val
    def get_list_filter_timeunit(self):
        val=[]
        val.extend(self.list_filter_timeunit)
        return val
    list_filter = [
        Option_pic(field='MonitorAddress',is_choice=False,is_multi=True,text_func=lambda x:x.name, value_func=lambda x:x.pk),
        Option_pic(field=business,is_choice=False,is_multi=False,text_func=text_func, value_func=value_func),
    ]
    # list_filter_column = ['Monitor','reportURLNUM','monitorURLNUM']
    list_filter_column = [
        Option_plt(filed='Monitor',colum_nu=1,title='流量图',unit='K',explain='接收文件大小'),
        Option_plt(filed='reportURLNUM',colum_nu=2,title='中标量',unit="个",explain='中标数量'),
        Option_plt(filed='monitorURLNUM',colum_nu=3,title='DPI URL总量',unit="个",explain='DPI URL总量'),
        Option_plt(filed='10G',colum_nu=4,title='10G流量',unit="k",explain='10G还原量',colum_func=colum_10g),
        Option_plt(filed='RATE',colum_nu=5,title='中标率',unit="",explain='中标率',colum_func=colum_rate,plt_func=plt_rate),
        Option_plt(filed='GURL_NU',colum_nu=6,title='每G文件包含URL量',unit='百个',explain='URL数量', colum_func=colum_content,plt_func=plt_content),
        Option_plt(filed='PIC-SIZE',colum_nu=7,title='图片平均大小',unit='K',explain='图片平均大小', colum_func=colum_size,plt_func=plt_size),
    ]
    list_filter_count = [
        Option_count(field='MonitorAddress', is_choice=False, is_multi=True, text_func=lambda x: x.name,
                   value_func=lambda x: x.pk),
        Option_count(field=business_count, is_choice=False, is_multi=True, text_func=text_func, value_func=value_func),
    ]
    list_filter_count_column=[
        Option_plt(filed='Monitor', colum_nu=1,title='流量图', unit='K', explain='接收文件大小'),
        Option_plt(filed='reportURLNUM', colum_nu=2, title='中标量', unit="个", explain='中标数量'),
        Option_plt(filed='monitorURLNUM', colum_nu=3, title='DPI URL总量', unit="个", explain='DPI URL总量'),
    ]
    # 周：’w', 日：‘D'， 小时:'H', 分钟:'T' or 'min',月：’m', 季度：q
    list_filter_timeunit=[
        Option_timeunit(unit='H',filed='时'),
        Option_timeunit(unit='D', filed='天'),
        Option_timeunit(unit='m', filed='月'),
    ]
    list_filter_count_type=[

    ]
    def get_list_filter_column(self):
        val = self.list_filter_column
        return val
    def plastic(self,x,):
        x=int(x)
        x1 = list(str(x))
        for i in range(len(str(x))):
            if i == 0:
                continue
            x1[i] = '0'
        a = ''.join(x1)
        return int(a)
    def get_time(self,request):
        kssj = request.GET.get('kssj')
        jssj = request.GET.get('jssj')
        # logger.debug(kssj, jssj)
        if not kssj and not jssj:
            kssj=(datetime.datetime.now()+datetime.timedelta(days=-10)).strftime("%Y-%m-%d %H:%M:%S")
            jssj=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif kssj and not jssj:
            jssj = (datetime.datetime.strptime(kssj,"%Y-%m-%d %H:%M:%S")+datetime.timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
        elif jssj and not kssj:
            kssj = (datetime.datetime.strptime(jssj,"%Y-%m-%d %H:%M:%S")+datetime.timedelta(days=-10)).strftime("%Y-%m-%d %H:%M:%S")
        return kssj,jssj
    def get_bussiness(self,request):
        bussiness = request.GET.get('bussiness')
        if not bussiness:
            bussiness = 'Monitor'
        return bussiness
    def get_interva(self,min_shu,max_shu,identification):
        logger.debug(min_shu)
        logger.debug(max_shu)
        if identification.filed == "RATE":
            interva = round((max_shu-min_shu)/10,3)
            min_shu = round(min_shu, 4)
            max_shu = round(max_shu, 4) + interva
        elif identification.filed == "GURL_NU":
            interva = (max_shu - min_shu) // 10
            try:
                interva = self.plastic(interva)
            except:
                pass
            max_shu = max_shu + interva
        elif identification.filed == 'PIC-SIZE':
            interva = (max_shu - min_shu) // 10
            # interva = self.plastic(interva)
            # min_shu = self.plastic(min_shu)
            if interva >= 1:
                interva = (max_shu - min_shu) // 10
                # interva = self.plastic(interva)
                # min_shu = self.plastic(min_shu)
        else:
            interva = (max_shu - min_shu) // 10
            interva = self.plastic(interva)
            min_shu = self.plastic(min_shu)
        if interva == 0:
            if identification.filed == "RATE":
                interva = round(max_shu/10, 3)
            else:
                interva = max_shu//10
            if interva==0:
                interva=1
        if pd.isna(min_shu):
            min_shu =0
        if pd.isna(max_shu):
            max_shu=1
        if pd.isna(interva):
            interva=1
        max_shu = max_shu + interva
        return min_shu,max_shu,interva
    def get_src(self,plt,min_shu=None,max_shu=None,x1=None,bussiness='Monitor'):
        list_filter_column = self.list_filter_column
        for i in list_filter_column:
            if i.filed == bussiness:
                identification=i
        if min_shu==None and max_shu==None:
            plt.title(identification.title)
            plt.ylabel('无数据')
            sio = BytesIO()
            plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
            data = base64.encodebytes(sio.getvalue()).decode()
            src = 'data:image/png;base64,' + str(data)
            plt.close()
            return src
        else:
            if min_shu == max_shu:
                min_shu = 0
            plt.title(identification.title)
            date_list = []
            for i in x1:
                date_list.append(i.strftime('%Y-%m-%d'))
            plt.xticks(date_list, date_list, rotation=45)
            min_shu, max_shu, interva = self.get_interva(min_shu, max_shu, identification)
            y_majoy_locator = MultipleLocator(interva)
            plt.ylabel(f'{identification.explain}，刻度间隔为{interva}{identification.unit}', fontsize=20)
            plt.ylim((min_shu, max_shu))
            ax = plt.gca()
            ax.yaxis.set_major_locator(y_majoy_locator)
            plt.legend(loc='best')
            sio = BytesIO()
            plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
            data = base64.encodebytes(sio.getvalue()).decode()
            src = 'data:image/png;base64,' + str(data)
            plt.close()
            return src
    def get_qs_dataframe(self,queryset,bussiness):
        qs_dataframe = read_frame(qs=queryset)
        for i in self.get_list_filter_column():
            if isinstance(i.colum_func,FunctionType) and bussiness == i.filed:
                qs_dataframe = i.colum_func(self,qs_dataframe,i.filed)
                return qs_dataframe
        qs_dataframe = qs_dataframe[['inserttime', 'MonitorAddress', bussiness]]
        return qs_dataframe
    def get_plt(self,request,queryset):
        # 获取处理的类型
        bussiness = self.get_bussiness(request)
        qs_dataframe = self.get_qs_dataframe(queryset,bussiness)
        s = qs_dataframe.groupby('MonitorAddress')
        plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
        plt.rcParams["axes.unicode_minus"] = False
        plt.figure(figsize=(20, 8), dpi=80)
        x1 = set()
        for i, j in s:
            j['inserttime'] = pd.to_datetime(j['inserttime'], format='%Y-%m')
            j.sort_values(by=['inserttime'], inplace=True)
            j.set_index('inserttime', inplace=True)
            j = j.resample('d').sum()
            for option_plt in self.get_list_filter_column():
                if isinstance(option_plt.plt_func, FunctionType) and bussiness == option_plt.filed:
                    j = option_plt.plt_func(self,j,option_plt.filed)
            _x = j.index
            # print(j)
            x1.update(list(_x))
            _y = j[bussiness]
            plt.plot(_x, _y, 'o-', label=i)
            if 'min_shu' in locals().keys():
                if _y.min() < min_shu:
                    min_shu = _y.min()
            else:
                min_shu = _y.min()
            if 'max_shu' in locals().keys():
                if _y.max() > max_shu:
                    max_shu = _y.max()
            else:
                max_shu = _y.max()
        if '_y' not in locals().keys():
            min_shu = None
            max_shu = None
        src = self.get_src(plt,min_shu,max_shu,x1,bussiness)
        return src
    def changelist_view(self, request):
        if request.method == 'POST':
            action_name = request.POST.get('action')
            action_dict = self.get_action_dict()
            if action_name not in action_dict:
                return HttpResponse('非法请求')
            response = getattr(self, action_name)(request)
            if response:
                return response
        # ##### 处理搜索 #####
        search_list, q, con = self.get_search_condition(request)
        # ##### 处理分页 #####
        from stark.utils.pagination import Pagination
        total_count = self.model_class.objects.filter(con).count()
        query_params = request.GET.copy()
        query_params._mutable = True
        page = Pagination(request.GET.get('page'), total_count, request.path_info, query_params, per_page=7)
        # 获取组合搜索筛选
        origin_queryset = self.get_queryset()
        # logger.debug(con,self.get_list_filter_condition())
        # 获取开始结束时间
        kssj, jssj = self.get_time(request)
        logger.debug(kssj,jssj)
        queryset = origin_queryset.filter(inserttime__range=(kssj,jssj)).filter(con).filter(**self.get_list_filter_condition()).order_by(
            *self.get_order_by())
        src=self.get_plt(request,queryset)
        cl = CangeList_pic(self, queryset, q, search_list, page)
        # ######## 组合搜索 #########
        # list_filter = ['name','user']
        context = {
            'cl': cl,
            'src':src
        }
        return render(request,'business_presen/pic.html',context)
    def reverse_count(self,row):
        app_label = self.model_class._meta.app_label
        model_name = self.model_class._meta.model_name
        namespace = site.namespace
        name = '%s:%s_%s_changelist_count' % (namespace, app_label, model_name)
        count_url = reverse(name)
        return count_url
    def extra_url(self):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        s = url(r'^changelist_count/$', self.changelist_count, name='%s_%s_changelist_count' % info)
        return s

    def changelist_count(self,request):
        origin_queryset = self.get_queryset()
        # logger.debug(con,self.get_list_filter_condition())
        # 获取开始结束时间
        kssj, jssj = self.get_time(request)
        # logger.debug(kssj, jssj)
        comb_condition = {}
        element = request.GET.getlist('MonitorAddress')
        if element:
            comb_condition['%s__in' % 'MonitorAddress'] = element
        logger.debug(comb_condition)
        _time_format = self.get_time_format(request)
        _annotate_list = self.get_annotate_list(request)
        logger.debug(_annotate_list)
        queryset = origin_queryset.filter(inserttime__range=(kssj, jssj)).filter().filter(**comb_condition
        ).extra(select=_time_format).values('MonitorAddress__name','inserttime').annotate(*_annotate_list).order_by(
            *self.get_order_by())
        cl = ChangeList_count(self, queryset, request)
        c2 = ChangeList_timeunit(self, request.GET)
        return render(request,'business_presen/count.html', {'cl': cl, 'c2': c2,})
    def get_annotate_list(self,request):
        _annotate_list=[]
        bussiness_list = request.GET.getlist('bussiness')
        if not bussiness_list:
            _annotate_list.append(Sum('Monitor'))
            _annotate_list.append(Sum('reportURLNUM'))
            _annotate_list.append(Sum('monitorURLNUM'))
            return _annotate_list
        for bussiness in bussiness_list:
            _annotate_list.append(Sum(bussiness))
        return _annotate_list
        
    def get_time_format(self,request):
        time_unit = request.GET.get('timeunit')
        if time_unit is None:
            time_unit = 'D'
        if time_unit == 'D':
            time_format = {'inserttime': "DATE_FORMAT(inserttime,'%%Y-%%m-%%d')"}
        elif time_unit == 'H':
            time_format = {'inserttime': "DATE_FORMAT(inserttime,'%%Y-%%m-%%d %%H')"}
        elif time_unit == 'm':
            time_format = {'inserttime': "DATE_FORMAT(inserttime,'%%Y-%%m')"}
        elif time_unit == 'Y':
            time_format = {'inserttime': "DATE_FORMAT(inserttime,'%%Y')"}
        return time_format
    def src_pic(self,pd):
        pass

site.register(Count_data,Count_dataConfig)

class Colum_Count(Count_dataConfig):
    '''月流量'''
    def business(self):
        list_column = self.list_filter_column
        list_column1 = []
        for i in list_column:
            list_column1.append(i.filed)
        return list_column1
    def text_func(self, option):
        return option.field
    def value_func(self, option):
        return option.colum_nu
    def colum_monitor(self,qs_dataframe,bussiness):
        qs_dataframe['Monitor'] = qs_dataframe['Monitor']//1000000
        return qs_dataframe
    def colum_10g(self, qs_dataframe, bussiness):
        from hardmanage.models import IDC
        queryset_IDC = IDC.objects.all()
        idc_dateframe = read_frame(qs=queryset_IDC)
        qs_dataframe = pd.merge(qs_dataframe, idc_dateframe, left_on='MonitorAddress', right_on='name')
        qs_dataframe[bussiness] = qs_dataframe['Monitor'] // qs_dataframe['desflow']
        qs_dataframe = qs_dataframe[['inserttime', 'MonitorAddress', bussiness, ]]
        return qs_dataframe
    def colum_rate(self, qs_dataframe, bussiness):
        qs_dataframe = qs_dataframe[['inserttime', 'MonitorAddress', 'monitorURLNUM', 'reportURLNUM']]
        qs_dataframe[bussiness] = round(qs_dataframe['reportURLNUM'] / qs_dataframe['monitorURLNUM'], 5)
        qs_dataframe = qs_dataframe[['inserttime', 'MonitorAddress',bussiness]]
        return qs_dataframe
    def colum_content(self, qs_dataframe, bussiness):
        qs_dataframe = qs_dataframe[['inserttime', 'MonitorAddress', 'monitorURLNUM', 'Monitor']]
        qs_dataframe[bussiness] = round(qs_dataframe['monitorURLNUM'] / (qs_dataframe['Monitor'] / (1024 * 1024)) / 100, 0)
        qs_dataframe = qs_dataframe[['inserttime', 'MonitorAddress',bussiness]]
        return qs_dataframe
    def colum_size(self, qs_dataframe, bussiness):
        qs_dataframe = qs_dataframe[['inserttime', 'MonitorAddress', 'monitorURLNUM', 'Monitor']]
        qs_dataframe[bussiness] = round(qs_dataframe['Monitor'] / qs_dataframe['monitorURLNUM'], 1)
        qs_dataframe = qs_dataframe.fillna(0)
        qs_dataframe =qs_dataframe[['inserttime', 'MonitorAddress',bussiness]]
        return qs_dataframe
    def plt_size(self, j, bussiness):
        j[bussiness] = round(j['Monitor'] / j['monitorURLNUM'], 1)
        j = j.fillna(0)
        logger.debug(j[[bussiness]])
        return j[[bussiness]]
    list_filter = [
        Option_pic(field='MonitorAddress', is_choice=False, is_multi=True, text_func=lambda x: x.name,value_func=lambda x: x.pk),
        Option_pic(field=business, is_choice=False, is_multi=False, text_func=text_func, value_func=value_func),
    ]
    list_filter_column = [
        Option_plt(filed='Monitor', colum_nu=1, title='流量图', unit='G', explain='接收文件大小',colum_func=colum_monitor),
        Option_plt(filed='reportURLNUM', colum_nu=2, title='中标量', unit="个", explain='中标数量'),
        Option_plt(filed='monitorURLNUM', colum_nu=3, title='DPI URL总量', unit="个", explain='DPI URL总量'),
        Option_plt(filed='10G', colum_nu=4, title='10G流量', unit="k", explain='10G还原量', colum_func=colum_10g),
        Option_plt(filed='RATE', colum_nu=5, title='中标率', unit="", explain='中标率', colum_func=colum_rate),
        Option_plt(filed='GURL_NU', colum_nu=6, title='每G文件包含URL量', unit='百个', explain='URL数量',colum_func=colum_content,),
        Option_plt(filed='PIC-SIZE', colum_nu=7, title='图片平均大小', unit='K', explain='图片平均大小', colum_func=colum_size,plt_func=plt_size),
    ]
    def get_src(self,plt,qs_dataframe,bussiness):
        list_filter_column = self.list_filter_column
        for i in list_filter_column:
            if i.filed == bussiness:
                identification = i
        if not qs_dataframe.empty:
            date_list = pd.date_range(qs_dataframe['inserttime'].min(), qs_dataframe['inserttime'].max(), freq="M")
            plt.xticks(date_list, date_list.map(lambda x: x.strftime('%Y-%m')), rotation=45)
            plt.title(identification.title)
            min_shu =qs_dataframe[bussiness].min()
            max_shu =qs_dataframe[bussiness].max()
            min_shu, max_shu, interva = self.get_interva(min_shu, max_shu, identification)
            y_major_locator = MultipleLocator(interva)
            plt.ylim(min_shu,max_shu)

            plt.ylabel(f'{identification.explain}，刻度间隔为{interva}{identification.unit}', fontsize=20)
            ax = plt.gca()
            ax.yaxis.set_major_locator(y_major_locator)
            plt.legend(loc='best')
            sio = BytesIO()
            plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
            data = base64.encodebytes(sio.getvalue()).decode()
            src = 'data:image/png;base64,' + str(data)
            plt.close()
            return src
        else:
            plt.title(identification.title)
            plt.ylabel('无数据')
            sio = BytesIO()
            plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
            data = base64.encodebytes(sio.getvalue()).decode()
            src = 'data:image/png;base64,' + str(data)
            plt.close()
            return src
    def get_plt(self,request,queryset):
        # 获取处理的类型
        bussiness = self.get_bussiness(request)
        qs_dataframe = self.get_qs_dataframe(queryset,bussiness)
        s = qs_dataframe.groupby('MonitorAddress')
        plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
        plt.rcParams["axes.unicode_minus"] = False
        plt.figure(figsize=(20, 8), dpi=80)
        for i, j in s:
            j['inserttime'] = pd.to_datetime(j['inserttime'], format='%Y-%m')
            j.sort_values(by=['inserttime'], inplace=True)
            j.set_index('inserttime', inplace=True)
            _x = j.index
            _y=j[bussiness]
            plt.plot(_x,_y,'o-',label=i)
        src = self.get_src(plt, qs_dataframe, bussiness)
        return src
    def changelist_view(self, request):
        if request.method == 'POST':
            action_name = request.POST.get('action')
            action_dict = self.get_action_dict()
            if action_name not in action_dict:
                return HttpResponse('非法请求')
            response = getattr(self, action_name)(request)
            if response:
                return response
        # ##### 处理搜索 #####
        search_list, q, con = self.get_search_condition(request)
        # ##### 处理分页 #####
        from stark.utils.pagination import Pagination
        total_count = self.model_class.objects.filter(con).count()
        query_params = request.GET.copy()
        query_params._mutable = True
        page = Pagination(request.GET.get('page'), total_count, request.path_info, query_params, per_page=7)
        # 获取组合搜索筛选
        origin_queryset = self.get_queryset()
        # logger.debug(con,self.get_list_filter_condition())
        # 获取开始结束时间
        kssj, jssj = self.get_time(request)
        queryset = origin_queryset.extra(
        select={"inserttime": "DATE_FORMAT(inserttime, '%%Y-%%m')"}).filter(inserttime__range=(kssj,jssj)).filter(con).filter(**self.get_list_filter_condition()).order_by(
            *self.get_order_by())
        src=self.get_plt(request,queryset)
        cl = CangeList_pic(self, queryset, q, search_list, page)
        # ######## 组合搜索 #########
        # list_filter = ['name','user']
        context = {
            'cl': cl,
            'src':src,
        }
        return render(request,'business_presen/picmon.html',context)
    def get_time(self,request):
        kssj = request.GET.get('kssj')
        jssj = request.GET.get('jssj')
        logger.debug(kssj, jssj)
        if not kssj and not jssj:
            kssj=(datetime.datetime.now()+datetime.timedelta(days=-180)).strftime("%Y-%m-%d")
            jssj=datetime.datetime.now().strftime("%Y-%m-%d")
        elif kssj and not jssj:
            jssj = (datetime.datetime.strptime(kssj,"%Y-%m-%d")+datetime.timedelta(days=180)).strftime("%Y-%m-%d")
        elif jssj and not kssj:
            kssj = (datetime.datetime.strptime(jssj,"%Y-%m-%d")+datetime.timedelta(days=-180)).strftime("%Y-%m-%d")
        logger.debug(kssj, jssj)
        return kssj,jssj
site.register(Count_mon,Colum_Count)

class DomainStarkConfig(StarkConfig):
    def reverse_dqpic_url(self,row):
        app_label = self.model_class._meta.app_label
        model_name = self.model_class._meta.model_name
        namespace = site.namespace
        name = '%s:%s_%s_dqpic_list' % (namespace, app_label, model_name)
        dqpic_url = reverse(name,kwargs={'pk': row.pk})
        return dqpic_url
    def get_domain(self,row=None,header=False):
        if header:
            return "主机名"
        return mark_safe('<a href="%s" >%s</a>' % (self.reverse_dqpic_url(row), row.domain))
    list_display = [get_domain,'endcatchdate']
    search_list = ['domain']
    order_by = ['-endcatchdate']
    def extra_url(self):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        s = url(r'^(?P<pk>\d+)/dqpic_list/$', self.business_presen_dqpic_list, name='%s_%s_dqpic_list' % info)
        return s
    def get_time_filter(self,request):
        kssj = request.GET.get('kssj')
        jssj = request.GET.get('jssj')
        logger.debug(kssj, jssj)
        con=Q()
        if kssj and not jssj:
            con = Q(sendtime__gt=kssj)
        elif jssj and not kssj:
            con = Q(sendtime__lt=jssj)
        elif kssj and jssj:
            con = Q(sendtime__range=(kssj,jssj))
        logger.debug(kssj, jssj)
        return con
    def get_search_condition_url(self, request):
        con = self.get_time_filter(request)
        return con
    def get_search_condition_dqpic(self, request,search_list):
        q = request.GET.get('q', "")  # ‘大’
        con = Q()
        con.connector = "OR"
        if q:
            for field in search_list:
                con.children.append(('%s__contains' % field, q))

        return  con
    def business_presen_dqpic_list(self,request,pk):
        '''图片显示'''
        search_list = ['colleteid']
        con = self.get_search_condition_url(request)
        conn =self.get_search_condition_dqpic(request,search_list)
        total_count  = DqPic.objects.using('orac119').filter(domainid=pk).filter(con).filter(conn).count()
        query_params = request.GET.copy()
        query_params._mutable = True
        page = Pagination(request.GET.get('page'), total_count, request.path_info, query_params, per_page=8)
        queryset = DqPic.objects.using('orac119').filter(domainid=pk).filter(con).filter(conn).distinct().values('url')[page.start:page.end]
        # print(queryset)
        q = request.GET.get('q', "")
        context = {
            'urls': queryset,
            'page': page,
            'search_list': search_list,
            'q': q,
        }
        return render(request, 'business_presen/url.html',context)
    def changelist_view(self, request):
        """
        所有URL的查看列表页面
        :param request:
        :return:
        """
        if request.method == 'POST':
            action_name = request.POST.get('action')
            action_dict = self.get_action_dict()
            if action_name not in action_dict:
                return HttpResponse('非法请求')
            response = getattr(self, action_name)(request)
            if response:
                return response
        # ##### 处理搜索 #####
        search_list, q, con = self.get_search_condition(request)
        # ##### 处理分页 #####
        total_count = self.model_class.objects.using('orac119').filter(con).count()
        query_params = request.GET.copy()
        query_params._mutable = True
        page = Pagination(request.GET.get('page'), total_count, request.path_info, query_params, per_page=7)
        list_filter = self.get_list_filter()
        # 获取组合搜索筛选
        queryset = Domain.objects.using('orac119').filter(con).filter(**self.get_list_filter_condition()).order_by(*self.get_order_by()).distinct()[page.start:page.end]
        cl = ChangeList(self, queryset, q, search_list, page)

        # ######## 组合搜索 #########
        # list_filter = ['name','user']
        context = {
            'cl': cl
        }
        return render(request, 'stark/changelist.html', context)
site.register(Domain,DomainStarkConfig)