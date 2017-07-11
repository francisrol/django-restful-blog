# encoding=utf-8
from datetime import datetime
import json
from django.core import serializers
from django.core.paginator import Page
from django.db.models.query import QuerySet


class PageOrQuerySetSerializer(object):

    def __init__(self):
        self.pageAttr = ['has_next',
                         'has_previous',
                         'has_other_pages',
                         'start_index',
                         'end_index',]

    def serialize(self, obj=None):
        if isinstance(obj, Page):
            ret = dict([(key, obj.__getattribute__(key)()) for key in self.pageAttr])
            ret['object_list'] = self.serialize(obj.object_list)
            ret['number'] = obj.number
            return ret
        elif isinstance(obj, QuerySet):
            # datetime 实例序列化为字符串
            dtSer = lambda dt: dt.strftime("%Y-%m-%d %H:%M") if dt.year != datetime.now().year else dt.strftime("%m-%d %H:%M")
            # 模序类序列化为字典
            modelSer = lambda md, key: md.__dict__[key] if not isinstance(md.__dict__[key], datetime) else dtSer(md.__dict__[key])
            return [dict([(key, modelSer(model,key)) for key in model.allowedFields]) for model in obj ]



