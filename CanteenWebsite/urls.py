from django.conf.urls import url

from . import views
from CanteenWebsite.admin import canteen_admin_site

urlpatterns = [
    url(r"^admin/", canteen_admin_site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^(?P<category_id>[0-9]+)/$', views.category, name='category'),
    url(r'^search/(?P<key_word>[\S]+)/$', views.search, name='search'),
]
