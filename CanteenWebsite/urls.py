from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<category_id>[0-9]+)/$', views.category, name='category'),
    url(r'^search/(?P<key_word>[\S]+)/$', views.search, name='search'),
]
