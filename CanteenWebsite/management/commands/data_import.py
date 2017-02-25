import os
from django.core.management.base import BaseCommand, CommandError
from CanteenWebsite.models import Category, Goods
from CanteenWebsite.functions.data_import import XlsDataImporter
from CanteenWebsite.functions.util import setting_get_json


class Command(BaseCommand):
    help = "从XLS文件中导入数据"

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str, help="XLS文件")
        parser.add_argument('--filter', nargs='+', type=str, help="使用黑白名单")
        parser.add_argument('--delete', action='store_true', help="清空现有数据库")

    def handle(self, *args, **options):
        importer = XlsDataImporter()
        for filename in options['filename']:
            try:
                self.stdout.write(self.style.SUCCESS('导入文件： %s' % filename))
                title = setting_get_json("column_index")
                counter_category, counter_items = importer.import_data(filename, title)
                self.stdout.write(self.style.SUCCESS('目前分类数： %s' % counter_category))
                self.stdout.write(self.style.SUCCESS('目前商品数： %s' % counter_items))
            except:
                self.stdout.write(self.style.ERROR('文件 %s 导入出错' % filename))