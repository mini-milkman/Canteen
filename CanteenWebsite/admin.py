from django.contrib import admin
from django.contrib.admin import AdminSite
from django.http import HttpResponse
from .models import Category
from .models import Goods
from .models import Setting
from django.urls import reverse


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'goods_counter']

    def goods_counter(self, obj):
        return obj.goods_set.count()

    goods_counter.__name__ = "商品数量"


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
