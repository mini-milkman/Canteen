# Canteen

一个__懒人版__淘宝客系统

## 系统依赖

1. Python 3
1. Python3-pip

## 安装

```bash
cd install
./install.sh
```

## 使用

1. 导入商品： `manage.py data_import 商品XLS文件.xls`
1. 清理过期商品： `manage.py delete_outdate_goods`

## 其他说明

1. 建议使用 cron job 来自动清理过期商品： `10 0 * * * cd /var/www/Canteen; python3 manage.py delete_outdate_goods`

