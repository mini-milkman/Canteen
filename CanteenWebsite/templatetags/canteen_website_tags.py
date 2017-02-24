from django import template
from CanteenWebsite.models import Category

register = template.Library()


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
