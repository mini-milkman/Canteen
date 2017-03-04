# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin
from django.template.response import TemplateResponse

from .admin_forms import OptionsForm, DataImportOptionForm, DataImportForm
from .models import Category
from .models import Goods
from .models import Setting


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'goods_counter']
    list_display_links = ['id', 'category_name']

    def goods_counter(self, obj):
        return obj.goods_set.count()

    goods_counter.__name__ = "商品数量"


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price_real', 'commission', 'platform_type']
    list_display_links = ['id', 'name']
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

    def get_urls(self):
        urls = super(SettingAdmin, self).get_urls()
        my_urls = [
            url(r'^general_options/$', self.general_options, name="general_options"),
            url(r'^data_import_options/$', self.data_import_options, name="data_import_options"),
            url(r'^data_import/$', self.data_import, name="data_import")
        ]
        return my_urls + urls

    def general_form(self, request, ModelForm, form_url="", extra_context=None, title="设置"):
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES)
            if form.save():
                pass
            else:
                pass
        else:
            form = ModelForm()
        context = dict(
            self.admin_site.each_context(request),
            has_file_field=True,
            title=title,
            form=form,
            form_url=form_url
        )
        context.update(extra_context or {})
        return TemplateResponse(request,
                                "admin/canteen_form.html",
                                context
                                )

    def general_options(self, request, form_url='', extra_context=None):
        return self.general_form(request,
                                 OptionsForm,
                                 form_url=form_url,
                                 extra_context=extra_context,
                                 title="基本设置")

    def data_import_options(self, request, form_url='', extra_context=None):
        return self.general_form(request,
                                 DataImportOptionForm,
                                 form_url=form_url,
                                 extra_context=extra_context,
                                 title="数据导入设置")

    def data_import(self, request, form_url='', extra_context=None):
        return self.general_form(request,
                                 DataImportForm,
                                 form_url=form_url,
                                 extra_context=extra_context,
                                 title="数据导入")
