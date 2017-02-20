from django.contrib import admin
from .models import Category
from .models import Goods
from .models import Setting

admin.site.register(Category)
admin.site.register(Goods)
admin.site.register(Setting)
