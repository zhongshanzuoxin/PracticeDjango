from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    """与えられた値と引数を掛け合わせるカスタムテンプレートフィルター"""
    return value * arg
