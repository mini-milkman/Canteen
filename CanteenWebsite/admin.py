# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import reverse

from CanteenWebsite.utils.functions import setting_get, setting_get_json
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

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    def get_urls(self):
        urls = super(SettingAdmin, self).get_urls()
        my_urls = [
            url(r'^general_options/$', self.general_options, name="general_options"),
            url(r'^data_import_options/$', self.data_import_options, name="data_import_options"),
            url(r'^data_import/$', self.data_import, name="data_import")
        ]
        return my_urls + urls

    def general_form(self, request, ModelForm, form_url="", extra_context=None, title="设置", initial={}):
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES)
            if form.save():
                pass
            else:
                pass
        else:
            form = ModelForm(initial=initial)
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

    def general_options(self, request, extra_context=None):
        if request.method == 'POST':
            initial_data = None
        else:
            initial_data = dict(
                site_name=setting_get("site_name"),
                site_slogan=setting_get("site_slogan"),
                index_page=setting_get("index_page"),
                goods_per_page=int(setting_get("goods_per_page", 50)),
                goods_sort_strategy=setting_get("goods_sort_strategy"),
                goods_list_style=setting_get("goods_list_style"),
            )
        return self.general_form(request,
                                 OptionsForm,
                                 form_url=reverse("admin:general_options"),
                                 extra_context=extra_context,
                                 title="基本设置",
                                 initial=initial_data)

    def data_import_options(self, request, extra_context=None):
        if request.method == 'POST':
            initial_data = None
        else:
            initial_data = dict(
                column_index=str(setting_get_json("column_index")).strip('[]'),
                delete_before_import=setting_get_json("delete_before_import"),
                blacklist_category_active=setting_get_json("blacklist_category_active"),
                blacklist_category=','.join(setting_get_json("blacklist_category", [])),
                whitelist_category_active=setting_get_json("whitelist_category_active"),
                whitelist_category=','.join(setting_get_json("whitelist_category", [])),
                blacklist_goods_active=setting_get_json("blacklist_goods_active"),
                blacklist_goods=','.join(setting_get_json("blacklist_goods", [])),
                whitelist_goods_active=setting_get_json("whitelist_goods_active"),
                whitelist_goods=','.join(setting_get_json("whitelist_goods", [])),
            )
        return self.general_form(request,
                                 DataImportOptionForm,
                                 form_url=reverse("admin:data_import_options"),
                                 extra_context=extra_context,
                                 title="数据导入设置",
                                 initial=initial_data)

    def data_import(self, request, extra_context=None):
        return self.general_form(request,
                                 DataImportForm,
                                 form_url=reverse("admin:data_import"),
                                 extra_context=extra_context,
                                 title="数据导入")
