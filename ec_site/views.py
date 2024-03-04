
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View, UpdateView
from .models import Product, Order, OrderProduct, CustomUser, Payment, ShippingAddress
from allauth.account import views
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import  SignupUserForm, ShippingAddressForm
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)

        return render(request, 'profile.html', {'user_data': user_data})
    
from allauth.account.views import EmailView, PasswordResetView, PasswordResetDoneView, PasswordResetFromKeyView, PasswordResetFromKeyDoneView

class CustomEmailView(EmailView):
    template_name = 'account/email.html'

class CustomPasswordResetView(PasswordResetView):
    template_name = 'account/password_reset.html'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'

class CustomPasswordResetFromKeyView(PasswordResetFromKeyView):
    template_name = 'account/password_reset_from_key.html'

class CustomPasswordResetFromKeyDoneView(PasswordResetFromKeyDoneView):
    template_name = 'account/password_reset_from_key_done.html'
    

class NameEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['full_name']
    template_name = 'name_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    

def AddShippingAddress(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect('shipping_address_list')
    else:
        form = ShippingAddressForm()
    return render(request, 'add_shipping_address.html', {'form': form})

@login_required
def EditShippingAddress(request, id):
    shipping_address = get_object_or_404(ShippingAddress, id=id, user=request.user)
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            form.save()
            return redirect('shipping_address_list')
    else:
        form = ShippingAddressForm(instance=shipping_address)
    return render(request, 'edit_shipping_address.html', {'form': form})

@login_required
def DeleteShippingAddress(request, id):
    shipping_address = get_object_or_404(ShippingAddress, id=id, user=request.user)
    if request.method == 'POST':
        shipping_address.delete()
        return redirect('shipping_address_list')
    return render(request, 'shipping_address_list.html')

class ShippingAddressList(LoginRequiredMixin, ListView):
    model = ShippingAddress
    template_name = 'shipping_address_list.html'
    context_object_name = 'shipping_addresses'

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user)


class SignupFunc(views.SignupView):
    form_class = SignupUserForm
    success_url = reverse_lazy('top') 
    template_name = 'signup.html' 
    

class LoginFunc(views.LoginView):
    template_name = 'login.html'
    authentication_form = None

class LogoutFunc(views.LogoutView):
    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('login')


class ProductListFunc(ListView):
    model = Product
    template_name = 'products/product_list.html'

class ProductDetailFunc(DetailView):
    def get(self, request, *args, **kwargs):
        product_data = Product.objects.get(slug=self.kwargs['slug'])
        return render(request, 'products/product_detail.html', {'product_data': product_data})


def AddProductToCart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    quantity = int(request.POST.get('quantity', 1))
    
    if request.user.is_authenticated:
        order_product, created = OrderProduct.objects.get_or_create(
            product=product,
            user=request.user,
            ordered=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.products.filter(product__slug=product.slug).exists():
                order_product.quantity += quantity
                order_product.save()
                messages.info(request, f'カート内の {product.product_name} の数量が {order_product.quantity} に更新されました。')
            else:
                order_product.quantity = quantity
                order_product.save()
                order.products.add(order_product)
                messages.success(request, f'{product.product_name} をカートに追加しました。')
        else:
            order = Order.objects.create(user=request.user, ordered_date=timezone.now())
            order_product.quantity = quantity
            order_product.save()
            order.products.add(order_product)
            messages.success(request, f'{product.product_name} をカートに追加しました。')
    else:
        cart = request.session.get('cart', {})
        item_id = str(product.id)
        if item_id in cart:
            cart[item_id]['quantity'] += quantity
            messages.info(request, f'カート内の {product.product_name} の数量が {cart[item_id]["quantity"]} に更新されました。')
        else:
            image_url = product.images.first().image.url if product.images.exists() else "https://via.placeholder.com/150"
            cart[item_id] = {'quantity': quantity, 'slug': product.slug, 'price': str(product.price), 'image_url': image_url}
            messages.success(request, f'{product.product_name} をカートに追加しました。')
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('order')


def AddProductToOrder(request, product, quantity):
    order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += quantity
            order_product.save()
        else:
            order_product.quantity = quantity
            order_product.save()
            order.products.add(order_product)
    else:
        order = Order.objects.create(user=request.user, ordered_date=timezone.now())
        order_product.quantity = quantity
        order_product.save()
        order.products.add(order_product)


def ReductionProduct(request, slug):
    if request.user.is_authenticated:
        # ログインしている場合の処理
        product = get_object_or_404(Product, slug=slug)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.products.filter(product__slug=product.slug).exists():
                order_product = OrderProduct.objects.filter(
                    product=product,
                    user=request.user,
                    ordered=False
                )[0]
                if order_product.quantity > 1:
                    order_product.quantity -= 1
                    order_product.save()
                else:
                    order.products.remove(order_product)
                messages.info(request, "この商品の数量が更新されました。")
            else:
                messages.info(request, "この商品はあなたのカートにありません。")
        else:
            messages.info(request, "あなたにはアクティブな注文がありません。")
    else:
        # ログインしていない場合の処理
        cart = request.session.get('cart', {})
        # slugを使ってProductを取得する処理を追加
        product = get_object_or_404(Product, slug=slug)
        item_id = str(product.id)  # ここでproduct変数を使用
        if item_id in cart:
            if cart[item_id]['quantity'] > 1:
                cart[item_id]['quantity'] -= 1
            else:
                del cart[item_id]
            request.session['cart'] = cart
            messages.info(request, "この商品の数量が更新されました。")
        else:
            messages.info(request, "この商品はカートにありません。")
    return redirect('order')

def RemoveProduct(request, slug):
    if request.user.is_authenticated:
        # ログインしている場合の処理
        product = get_object_or_404(Product, slug=slug)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.products.filter(product__slug=product.slug).exists():
                order_product = OrderProduct.objects.filter(
                    product=product,
                    user=request.user,
                    ordered=False
                )[0]
                order.products.remove(order_product)
                order_product.delete()
                messages.warning(request, "この商品があなたのカートから削除されました。")
            else:
                messages.info(request, "この商品はあなたのカートにありません。")
        else:
            messages.info(request, "あなたにはアクティブな注文がありません。")
    else:
        # ログインしていない場合の処理
        cart = request.session.get('cart', {})
        # slugを使ってProductを取得する処理を追加
        product = get_object_or_404(Product, slug=slug)
        item_id = str(product.id)  # ここでproduct変数を使用
        if item_id in cart:
            del cart[item_id]
            request.session['cart'] = cart
            messages.warning(request, "この商品がカートから削除されました。")
        else:
            messages.info(request, "この商品はカートにありません。")
    return redirect('order')


class OrderView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                order = Order.objects.get(user=request.user, ordered=False)
                total = order.get_total()
                # 商品の個数の合計を計算
                product_count = sum([item.quantity for item in order.products.all()])
                context = {
                    'order': order,
                    'total': total,
                    'product_count': product_count
                }
                return render(request, 'order.html', context)
            except ObjectDoesNotExist:
                return render(request, 'order.html', {'message': 'カートに商品がありません。'})
        else:
            # ログインしていない場合の処理
            cart = request.session.get('cart', {})
            products = []
            total = 0
            product_count = 0  # 商品の個数の合計を初期化
            for item_id, item_data in cart.items():
                product = get_object_or_404(Product, id=item_id)
                total += product.price * item_data['quantity']
                product_count += item_data['quantity']  # 商品の個数の合計を加算
                products.append({
                    'product': product,
                    'quantity': item_data['quantity'],
                    'total_price': product.price * item_data['quantity']
                })
            context = {
                'products': products,
                'total': total,
                'is_authenticated': False,
                'product_count': product_count 
            }
            return render(request, 'order.html', context)
        

class PaymentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        user_data = CustomUser.objects.get(id=request.user.id)
        # 配送料の計算
        if order.get_total() > 5000:
            shipping_cost = 0
        else:
            shipping_cost = 1250
        context = {
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'order': order,
            'user_data': user_data,
            'shipping_cost': shipping_cost, 
        }
        return render(request, 'payment.html', context)
    
    
    def post(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        token = request.POST.get('stripeToken')
        if not token:
            return HttpResponse('Invalid token', status=400)
        order_products = order.products.all()
        amount = order.get_total()
        if amount > 5000:
            shipping_cost = 0
        else:
            shipping_cost = 1250
        total_amount = amount + shipping_cost
        product_list = []
        for order_product in order_products:
            product_list.append(str(order_product.product) + ':' + str(order_product.quantity))
        description = ' '.join(product_list)

        try:
            charge = stripe.Charge.create(
                amount=total_amount,
                currency='jpy',
                description=description,
                source=token,
            )
        except stripe.error.StripeError as e:
            return HttpResponse(str(e), status=400)

        payment = Payment(user=request.user)
        payment.stripe_charge_id = charge['id']
        payment.amount = total_amount
        payment.save()

        order_products.update(ordered=True)
        for product in order_products:
            product.product.stock -= product.quantity  # 在庫を減らす
            product.product.save()  # Productモデルの更新を保存
            product.save()

        order.ordered = True
        order.payment = payment
        order.save()
        return redirect('thanks')
    
class ThanksView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'thanks.html')



def Search(request):
    query = request.GET.get('q')
    products = None
    if query:
        products = Product.objects.filter(product_name__icontains=query)
    return render(request, 'search_results.html', {'products': products})


def SearchSuggest(request):
    query = request.GET.get('q', '')
    suggestions = list(Product.objects.filter(product_name__icontains=query).values('product_name', 'slug')[:5])
    return JsonResponse(suggestions, safe=False)