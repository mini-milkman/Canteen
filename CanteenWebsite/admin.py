from django.contrib import admin
from .models import Category
from .models import Goods
from .models import Setting


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']


admin.site.register(Category, CategoryAdmin)


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_real', 'commission', 'platform_type']
    list_filter = ['category', 'platform_type']


admin.site.register(Goods, GoodsAdmin)


class SettingAdmin(admin.ModelAdmin):
    list_display = ['name', 'value_show']

    def value_show(self, obj):
        if obj.is_json:
            return "JSON数据"
        else:
            return obj.value


admin.site.register(Setting, SettingAdmin)
