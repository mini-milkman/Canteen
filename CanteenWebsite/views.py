# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from CanteenWebsite.models import Category, Goods
from CanteenWebsite.utils.functions import get_goods_list
from CanteenWebsite.utils.functions import setting_get


def index(request):
    index_page = setting_get("index_page", "blank")
    goods_list = None
    list_style_template = "CanteenWebsite/inclusions/show_list_styles/{}.html".format(
        setting_get("goods_list_style")
    )

    if index_page != "blank":
        goods_list_all = Goods.objects.all()
        goods_list = get_goods_list(goods_list_all, request)

    context = {
        "index_page": index_page,
        "goods_list": goods_list,
        "list_style_template": list_style_template
    }
    return render(request=request,
                  template_name="CanteenWebsite/index.html",
                  context=context
                  )


def category(request, category_id):
    # 当前分类
    current_category = get_object_or_404(Category, pk=category_id)

    # 获取商品
    goods_list_all = current_category.goods_set.all()
    goods_list = get_goods_list(goods_list_all, request)

    # 显示样式
    list_style_template = "CanteenWebsite/inclusions/show_list_styles/{}.html".format(
        setting_get("goods_list_style")
    )

    context = {
        "current_category": current_category,
        "goods_list": goods_list,
        "list_style_template": list_style_template
    }
    return render(request=request,
                  template_name="CanteenWebsite/category.html",
                  context=context
                  )


def search(request, key_word):
    goods_list_all = Goods.objects.filter(name__contains=key_word)
    goods_list = get_goods_list(goods_list_all, request)
    list_style_template = "CanteenWebsite/inclusions/show_list_styles/{}.html".format(
        setting_get("goods_list_style")
    )
    context = {
        "keyword": key_word,
        "goods_list": goods_list,
        "list_style_template": list_style_template
    }
    return render(request=request,
                  template_name="CanteenWebsite/search.html",
                  context=context
                  )
