from django.shortcuts import get_object_or_404
from django.shortcuts import render

from CanteenWebsite.utils.functions import get_goods_list
from CanteenWebsite.utils.functions import setting_get
from CanteenWebsite.models import Category, Goods


def index(request):
    index_page = None
    goods_list = None
    if setting_get("index_page", "blank") != "blank":
        index_page = True
        goods_list_all = Goods.objects.all()
        goods_list = get_goods_list(goods_list_all, request)
    context = {
        "index_page": index_page,
        "goods_list": goods_list
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

    context = {
        "current_category": current_category,
        "goods_list": goods_list
    }
    return render(request=request,
                  template_name="CanteenWebsite/category.html",
                  context=context
                  )


def search(request, key_word):
    goods_list_all = Goods.objects.filter(name__contains=key_word)
    goods_list = get_goods_list(goods_list_all, request)
    context = {
        "keyword": key_word,
        "goods_list": goods_list
    }
    return render(request=request,
                  template_name="CanteenWebsite/search.html",
                  context=context
                  )
