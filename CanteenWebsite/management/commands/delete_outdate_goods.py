# -*- coding: utf-8 -*-
import os
from django.core.management.base import BaseCommand, CommandError
from CanteenWebsite.utils.functions import delete_outdated_goods
from CanteenWebsite.models import Goods, Category


class Command(BaseCommand):
    help = "清理过期商品"

    def handle(self, *args, **options):
        goods_deleted = delete_outdated_goods()
        self.stdout.write(self.style.SUCCESS("共清理{}件过期商品".format(goods_deleted)))

        counter_category = Category.objects.count()
        counter_goods = Goods.objects.count()
        self.stdout.write(self.style.SUCCESS('目前分类数： %s' % counter_category))
        self.stdout.write(self.style.SUCCESS('目前商品数： %s' % counter_goods))

        self.stdout.write(self.style.SUCCESS("完成"))
