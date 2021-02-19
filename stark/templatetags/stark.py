from django.template import Library
from types import FunctionType


register = Library()

def header_list(cl):
    """
    表头
    :param cl:
    :return:
    """
    if cl.list_display:
        for name_or_func in cl.list_display:
            if isinstance(name_or_func, FunctionType):
                verbose_name = name_or_func(cl.config, header=True)
            else:
                verbose_name = cl.config.model_class._meta.get_field(name_or_func).verbose_name
            yield verbose_name
    else:
        yield cl.config.model_class._meta.model_name

def body_list(cl):
    """
    表格内容
    :param cl:
    :return:
    """
    for row in cl.queryset:
        row_list = []
        if not cl.list_display:
            row_list.append(row)
            yield row_list
            continue
        for name_or_func in cl.list_display:
            if isinstance(name_or_func, FunctionType):
                val = name_or_func(cl.config, row=row)
            else:
                val = getattr(row, name_or_func)
            row_list.append(val)
        yield row_list

def header_count(cl):
    business_list = cl.request.GET.getlist('bussiness')
    if not business_list:
        business_list=['Monitor','reportURLNUM','monitorURLNUM']
    row_list=['机房','时间']
    row_list.extend(business_list)
    return row_list
def body_coun(cl):
    business_list = cl.request.GET.getlist('bussiness')
    if not business_list:
        business_list=['Monitor','reportURLNUM','monitorURLNUM']
    row_list = ['机房', '时间']
    row_list.extend(business_list)
    queryset = cl.queryset

    for body in queryset:
        # print(body)
        row_list = []
        row_list.append(body["MonitorAddress__name"])
        row_list.append(body["inserttime"])
        for name in business_list:
            row_list.append(body['%s__sum' % name])
        yield row_list
def count_list(cl):
    business_list = cl.request.GET.getlist('bussiness')
    row_list = ['机房', '时间']
    row_list.extend(business_list)
    queryset = cl.queryset

    for body in queryset:
        row_list = []
        row_list.append(body.MonitorAddress__name)
        row_list.append(body.inserttime)
        for name in business_list:
            row_list.append('body.%s__sum' % name)
    yield row_list
@register.inclusion_tag('business_presen/table.html')
def table_count(cl):
    return {'header_list':header_count(cl),'body_list':body_coun(cl)}

@register.inclusion_tag('stark/table.html')
def table(cl):
    return {'header_list':header_list(cl),'body_list':body_list(cl)}

@register.filter
def get_obj_attr(obj, attr):
    return getattr(obj, attr)
