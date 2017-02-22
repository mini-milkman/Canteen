import os
import pandas as pd
from CanteenWebsite.models import Category, Goods


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
        # 导入数据
        counter_category, counter_goods = self.__import_data(data_source)

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
                item_category = item[index["商品一级类目"]]
                if item_category in category_cache:
                    category = category_cache[item_category]
                else:
                    category = Category(category_name=item_category)
                    category.save()
                    category_cache[item_category] = category
                # 拿到了Category，下面创建Goods
                goods = Goods()
                try:
                    goods.save()
                except:
                    pass
            except:
                pass
        counter_category = 0
        counter_goods = 0
        return counter_category, counter_goods


class XlsDataImporter(DataImporter):
    def __init__(self):
        pass

    def import_data(self, filename, title=""):
        counter_category = 0
        counter_goods = 0
        index = self.__match_title(title)
        if os.path.exists(filename):
            with pd.ExcelFile("data.xls") as xls_file:
                counter_category, counter_goods = self.__import_data(xls_file.parse(0), index)
        return counter_category, counter_goods
