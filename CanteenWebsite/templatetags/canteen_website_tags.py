from django import template
from CanteenWebsite.models import Category
from CanteenWebsite.functions.util import setting_get

register = template.Library()


@register.simple_tag
def get_setting(name, default=None):
    return setting_get(name, default)


@register.inclusion_tag('CanteenWebsite/inclusions/sidebar_category_list.html', takes_context=True)
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


@register.inclusion_tag('CanteenWebsite/inclusions/show_pagination.html')
def show_pagination(page):
    pagination = page.paginator
    page_range = list()

    if pagination.num_pages <= 10:
        page_range = pagination.page_range
    else:
        ON_EACH_SIDE = 2
        ON_ENDS = 2
        DOT = '...'
        if page.number > (ON_EACH_SIDE + ON_ENDS):
            page_range.extend(range(1, ON_ENDS))
            page_range.append(DOT)
            page_range.extend(range(page.number - ON_EACH_SIDE, page.number + 1))
        else:
            page_range.extend(range(1, page.number + 1))
        if page.number < (pagination.num_pages - ON_EACH_SIDE - ON_ENDS - 1):
            page_range.extend(range(page.number + 1, page.number + ON_EACH_SIDE + 1))
            page_range.append(DOT)
            page_range.extend(range(pagination.num_pages - ON_ENDS, pagination.num_pages + 1))
        else:
            page_range.extend(range(page.number + 1, pagination.num_pages + 1))
    return {
        'page': page,
        'pages': page_range
    }
