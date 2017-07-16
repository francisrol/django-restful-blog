# encoding=utf-8

import os
from functools import wraps
from django.shortcuts import render
from django.conf import settings


class Permission(object):

    __instance = None
    # 单例模式
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Permission, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def hasEditPermission(self, func):
        '''
        是否有编辑权限
        :return:
        '''
        @wraps(func)
        def inner(request, *args, **kwargs):
            permissionCodeName = request.session.get("permissionCodeName", '')
            permissionCodePasswd = request.session.get("permissionCodePasswd", '')
            if not self.getPermissionCode(permissionCodeName, permissionCodePasswd):
                # return HttpResponse("很抱歉，您没有访问该页面的权限！",status=403)
                return render(request, 'error/403.html', {"message":"很抱歉，您没有访问该页面的权限"}, status=403)
            return func(request, *args, **kwargs)
        return inner

    def allowedMethod(self, methods=[]):
        '''
        判断是否是允许的HTTP方法
        :param func:
        :return:
        '''
        def decorator(func):
            @wraps(func)
            def inner(request, *args, **kwargs):
                if request.method not in methods:
                    return render(request, 'error/405.html', {"message": "only allowed %s method"%methods}, status=405)
                return func(request, *args, **kwargs)
            return inner
        return decorator

    def getPermissionCode(self,loginName , loginPasswd):
        '''
        从系统环境变量中，提取秘钥token信息
        :return:
        '''
        return loginName == os.environ.get(settings.LOGINNAME) and loginPasswd== os.environ.get(settings.LOGINPASSWD)



permission = Permission()
