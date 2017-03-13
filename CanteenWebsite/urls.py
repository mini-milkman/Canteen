# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^category/(?P<category_id>[0-9]+)/$', views.category, name='category'),
    url(r'^detail/(?P<goods_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^search/(?P<key_word>[\S]+)/$', views.search, name='search'),
]
