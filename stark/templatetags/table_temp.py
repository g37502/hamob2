# -*- coding:utf-8 -*-
#  2020/11/16 
#  table_temp.py
#  
# author:gyl

from django.template import Library
from stark.utils.log_ctrl import logger
register = Library()
from stark.utils.pagination import Pagination
@register.inclusion_tag('stark/change_tmp.html')
def changelist_tmp(c1):
    config = c1.config
    query_set = c1.query_set
    header_list = config.get_header_list()
    body_list = config.get_body_list(query_set)
    action_list = c1.action_list
    q = c1.q
    page = c1.page
    return {'header_list':header_list,'body_list': body_list,'action_list':action_list,'q':q,'page':page}

@register.inclusion_tag('hardmanage/table_tmp.html')
def host_table_tmp(obj,list_name):
    logger.debug(obj)
    head_list = []
    body_list = []
    for name in list_name:
        logger.debug(name)
        head_list.append(obj._meta.get_field(name).verbose_name)
        body_list.append(getattr(obj,name))
    logger.debug(head_list)
    logger.debug(body_list)
    return {'head_list':head_list,'body_list':body_list}