from django.contrib import admin
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
