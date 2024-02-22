from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, View, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Order, Product, Favorite, Cart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from .forms import CustomUserCreationForm
from django.views import generic
from django.conf import settings
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
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(
            user=request.user, 
            product=product
        )
        if created:
            cart.quantity = 1  # 新規作成時の数量を設定
        else:
            cart.quantity += 1  # 既存の場合は数量を増やす
        cart.save()
        return redirect('product_detail', pk=product_id)



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
