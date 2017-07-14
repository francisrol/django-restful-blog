# encoding=utf-8

import os
from functools import wraps
from django.shortcuts import render


class Permission(object):

    # def __new__(cls, *args, **kwargs):
    #     return super(Permission, cls).__new__(*args, **kwargs)

    def hasEditPermission(self, func):
        '''
        是否有编辑权限
        :return:
        '''
        @wraps(func)
        def inner(request, *args, **kwargs):
            permissionCode = request.session.get("permissionCode", '')
            if permissionCode != self.getPermissionCode():
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

    def getPermissionCode(self):
        '''
        从系统环境变量中，提取秘钥token信息
        :return:
        '''
        return os.environ.get('BLOGPERMISSION')


permission = Permission()
