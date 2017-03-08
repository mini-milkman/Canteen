# -*- coding: utf-8 -*-
import threading

from django import forms
from django.contrib import messages

from CanteenWebsite.utils.data_importers import XlsDataImporter
from CanteenWebsite.utils.functions import setting_get
from CanteenWebsite.utils.functions import setting_get_json
from CanteenWebsite.utils.functions import setting_set
from CanteenWebsite.utils.functions import setting_set_json


class MessageMixin:
    def get_message(self, message_type):
        msg = {
            messages.SUCCESS: "设置保存成功",
            messages.ERROR: "设置保存失败"
        }
        if message_type in msg:
            return msg[message_type]
        else:
            return str(message_type)


class OptionsForm(forms.Form, MessageMixin):
    site_name = forms.CharField(
        label='站点名称',
        max_length=100
    )
    site_slogan = forms.CharField(
        label="站点副标题",
        max_length=100,
        required=False
    )
    index_page = forms.ChoiceField(
        label="首页显示内容",
        initial="random",
        choices=(
            ('random', '随机'),
            ('blank', '空白'),
        )
    )
    goods_per_page = forms.IntegerField(
        label="每页显示商品数量",
        initial=50,
        min_value=1
    )
    goods_sort_strategy = forms.ChoiceField(
        label="商品排序方式",
        initial='None',
        choices=(
            ('None', '随机/不排序'),
            ('id', '商品ID'),
            ('commission', '佣金 从低到高'),
            ('-commission', '佣金 从高到低'),
            ('commission_rate', '佣金比率 从低到高'),
            ('-commission_rate', '佣金比率 从高到低'),
            ('coupon_time_end', '优惠券结束时间 从早到晚'),
            ('-coupon_time_end', '优惠券结束时间 从晚到早'),
            ('price_real', '商品实际购买价格 从低到高'),
            ('-price_real', '商品实际购买价格 从高到低'),
        )
    )
    goods_list_style = forms.ChoiceField(
        label="商品显示样式",
        initial='style_1',
        choices=(
            ('style_1', '上图下介绍'),
            ('style_2', '左图右介绍'),
        )
    )

    @classmethod
    def get_initial_data(cls):
        initial_data = dict(
            site_name=setting_get("site_name"),
            site_slogan=setting_get("site_slogan"),
            index_page=setting_get("index_page"),
            goods_per_page=int(setting_get("goods_per_page", 50)),
            goods_sort_strategy=setting_get("goods_sort_strategy"),
            goods_list_style=setting_get("goods_list_style"),
        )
        return initial_data

    def save(self):
        save_succeed = False
        if self.is_valid():
            for key, value in self.cleaned_data.items():
                setting_set(key, value)
            save_succeed = True
        return save_succeed


class DataImportOptionForm(forms.Form, MessageMixin):
    column_index = forms.CharField(
        label="文件导入结构",
        max_length=1000
    )
    delete_before_import = forms.BooleanField(
        label="导入前清空",
        initial=False,
        required=False
    )

    # 分类黑白名单
    blacklist_category_active = forms.BooleanField(
        label="使用分类黑名单",
        initial=False,
        required=False
    )
    blacklist_category = forms.CharField(
        label="分类黑名单",
        widget=forms.Textarea,
        required=False
    )
    whitelist_category_active = forms.BooleanField(
        label="使用分类白名单",
        initial=False,
        required=False
    )
    whitelist_category = forms.CharField(
        label="分类白名单",
        widget=forms.Textarea,
        required=False
    )

    # 商品黑白名单
    blacklist_goods_active = forms.BooleanField(
        label="使用商品黑名单",
        initial=False,
        required=False
    )
    blacklist_goods = forms.CharField(
        label="商品黑名单",
        widget=forms.Textarea,
        required=False
    )
    whitelist_goods_active = forms.BooleanField(
        label="使用商品白名单",
        initial=False,
        required=False
    )
    whitelist_goods = forms.CharField(
        label="商品白名单",
        widget=forms.Textarea,
        required=False
    )

    @classmethod
    def get_initial_data(cls):
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
        return initial_data

    def save(self):
        save_succeed = False
        if self.is_valid():
            # 文件结构
            data = list()
            for x in self.cleaned_data['column_index'].split(','):
                try:
                    data.append(int(x))
                except:
                    data.append(0)
            setting_set_json("column_index", data)

            # 不需要使用特殊包裹的
            for key in ["delete_before_import",
                        "blacklist_category_active", "whitelist_category_active",
                        "blacklist_goods_active", "whitelist_goods_active"]:
                setting_set_json(key, self.cleaned_data[key])

            # 需要变成列表的
            for key in ["blacklist_category", "whitelist_category",
                        "blacklist_goods", "whitelist_goods"]:
                data = self.cleaned_data[key].strip().split(',')
                data = [x.strip() for x in data]
                setting_set_json(key, data)
            save_succeed = True
        return save_succeed


class DataImportForm(forms.Form, MessageMixin):
    file = forms.FileField(
        label="选择文件"
    )

    def save(self):
        save_succeed = False
        if self.is_valid():
            title = setting_get_json("column_index")
            importer = XlsDataImporter()
            # 由于数据量很大，这里新开一个线程进行数据导入
            th = threading.Thread(
                target=importer.import_data,
                args=(self.cleaned_data['file'].temporary_file_path(),
                      title,)
            )
            th.start()
            save_succeed = True
        return save_succeed

    @classmethod
    def get_initial_data(cls):
        initial_data = dict()
        return initial_data

    def get_message(self, message_type):
        msg = {
            messages.SUCCESS: "数据上传成功！\n导入中……",
            messages.ERROR: "数据上传失败"
        }
        if message_type in msg:
            return msg[message_type]
        else:
            return str(message_type)
