from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Category


def index(request):
    context = {}
    return render(request=request,
                  template_name="index.html",
                  context=context
                  )


def category(request, category_id):
    category_query = get_object_or_404(Category, pk=category_id)
    context = {
        "category": category_query
    }
    return render(request=request,
                  template_name="category.html",
                  context=context
                  )
