from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Category

from CanteenWebsite.functions.util import get_goods_list


def index(request):
    context = {}
    return render(request=request,
                  template_name="CanteenWebsite/index.html",
                  context=context
                  )


def category(request, category_id):
    # 当前分类
    current_category = get_object_or_404(Category, pk=category_id)

    # 获取商品
    goods_list = get_goods_list(current_category, request)

    context = {
        "current_category": current_category,
        "goods_list": goods_list
    }
    return render(request=request,
                  template_name="CanteenWebsite/category.html",
                  context=context
                  )
