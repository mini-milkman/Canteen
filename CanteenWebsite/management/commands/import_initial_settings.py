from django.core.management.base import BaseCommand

from CanteenWebsite.functions.util import setting_set, setting_set_json


class Command(BaseCommand):
    help = "导入网站初始设置"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("导入网站初始设置"))

        # 站点名称
        setting_set("site_name", "Canteen")
        # 站点副标题
        setting_set("site_slogan", "发现好物")
        # 首页显示什么 random/none
        setting_set("index_page", "random")
        # 每页显示多少商品
        setting_set("goods_per_page", 50)
        # 商品排序方式
        setting_set("goods_sort_strategy", "None")
        # 商品显示方式
        setting_set("goods_list_style", "style_1")

        # 文件结构
        setting_set_json("column_index", [0, 1, 2, 4, 5, 6, 8, 9, 12, 13, 17, 18, 19, 20, 21])
        # 导入前清空
        setting_set_json("delete_before_import", False)
        # 分类黑名单
        setting_set_json("blacklist_category_active", False)
        setting_set_json("blacklist_category", [])
        # 分类白名单
        setting_set_json("whitelist_category_active", False)
        setting_set_json("whitelist_category", [])
        # 商品黑名单
        setting_set_json("blacklist_goods_active", False)
        setting_set_json("blacklist_goods", [])
        # 商品白名单
        setting_set_json("whitelist_goods_active", False)
        setting_set_json("whitelist_goods", [])

        self.stdout.write(self.style.SUCCESS("完成"))
