from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, View, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Order, Product, Favorite, Cart, ShippingAddress
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from .forms import CustomUserCreationForm, ShippingAddressForm
from django.views import generic
from django.conf import settings
from django.views.generic import FormView
from rest_framework.views import APIView
from rest_framework.response import Response
import stripe


 

class Top(TemplateView):
    template_name = 'top.html'



class SignupFunc(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('top') 
    template_name = 'signup.html' 


class LoginFunc(LoginView):
    template_name = 'login.html'
    authentication_form = None 


class LogoutFunc(LogoutView):
    next_page = reverse_lazy('top')


class ProductListFunc(ListView):
    model = Product
    template_name = 'products/product_list.html'  # 商品リストを表示するテンプレート


class ProductDetailFunc(DetailView):
    model = Product
    template_name = 'products/product_detail.html'  # 商品詳細ページのテンプレート


class OrderDetailFunc(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'  # 注文詳細を表示するテンプレート

    def get_queryset(self):
        # ログインしているユーザーの注文のみを取得
        return Order.objects.filter(user=self.request.user)



class AddToFavoritesFunc(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        Favorite.objects.get_or_create(user=request.user, product=product)
        return redirect('product_detail', pk=product_id)


class AddToCartFunc(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        quantity = request.POST.get('quantity', 1)  # フォームから送信された数量を取得
        product = get_object_or_404(Product, product_id=product_id)
        cart, created = Cart.objects.get_or_create(
            user=request.user, 
            product=product,
            defaults={'quantity': 0},  # 新規作成時は数量を0に設定し、後で更新
        )
        if created:
            cart.quantity = quantity  # 新規作成時の数量を設定
        else:
            cart.quantity += int(quantity)  # 既存の場合は数量を増やす
        cart.save()
        return redirect('cart_view')  # カートページにリダイレクト

class CartFunc(LoginRequiredMixin, View):
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        context = {
            'cart_items': cart_items,
            'total_price': total_price
        }
        return render(request, self.template_name, context)
    

class UpdateCartFunc(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        quantity = request.POST.get('quantity', 1)
        cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
        cart_item.quantity = int(quantity)
        cart_item.save()
        return redirect('cart_view')


class RemoveFromCartFunc(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        Cart.objects.filter(user=request.user, product_id=product_id).delete()
        return redirect('cart_view')


class OrderHistoryFunc(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order_history.html'

    def get_queryset(self):
        # ログインしているユーザーの注文のみを取得し、created_atフィールドに基づいて降順にソート
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    
class CancelOrderFunc(View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Order, pk=order_id, user=request.user)

        if order.cancel_order():
            messages.success(request, "注文がキャンセルされました。")
        else:
            messages.error(request, "この注文はキャンセルできません。")

        return HttpResponseRedirect(reverse('order_detail', args=[order_id]))
    

class ConfirmOrderFunc(View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Order, pk=order_id, user=request.user)  # ユーザーによるフィルタを追加
        if order.confirm_order():
            messages.success(request, "注文が確認されました。")
        else:
            messages.error(request, "在庫不足などの理由で注文を確認できませんでした。")
        return HttpResponseRedirect(reverse('order_detail', args=[order_id]))


class PaymentMethodView(LoginRequiredMixin, FormView):
    template_name = 'payment_method.html'
    form_class = ShippingAddressForm
    success_url = reverse_lazy('order_confirmation')  # 注文確認画面のURLに適宜変更してください

    def form_valid(self, form):
        # ここで配送先情報を保存し、セッションに支払い情報を保存する処理を実装します。
        address = form.save(commit=False)
        address.user = self.request.user
        address.save()
        # 例えば、支払い方法をセッションに保存する
        self.request.session['payment_method'] = 'credit_card'  # 支払い方法の例
        return super().form_valid(form)

class OrderConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = 'order_confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items'] = Cart.objects.filter(user=self.request.user)
        context['shipping_address'] = ShippingAddress.objects.filter(user=self.request.user).last()  # 最新の配送先住所を取得
        context['payment_method'] = self.request.session.get('payment_method', '未選択')
        return context



stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionFunc(View):
    def post(self, request, *args, **kwargs):
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'jpy',
                        'product_data': {
                            'name': '商品名',
                        },
                        'unit_amount': 1000,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success')),
                cancel_url=request.build_absolute_uri(reverse('cancel')),
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return str(e)


class PaymentSuccessFunc(TemplateView):
    template_name = 'success.html'

class PaymentCancelFunc(TemplateView):
    template_name = 'cancel.html'

