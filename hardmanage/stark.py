# -*- coding:utf-8 -*-
#  2020/12/9 
#  stark.py
#  
# author:gyl
from stark.service.stark import site, StarkConfig,Option
from hardmanage import models
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.urls import reverse
from django.shortcuts import HttpResponse,render,redirect
from stark.utils.log_ctrl import logger

class ProvinceConfig(StarkConfig):
    order_by = ['province']
    search_list = ['province']
    action_list = [StarkConfig.multi_delete]
    list_display = ['province']
site.register(models.Province,ProvinceConfig)
class CityConfig(StarkConfig):
    order_by = ['city']
    search_list = ['city']
    action_list = [StarkConfig.multi_delete]
    list_display = [ 'city']
    list_filter = [
        Option(field='prov', is_choice=False, is_multi=True, text_func=lambda x: x.province,value_func=lambda x: x.pk),
    ]
site.register(models.City, CityConfig)
class AddressConfig(StarkConfig):
    order_by = ['address']
    search_list = ['address']
    action_list = [StarkConfig.multi_delete]
    list_display = ['address']
site.register(models.Address,AddressConfig)

class IDCConfig(StarkConfig):
    order_by = ['name']
    search_list = ['name']
    action_list = [StarkConfig.multi_delete]
    list_display = [ 'name', 'address']
site.register(models.IDC,IDCConfig)
class HostConfig(StarkConfig):
    # list_filter = ['HOSTNAME']
    def get_hostname(self,row=None, header=False):
        if header:
            return "主机名"
        return mark_safe('<a href="%s" >%s</a>' % (self.reverse_host_details(row),row.HOSTNAME))
    def reverse_host_details(self,row):
        app_label = self.model_class._meta.app_label
        model_name = self.model_class._meta.model_name
        namespace = site.namespace
        name = '%s:%s_%s_details' % (namespace, app_label, model_name)
        details = reverse(name,kwargs={'pk': row.pk})
        return details
    def extra_url(self):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        s = url(r'^(?P<pk>\d+)/details/$', self.hardmanage_host_details, name='%s_%s_details' % info)
        return s
    def hardmanage_host_details(self,request,pk):
        # logger.debug(pk)
        # obj = self.model_class.objects.filter(pk=pk)
        # ips = obj.memory_number.all()
        # for ip in ips:
        #     logger.debug(ip)
        # return HttpResponse('这个是host details')
        obj = models.Host.objects.filter(pk=pk).first()
        # cpu_inf = obj.CPU
        # host_tmp = cpu_inf.host_cpu.filter(HOSTNAME=obj.HOSTNAME)
        # print(type(host_tmp))
        # for x in host_tmp:
        #     print(x.CPU_NUMber)
        return render(request,'hardmanage/host_details.html',{'obj':obj,'list_name':self.details_host,'list_cpu':self.details_cpu})
    # def multiple_del(self,request):
    details_host = ['HOSTNAME', 'Serian_Number','Manufacturer','Producer_Name']
    details_cpu = ['name','Core_number','Frequ']
    order_by = ['HOSTNAME']
    search_list = ['HOSTNAME']
    action_list = [StarkConfig.multi_delete]
    # list_filter = ['hostname']
    list_display = [get_hostname,'Serian_Number','Producer_Name','Manufacturer']
    list_filter = [
        Option(field='Producer_Name',is_choice=False,is_multi=False,text_func=lambda x:x.Product_Name,value_func=lambda x:x.pk),
        Option(field='host_service',is_choice=False,is_multi=False,text_func=lambda x:x.name,value_func=lambda x:x.pk),
    ]
site.register(models.Host,HostConfig)
class ServiceConfig(StarkConfig):
    list_display = ['name']
site.register(models.Services,ServiceConfig)
class IDCFuncConfig(StarkConfig):
    list_display = ['name_func']
site.register(models.IDC_Func, IDCFuncConfig)