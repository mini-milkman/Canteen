import os
from django.core.management.base import BaseCommand, CommandError
from CanteenWebsite.functions.util import setting_set, setting_set_json


class Command(BaseCommand):
    help = "基本设置"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("导入默认设置"))
        # 站点名称
        setting_set_json("site_name", "Canteen")
        # 站点副标题
        setting_set_json("site_slogan", "发现好物")
        # 首页显示什么 random/none
        setting_set_json("index_page", "random")
        # 每页显示多少商品
        setting_set_json("goods_per_page", 50)
        # 每页显示多少商品
        setting_set_json("goods_per_page", "style_1")
        # 文件结构
        setting_set_json("column_index", [0, 1, 2, 4, 5, 6, 8, 9, 12, 13, 17, 18, 19, 20, 21])
        # 导入前清空
        setting_set_json("delete_before_import", False)
        # 分类黑名单
        setting_set_json("blacklist_category", {"active": False, "list": []})
        # 分类白名单
        setting_set_json("whitelist_category", {"active": False, "list": []})
        # 商品黑名单
        setting_set_json("blacklist_goods", {"active": False, "list": []})
        # 商品白名单
        setting_set_json("whitelist_goods", {"active": False, "list": []})

        self.stdout.write(self.style.SUCCESS("完成"))