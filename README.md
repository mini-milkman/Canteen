# Canteen

一个__懒癌版__淘宝客系统

## 系统依赖

1. Python 3
1. Python3-pip

## 安装与升级

### 安装

```bash
cd install; ./install.sh
```

### 升级

```bash
cd install; ./update.sh
```

## 控制台使用

1. 导入商品： `manage.py data_import 商品XLS文件.xls`
1. 清理过期商品： `manage.py delete_outdate_goods`

## 其他说明

1. 数据库字符集必须为 `utf8mb4-` ，否则会出现各种玄学错误
1. 建议使用 cron job 来自动清理过期商品： `10 0 * * * cd /var/www/Canteen; python3 manage.py delete_outdate_goods`
1. 如遇到 pip 错误，请 `sudo apt-get install localepurge` ，选择 `zh_CN.UTF-8` 和 `en_US.UTF-8` ，并 `sudo locale-gen zh_CN.UTF-8 en_US.UTF-8` 
