# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=31, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98')),
                ('keyWords', models.CharField(default=b'', max_length=100, verbose_name=b'\xe5\x85\xb3\xe9\x94\xae\xe5\xad\x97')),
                ('summary', models.TextField(verbose_name=b'\xe6\x91\x98\xe8\xa6\x81')),
                ('content', models.TextField(verbose_name=b'\xe6\xad\xa3\xe6\x96\x87')),
                ('createdTime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('lastEditTime', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9c\x80\xe5\x90\x8e\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('category', models.CharField(default=b'web', max_length=15, verbose_name=b'\xe5\x88\x86\xe7\xb1\xbb', choices=[(1, b'\xe6\x9c\xba\xe5\x99\xa8\xe5\xad\xa6\xe4\xb9\xa0'), (2, b'\xe7\x88\xac\xe8\x99\xab'), (3, b'\xe6\x95\xb0\xe6\x8d\xae\xe5\x88\x86\xe6\x9e\x90'), (4, b'web'), (5, b'\xe6\x95\xb0\xe6\x8d\xae\xe7\xbb\x93\xe6\x9e\x84'), (6, b'HTTP')])),
                ('family', models.CharField(default=b'\xe5\x85\xb6\xe4\xbb\x96', max_length=63, verbose_name=b'\xe7\xb3\xbb\xe5\x88\x97', choices=[(1, b'\xe6\x9d\x82\xe6\x96\x87\xe7\xac\x94\xe8\xae\xb0'), (-1, b'\xe5\x85\xb6\xe4\xbb\x96')])),
                ('visitedNumber', models.IntegerField(default=0, verbose_name=b'\xe8\xae\xbf\xe9\x97\xae\xe9\x87\x8f')),
                ('slug', models.SlugField(max_length=100, verbose_name=b'url\xe5\x90\x8d\xe7\xa7\xb0')),
            ],
        ),
    ]
