# encoding=utf-8

from django.conf.urls import url
# 导入所有的视图函数
from api_blogs.views import *

urlpatterns = [
    url(r'^list/$', blogList),  # 博客列表
    url(r'^list/category/(?P<category>.*?)/$', blogList),  # 博客列表
    url(r'^list/family/(?P<family>.*?)/$', blogList),  # 博客列表
    url(r'^detail/(?P<slug>.+)?/$', blogDetail),  # 博客详情
    url(r'^create/$', createBlog),  # 创建博客
    url(r'^edit/(?P<slug>.+)?/$', editBlog),  # 博客编辑
    url(r'^delete/(?P<slug>.+)?/$', deleteBlog),  # 删除博客
    url(r'^categories/$', getCategories),  # 博客分类
    url(r'^allFamily/$', getBlogFamily),  # 博客系列
    url(r"^getPermission/$", getPermission)   # 获取权限
]

