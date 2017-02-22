import os
import pandas as pd
from CanteenWebsite.models import Category, Goods
from CanteenWebsite.functions.util import calculate_real_price, value_set_select
from dateutil.parser import parse as date_parse
import datetime


class DataImporter:
    COLUMNS = ['商品id',
               '商品名称',
               '商品主图',
               '商品一级类目',
               '淘宝客链接',
               '商品价格(单位：元)',
               '收入比率(%)',
               '佣金',
               '店铺名称',
               '平台类型',
               '优惠券面额',
               '优惠券开始时间',
               '优惠券结束时间',
               '优惠券链接',
               '商品优惠券推广链接'],

    def import_data(self, data_source, title):
        """
        从数据源中导入数据
        """
        index = self.__match_title(title)
        # 导入数据
        counter_category, counter_goods = self.__import_data(data_source, index)

        # 返回结果
        return counter_category, counter_goods

    def __match_title(self, title):
        """
        匹配给出的title和需要的title
        """
        result = dict()
        for x in self.__class__.COLUMNS:
            if x in title:
                result[x] = title.index(x)
            else:
                result[x] = None

        return result

    def __import_data(self, data, index):
        """
        导入数据
        这里 data 使用 numpy 数据格式
        """
        category_cache = dict()
        # 导入
        for item in data:
            try:
                # Category比较少，可以进行一个缓存，避免太频繁读取数据库
                item_category = value_set_select(index["商品一级类目"], item, None, str)
                if item_category is None:
                    continue
                if item_category in category_cache:
                    category = category_cache[item_category]
                else:
                    category = Category(category_name=item_category)
                    category.save()
                    category_cache[item_category] = category
                # 继续拿其他信息
                goods_price = value_set_select(index["商品价格(单位：元)"], item, 0, float)
                goods_coupon_money = value_set_select(index["优惠券面额"], item, "", str)
                # 写进数据库
                try:
                    category.goods_set.create(
                        id=int(item[index["商品id"]]),
                        name=str(item[index["商品名称"]]),
                        picture=str(item[index["商品主图"]]),
                        url_affiliate=str(item[index["淘宝客链接"]]),
                        price=float(item[index["商品价格(单位：元)"]]),
                        commission_rate=value_set_select(index["收入比率(%)"], item, 0, float),
                        commission=value_set_select(index["佣金"], item, 0, float),
                        shop_name=value_set_select(index["店铺名称"], item, "", str),
                        platform_type=value_set_select(index["平台类型"], item, "其他", str),
                        coupon_money=value_set_select(index["优惠券面额"], item, "", str),
                        coupon_time_start=value_set_select(index["优惠券开始时间"], item,
                                                           datetime.date.today(),
                                                           date_parse),
                        coupon_time_end=value_set_select(index["优惠券结束时间"], item,
                                                         datetime.date.today() + datetime.timedelta(days=30),
                                                         date_parse),
                        url_coupon=value_set_select(index["优惠券链接"], item, "", str),
                        url_affiliate_coupon=value_set_select(index["商品优惠券推广链接"], item, "", str),
                        price_real=calculate_real_price(goods_price, goods_coupon_money),
                    )
                except:
                    pass
            except:
                pass
        counter_category = 0
        counter_goods = 0
        return counter_category, counter_goods


class XlsDataImporter(DataImporter):
    def import_data(self, filename, title=None):
        counter_category = 0
        counter_goods = 0
        if os.path.exists(filename):
            with pd.ExcelFile(filename) as xls_file:
                data_sheet = xls_file.parse(0)
                if title is None:
                    title = [x for x in data_sheet.columns]
                index = self.__match_title(title)
                counter_category, counter_goods = self.__import_data(data_sheet.values, index)

        return counter_category, counter_goods
