# -*- coding:utf-8 -*-
#  2021/1/7 
#  routes.py
#  
# author:gyl
import re

def check_url_exclude(url):
    """
    排除特定的url
    :param url:
    :return:
    """
    exclude_url = [
        '/admin/.*',
        '/login/',
        '/index/',
    ]
    for regex in settings.AUTO_DISCOVER_EXCLUDE:
        if re.match(regex, url):
            return True


from django.urls.resolvers import URLPattern, URLResolver


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """
        用来做递归的函数
        递归的获取URL
    :param pre_namespace: namespace的前缀(rbac:xxx)，用于拼接name
    :param pre_url:url的前缀(/url/...)，用于拼接url
    :param urlpatterns: 路由关系列表
    :param url_ordered_dict: 用于保存递归中所有路由
    :return:
    """
    for item in urlpatterns:
        if isinstance(item, URLPattern):  # 非路由分发，吧路由添加到url_ordered_dict
            if not item.name:
                continue

            if pre_namespace:
                name = "%s:%s" % (pre_namespace, item.name)
            else:
                name = item.name
            url = pre_url + item.pattern.regex.pattern  # url拼接完是这个样子/^rbac/^user/edit/(xx/x)/$
            url = url.replace('^', '').replace('$', '')
            if check_url_exclude(url):
                continue

            url_ordered_dict[name] = {'name': name, 'url': url}

        elif isinstance(item, URLResolver):  # 路由分发，递归
            if pre_namespace:
                if item.namespace:
                    namespace = "%s:%s" % (pre_namespace, item.namespace)
                else:
                    namespace = item.namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            recursion_urls(namespace, pre_url + item.pattern.regex.pattern, item.url_patterns, url_ordered_dict)


from collections import OrderedDict  # 导入有序字典
from django.conf import settings
from django.utils.module_loading import import_string  # 根据字符串的形式来导入模块


def get_all_url_dict(ignore_namespace_list=None):
    """
        获取项目中所有的url
        url的路由中必须定义name='xxx'作为标记
        没有就忽略
    """
    ignore_list = ignore_namespace_list or []
    url_ordered_dict = OrderedDict()
    """
    {
        'rbac:menu_list':{name:'rbac:menu_list',url:'xxxx/x/menu/list'}
    }
    """

    md = import_string(settings.ROOT_URLCONF)  # from luff..import urls
    urlpatterns = []

    for item in md.urlpatterns:
        try:
            if item.namespace in ignore_list:
                continue
        except:
            break
        urlpatterns.append(item)
    # print(md.urlpatterns)
    recursion_urls(None, '/', urlpatterns, url_ordered_dict)  # 递归获取所有的路由
    return url_ordered_dict


def multi_permissions(request):
    """
    36:43
    批量操作权限
    :param request:
    :return:
    """
    all_url_dict = get_all_url_dict()
    for k, v in all_url_dict.items():
        print(k, v)