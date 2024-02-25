from django import template
from ec_site.models import Order

register = template.Library()

@register.filter
def product_count(user):
    if user.is_authenticated:
        order = Order.objects.filter(user=user, ordered=False)
        if order.exists():
            return order[0].products.count()
    return 0