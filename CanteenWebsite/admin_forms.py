from django import forms


class OptionsForm(forms.Form):
    site_name = forms.CharField(
        label='站点名称',
        max_length=100
    )
    site_slogan = forms.CharField(
        label="站点副标题",
        max_length=100
    )
    index_page = forms.ChoiceField(
        label="首页显示内容",
        choices=(
            ('random', '随机'),
            ('blank', '空白'),
        )
    )
    goods_per_page = forms.IntegerField(
        label="每页显示商品数量",
        min_value=1
    )
    goods_style = forms.ChoiceField(
        label="商品显示样式",
        choices=(
            ('style_1', '上图下介绍'),
            ('style_2', '左图右介绍'),
        )
    )
    goods_sort_strategy = forms.ChoiceField(
        label="商品排序方式",
        choices=(
            ('None', '随机/不排序'),
            ('id', '商品ID'),
            ('commission', '佣金 从低到高'),
            ('-commission', '佣金 从高到低'),
            ('commission_rate', '佣金比率 从低到高'),
            ('-commission_rate', '佣金比率 从高到低'),
            ('coupon_time_end', '优惠券结束时间 从早到晚'),
            ('-coupon_time_end', '优惠券结束时间 从晚到早'),
            ('price_real', '商品实际购买价格 从低到高'),
            ('-price_real', '商品实际购买价格 从高到低'),
        )
    )


class DataImportOptionForm(forms.Form):
    file = forms.FileField(
        label="选择文件"
    )
    column_index = forms.CharField(
        label="文件导入结构",
        max_length=1000
    )
    delete_before_import = forms.CharField(
        label="导入前清空",
        max_length=100
    )
    use_blacklist_category = forms.BooleanField(
        label="使用分类黑名单"
    )
    blacklist_category = forms.CharField(
        label="分类黑名单",
        max_length=100
    )
    use_whitelist_category = forms.BooleanField(
        label="使用分类白名单"
    )
    whitelist_category = forms.CharField(
        label="分类白名单",
        max_length=100
    )
    use_blacklist_goods = forms.BooleanField(
        label="使用商品黑名单"
    )
    blacklist_goods = forms.CharField(
        label="商品黑名单",
        max_length=100
    )
    use_whitelist_goods = forms.BooleanField(
        label="使用商品白名单"
    )
    whitelist_goods = forms.CharField(
        label="商品白名单",
        max_length=100
    )


class DataImportForm(forms.Form):
    file = forms.FileField(
        label="选择文件"
    )
