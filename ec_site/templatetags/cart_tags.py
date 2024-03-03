from django import template
from ec_site.models import Order

register = template.Library()

@register.simple_tag(takes_context=True)
def product_count(context):
    request = context['request']
    if request.user.is_authenticated:
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs.first()
            return sum(item.quantity for item in order.products.all())
    else:
        cart = request.session.get('cart', {})
        return sum(item['quantity'] for item in cart.values())
    return 0