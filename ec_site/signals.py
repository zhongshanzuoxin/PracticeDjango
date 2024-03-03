from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Product, OrderProduct, Order
from django.shortcuts import get_object_or_404
from django.utils import timezone

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    cart = request.session.get('cart', {})
    if cart:
        order_qs = Order.objects.filter(user=user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
        else:
            order = Order.objects.create(user=user, ordered_date=timezone.now())
        
        for item_id, item_data in cart.items():
            product = get_object_or_404(Product, id=item_id)
            order_product, created = OrderProduct.objects.get_or_create(
                product=product,
                user=user,
                ordered=False
            )
            if created:
                order_product.quantity = item_data['quantity']
            else:
                order_product.quantity += item_data['quantity']
            order_product.save()
            order.products.add(order_product)
        
        del request.session['cart']
        request.session.modified = True