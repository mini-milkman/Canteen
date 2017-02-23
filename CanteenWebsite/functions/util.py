import re
import json
from CanteenWebsite.models import Setting

DISCOUNT_TYPE = {
    "conditinal": {
        "reg": re.compile(r"满([\d.]+)元减([\d.]+)元"),
        "condition": 0,
        "discount": 1,
    },
    "unconditinal": {
        "reg": re.compile(r"([\d.]+)元无条件券"),
        "condition": None,
        "discount": 0,
    }
}


def parse_discount(coupon_str):
    condition = 0
    discount = 0
    for _, discounter in DISCOUNT_TYPE.items():
        result = discounter["reg"].match(coupon_str)
        print(discounter["reg"])
        if result:
            groups = result.groups()
            if discounter["condition"] is not None:
                condition = float(groups[discounter["condition"]])
            if discounter["discount"] is not None:
                discount = float(groups[discounter["discount"]])
            break
    return condition, discount


def calculate_real_price(price, coupon_str):
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


def setting_get(name, default=None, create=False):
    """
    获取设置
    :param name: name
    :param default: name不存在时的默认值
    :return: value 或 default
    """
    try:
        result = Setting.objects.get(name=name)
        return result.value
    except:
        if create:
            setting_set(name=name, value=default)
        return default


def setting_set(name, value=""):
    """
    写入设置
    :param name: name
    :param value: value
    :return: True，表示成功
    """
    try:
        result = Setting.objects.get(name=name)
        result.value = value
        result.save()
    except:
        Setting.objects.create(name=name, value=value)

    return True


def setting_set_json(name, value=None):
    try:
        json_string = json.dumps(value)
    except:
        json_string = json.dumps(None)
    setting_set(name=name, value=json_string)
    return True


def setting_get_json(name, default=None):
    json_string = setting_get(name=name)
    try:
        return json.loads(json_string)
    except:
        return default
