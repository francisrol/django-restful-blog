# encoding=utf-8
from django.db import models
from uuslug import uuslug
from django.conf import settings

from django.contrib.auth.models import User

# Create your models here.

class BlogModel(models.Model):
    allowedFields = ['title','keyWords','summary','content','createdTime','lastEditTime','category', 'family','visitedNumber','slug']
    # 标题
    title = models.CharField('标题', max_length=31)
    # 关键字
    keyWords = models.CharField('关键字', max_length=100, default='')
    # 简要
    summary = models.TextField('摘要')
    # 正文
    content = models.TextField('正文')
    # 创建时间
    # auto_now_add为True: 当第一次创建实例时，自动添加当前时间，并且不会再被更改
    createdTime = models.DateTimeField('创建时间', auto_now_add=True)
    # 最后更新时间
    # auto_now为True: 每次调用对象的save方式时，将会把当前时间自动更新
    lastEditTime = models.DateTimeField('最后更新时间', auto_now=True)
    # 分类
    # 提供选项卡功能：添加choices关键字参数
    # 默认为web
    category = models.CharField('分类', max_length=15, default='web', choices=settings.CATEGORIES)
    # 系列
    family = models.CharField('系列', max_length=63, default='其他', choices=settings.BLOGFAMILY)
    # 访问量
    visitedNumber = models.IntegerField('访问量', default=0)

    slug = models.SlugField('url名称', max_length=100)

    def save(self, *args, **kwargs):
        # 将文章标题转换为用于显示的url
        self.slug = uuslug(self.title, instance=self, start_no=2)
        super(BlogModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.title.encode('utf-8')  # python2


