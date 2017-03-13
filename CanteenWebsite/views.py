# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from CanteenWebsite.models import Category, Goods
from CanteenWebsite.utils.functions import get_goods_list
from CanteenWebsite.utils.functions import setting_get, setting_get_json


def index(request):
    index_page = setting_get("index_page", "blank")
    goods_list = None
    context_extend = dict(
        list_style_template="CanteenWebsite/inclusions/show_list_styles/{}.html".format(
            setting_get("goods_list_style")
        ),
        use_goods_detail_view=setting_get_json("use_goods_detail_view")
    )

    if index_page != "blank":
        goods_list_all = Goods.objects.all()
        goods_list = get_goods_list(goods_list_all, request)

    context = {
        "index_page": index_page,
        "goods_list": goods_list
    }
    context.update(context_extend)
    return render(request=request,
                  template_name="CanteenWebsite/index.html",
                  context=context
                  )


def category(request, category_id):
    context_extend = dict(
        list_style_template="CanteenWebsite/inclusions/show_list_styles/{}.html".format(
            setting_get("goods_list_style")
        ),
        use_goods_detail_view=setting_get_json("use_goods_detail_view")
    )

    # 当前分类
    current_category = get_object_or_404(Category, pk=category_id)

    # 获取商品
    goods_list_all = current_category.goods_set.all()
    goods_list = get_goods_list(goods_list_all, request)

    context = {
        "current_category": current_category,
        "goods_list": goods_list
    }
    context.update(context_extend)
    return render(request=request,
                  template_name="CanteenWebsite/category.html",
                  context=context
                  )


def detail(request, goods_id):
    # 当前商品
    current_goods = get_object_or_404(Goods, pk=goods_id)

    context = {
        "current_goods": current_goods
    }
    return render(request=request,
                  template_name="CanteenWebsite/detail.html",
                  context=context
                  )


def search(request, key_word):
    context_extend = dict(
        list_style_template="CanteenWebsite/inclusions/show_list_styles/{}.html".format(
            setting_get("goods_list_style")
        ),
        use_goods_detail_view=setting_get_json("use_goods_detail_view")
    )
    goods_list_all = Goods.objects.filter(name__contains=key_word)
    goods_list = get_goods_list(goods_list_all, request)
    context = {
        "keyword": key_word,
        "goods_list": goods_list
    }
    context.update(context_extend)
    return render(request=request,
                  template_name="CanteenWebsite/search.html",
                  context=context
                  )
