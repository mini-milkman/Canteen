import re

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
