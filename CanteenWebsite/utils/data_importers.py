# -*- coding: utf-8 -*-
import datetime
import os

import pandas as pd
from dateutil.parser import parse as date_parse
from tqdm import tqdm

from CanteenWebsite.models import Category, Goods
from CanteenWebsite.utils.functions import calculate_real_price, value_set_select, delete_outdated_goods


class DataImporter:
    COLUMNS = ['id',
               'name',
               'picture',
               'category',
               'url_affiliate',
               'price',
               'commission_rate',
               'commission',
               'shop_name',
               'platform_type',
               'coupon_money',
               'coupon_time_start',
               'coupon_time_end',
               'url_coupon',
               'url_affiliate_coupon'],

    def import_data(self, data_source, title):
        """
        从数据源中导入数据
        """
        index = self._match_title(title)
        # 导入数据
        counter_category, counter_goods = self._import_data(data_source, index)

        # 返回结果
        return counter_category, counter_goods

    def _match_title(self, title_index):
        """
        需要的title在给出数据的第几列？制作一个对应关系表
        """
        # 补齐
        while len(title_index) < len(self.__class__.COLUMNS):
            title_index.append(None)
        # 作出对应关系表
        result = dict()
        for ith, x in enumerate(self.__class__.COLUMNS[0]):
            result[x] = title_index[ith]
        return result

    def _import_data(self, data, index):
        """
        导入数据
        这里 data 使用 numpy 数据格式
        """
        category_cache = dict()
        # 导入
        with tqdm(total=len(data), unit="items") as progressbar:
            for item in data:
                progressbar.update(1)
                try:
                    # Category比较少，可以进行一个缓存，避免太频繁读取数据库
                    item_category = value_set_select(index["category"], item, None, str).strip()
                    if item_category is None:
                        continue
                    if item_category in category_cache:
                        category = category_cache[item_category]
                    else:
                        category, _ = Category.objects.get_or_create(category_name=item_category)
                        category_cache[item_category] = category

                    # 继续拿其他信息
                    goods_price = value_set_select(index["price"], item, 0, float)
                    goods_coupon_money = value_set_select(index["coupon_money"], item, "", str)

                    # 写进数据库
                    Goods.objects.update_or_create(
                        id=int(item[index["id"]]),
                        defaults={
                            'category': category,
                            'name': str(item[index["name"]]),
                            'picture': str(item[index["picture"]]),
                            'url_affiliate': str(item[index["url_affiliate"]]),
                            'price': float(item[index["price"]]),
                            'commission_rate': value_set_select(index["commission_rate"], item, 0, float),
                            'commission': value_set_select(index["commission"], item, 0, float),
                            'shop_name': value_set_select(index["shop_name"], item, "", str),
                            'platform_type': value_set_select(index["platform_type"], item, "其他", str),
                            'coupon_money': value_set_select(index["coupon_money"], item, "", str),
                            'coupon_time_start': value_set_select(index["coupon_time_start"], item,
                                                                  datetime.date.today(),
                                                                  date_parse),
                            'coupon_time_end': value_set_select(index["coupon_time_end"], item,
                                                                datetime.date.today() + datetime.timedelta(days=30),
                                                                date_parse),
                            'url_coupon': value_set_select(index["url_coupon"], item, "", str),
                            'url_affiliate_coupon': value_set_select(index["url_affiliate_coupon"], item, "", str),
                            'price_real': calculate_real_price(goods_price, goods_coupon_money),
                        }
                    )
                except Exception as e:
                    # print(e)
                    pass
        # 清理过期商品
        delete_outdated_goods()

        counter_category = Category.objects.count()
        counter_goods = Goods.objects.count()
        return counter_category, counter_goods


class XlsDataImporter(DataImporter):
    def import_data(self, filename, title=None):
        counter_category = 0
        counter_goods = 0
        if os.path.exists(filename):
            with pd.ExcelFile(filename) as xls_file:
                try:
                    data_sheet = xls_file.parse(0)
                    index = self._match_title(title)
                    counter_category, counter_goods = self._import_data(data_sheet.values, index)
                except Exception as e:
                    print(e)
                    counter_category = Category.objects.count()
                    counter_goods = Goods.objects.count()

        return counter_category, counter_goods
