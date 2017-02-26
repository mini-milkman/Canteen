import re
import json
from CanteenWebsite.models import Setting

DISCOUNT_TYPE = [
    {
        "reg": re.compile(r"满([\d.]+)元减([\d.]+)元"),
        "condition": 0,
        "discount": 1,
    }, {
        "reg": re.compile(r"([\d.]+)元无条件券"),
        "condition": None,
        "discount": 0,
    }
]


def parse_discount(coupon_str):
    """
    计算优惠券信息
    """
    condition = 0
    discount = 0
    for discounter in DISCOUNT_TYPE:
        result = discounter["reg"].match(coupon_str)
        if result:
            groups = result.groups()
            if discounter["condition"] is not None:
                condition = float(groups[discounter["condition"]])
            if discounter["discount"] is not None:
                discount = float(groups[discounter["discount"]])
            break
    return condition, discount


def calculate_real_price(price, coupon_str):
    """
    计算商品真实价格
    """
    condition, discount = parse_discount(coupon_str)
    if price >= condition:
        price -= discount
    return max(price, 0)


def value_set_select(key, value_set, default, wrapper):
    v = default
    if key is not None:
        try:
            v = wrapper(value_set[key])
        except:
            pass
    return v


def setting_get(name, default=None):
    """
    获取设置
    """
    try:
        result = Setting.objects.get(name=name)
        return result.value
    except:
        return default


def setting_set(name, value=""):
    """
    写入设置
    """
    Setting.objects.update_or_create(name=name,
                                     defaults={
                                         'is_json': False,
                                         'value': value
                                     }
                                     )

    return True


def setting_get_json(name, default=None):
    """
    获取Json设置
    """
    try:
        result = Setting.objects.get(name=name)
        return json.loads(result.value)
    except:
        return default


def setting_set_json(name, value=None):
    """
    写入Json设置
    """
    try:
        json_string = json.dumps(value)
    except:
        json_string = json.dumps(None)

    Setting.objects.update_or_create(name=name,
                                     defaults={'is_json': True, 'value': json_string}
                                     )

    return True
