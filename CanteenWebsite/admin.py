from django.contrib import admin
from django.contrib.admin import AdminSite
from django.http import HttpResponse
from .models import Category
from .models import Goods
from .models import Setting


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_real', 'commission', 'platform_type']
    list_filter = ['category', 'platform_type']


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['name', 'value_show']

    def value_show(self, obj):
        if obj.is_json:
            return "JSON数据"
        else:
            return obj.value

    value_show.__name__ = "值"


class CanteenAdminSite(AdminSite):
    site_header = 'Monty Python administration'

    def get_urls(self):
        from django.conf.urls import url
        urls = super(CanteenAdminSite, self).get_urls()
        urls += [
            url(r'^general_options/$', self.admin_view(self.general_options)),
            url(r'^data_import_options/$', self.admin_view(self.data_import_options)),
            url(r'^data_import/$', self.admin_view(self.data_import))
        ]
        return urls

    def general_options(self, request):
        return HttpResponse("General Options")

    def data_import_options(self, request):
        return HttpResponse("Data Import Options")

    def data_import(self, request):
        return HttpResponse("Data Import")


canteen_admin_site = CanteenAdminSite()
