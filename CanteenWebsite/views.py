from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from CanteenWebsite.functions.util import setting_get, setting_get_json


def index(request):
    context = {}
    return render(request=request,
                  template_name="CanteenWebsite/index.html",
                  context=context
                  )


def category(request, category_id):
    # 当前分类
    current_category = get_object_or_404(Category, pk=category_id)

    # 分类中的商品
    goods_list_all = current_category.goods_set.all()

    # 每页显示多少商品
    goods_per_page = max(int(setting_get_json("goods_per_page")), 1)

    # 如何排序
    sort_strategy = setting_get_json("goods_sort_strategy")
    if sort_strategy != "None":
        goods_list_all = goods_list_all.extra(order_by=[sort_strategy])

    # 分页
    paginator = Paginator(goods_list_all, goods_per_page)
    page = request.GET.get('page')
    try:
        goods_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        goods_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        goods_list = paginator.page(paginator.num_pages)

    context = {
        "current_category": current_category,
        "goods_list": goods_list
    }
    return render(request=request,
                  template_name="CanteenWebsite/category.html",
                  context=context
                  )
