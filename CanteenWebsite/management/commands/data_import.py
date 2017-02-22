import os
from django.core.management.base import BaseCommand, CommandError
from CanteenWebsite.models import Category, Goods
from CanteenWebsite.functions.data_import import XlsDataImporter


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
                counter_category, counter_items = importer.import_data(filename)
                self.stdout.write(self.style.SUCCESS('文件： %s' % filename))
                self.stdout.write(self.style.SUCCESS('分类数： %s' % counter_category))
                self.stdout.write(self.style.SUCCESS('商品数： %s' % counter_items))
            except:
                self.stdout.write(self.style.ERROR('文件 %s 导入出错' % filename))
