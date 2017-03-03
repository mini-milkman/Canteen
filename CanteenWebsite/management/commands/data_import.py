# -*- coding: utf-8 -*-
import os

from django.core.management.base import BaseCommand

from CanteenWebsite.models import Goods
from CanteenWebsite.utils.data_importers import XlsDataImporter
from CanteenWebsite.utils.functions import setting_get_json


class Command(BaseCommand):
    help = "从XLS文件中导入数据"

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str, help="XLS文件")
        parser.add_argument('--filter', nargs='+', type=str, help="使用黑白名单")
        parser.add_argument('--clean_database', action='store_true', help="清空现有数据库")
        parser.add_argument('--delete_file', action='store_true', help="导入成功后删除文件")

    def handle(self, *args, **options):
        if options["clean_database"]:
            Goods.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('数据库中商品信息已清空'))

        importer = XlsDataImporter()
        for filename in options['filename']:
            try:
                self.stdout.write(self.style.SUCCESS('导入文件： %s' % filename))
                title = setting_get_json("column_index")
                counter_category, counter_items = importer.import_data(filename, title)
                self.stdout.write(self.style.SUCCESS('目前分类数： %s' % counter_category))
                self.stdout.write(self.style.SUCCESS('目前商品数： %s' % counter_items))
                if options["delete_file"]:
                    os.remove(filename)
                    self.stdout.write(self.style.SUCCESS('文件 %s 已删除' % filename))
            except:
                self.stdout.write(self.style.ERROR('文件 %s 导入出错' % filename))
