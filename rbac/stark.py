# -*- coding:utf-8 -*-
#  2021/1/12 
#  stark.py
#  
# author:gyl
from django.conf import settings
from stark.service.stark import StarkConfig
from stark.service.stark import site
from rbac import models
import copy

class RbacPermission(object):

    def get_add_btn(self):
        name = "%s:%s" % (self.site.namespace, self.get_add_url_name,)
        name = self.get_add_url_name
        permission_dict = self.request.session.get(settings.PERMISSION_SESSION_KEY)
        # print(permission_dict)
        if name in permission_dict:
            return super().get_add_btn()

    # def get_list_display(self):
    #     # val = super().get_list_display()
    #     val = copy.deepcopy(self.list_display)
    #     permission_dict = self.request.session.get(settings.PERMISSION_SESSION_KEY)
    #     # edit_name = "%s:%s" % (self.site.namespace, self.get_change_url_name,)
    #     # del_name = "%s:%s" % (self.site.namespace, self.get_del_url_name,)
    #     edit_name = self.get_change_url_name
    #     del_name = self.get_del_url_name
    #     if edit_name in permission_dict and del_name in permission_dict:
    #         val.append(StarkConfig.display_edit_del)
    #         return val
    #     elif edit_name in permission_dict:
    #         val.append(StarkConfig.display_edit)
    #         return val
    #     elif del_name in permission_dict:
    #         val.append(StarkConfig.display_del)
    #         return val
    #     # if edit_name not in permission_dict:
    #     #     print('edit_name 不在权限中')
    #     #     val.remove(StarkConfig.display_edit)
    #     #     # print(val)
    #     # if del_name not in permission_dict:
    #     #     print('del_name 不在权限中')
    #     #     val.remove(StarkConfig.display_del)
    #     # if edit_name and del_name not in permission_dict:
    #     #     print(1111)
    #     #     try:
    #     #         val.remove(StarkConfig.display_edit_del)
    #     #     except:
    #     #         pass
    #     # return val

class UserInfoConfig(StarkConfig):
    list_display = ['id','username']
site.register(models.UserInfo,UserInfoConfig)
