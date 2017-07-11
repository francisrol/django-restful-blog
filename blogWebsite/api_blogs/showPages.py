# encoding=utf-8
from django.shortcuts import render
from django.conf.urls import url

def index(request):
    return render(request, 'index.html')

def detail(request):
    return render(request, 'detail.html')

def create(request):
    return render(request, 'edit.html')

def edit(request):
    return render(request, 'edit.html')

urlpatterns = [
    url(r'^$', index),
    url(r'^category/.+?/$', index),
    url(r'^detail/.+?/$', detail),
    url(r'^edit/.+?/$', edit),
    url(r'^create/$', create),
]