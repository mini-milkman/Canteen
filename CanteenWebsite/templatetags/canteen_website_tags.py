from django import template
from CanteenWebsite.models import Category
from CanteenWebsite.functions.util import setting_get

register = template.Library()


@register.simple_tag
def get_setting(name):
    return setting_get(name)


@register.inclusion_tag('inclusions/sidebar_category_list.html', takes_context=True)
def sidebar_category_list(context):
    categories = Category.objects.all()
    try:
        current_category = context['current_category']
    except:
        current_category = None
    return {
        'current': current_category,
        'categories': categories,
    }
