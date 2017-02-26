# Canteen

一个懒人版淘宝客系统

## 系统依赖

1. Python 3
1. django
1. django-material
1. pandas
1. tqdm

## 安装

1. manage.py makemigrations
1. manage.py migrate
1. manage.py setup
1. manage.py createsuperuser

## 使用
1. 导入商品： `manage.py data_import 商品XLS文件.xls`
1. 清理过期商品： `manage.py delete_outdate_goods`