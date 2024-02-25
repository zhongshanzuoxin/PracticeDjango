from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Order, Product, OrderProduct, CustomUser
from allauth.account import views
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import  SignupUserForm, ProfileForm
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class Top(TemplateView):
    template_name = 'top.html'

class ProfileView(View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)

        return render(request, 'profile.html', {'user_data': user_data})
    
class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            initial={
                'full_name': user_data.full_name,
            }
        )

        return render(request, 'profile_edit.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            user_data = CustomUser.objects.get(id=request.user.id)
            user_data.full_name = form.cleaned_data['full_name']
            user_data.save()
            return redirect('profile')
        
        return render(request, 'profile_edit.html', {'form': form})

class SignupFunc(views.SignupView):
    form_class = SignupUserForm
    success_url = reverse_lazy('top') 
    template_name = 'signup.html' 

class LoginFunc(LoginView):
    template_name = 'login.html'
    authentication_form = None

class LogoutFunc(LogoutView):
    next_page = reverse_lazy('top')

class ProductListFunc(ListView):
    model = Product
    template_name = 'products/product_list.html'

class ProductDetailFunc(DetailView):
    def get(self, request, *args, **kwargs):
        product_data = Product.objects.get(slug=self.kwargs['slug'])
        return render(request, 'products/product_detail.html', {'product_data': product_data})

@login_required
def AddProduct(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order = Order.objects.filter(user=request.user, ordered=False)

    if order.exists():
        order = order[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
        else:
            order.products.add(order_product)
    else:
        order = Order.objects.create(user=request.user, ordered_date=timezone.now())
        order.products.add(order_product)
    
    return redirect('order')

from django.shortcuts import get_object_or_404, redirect
from .models import Product, Order, OrderProduct
from django.contrib import messages

def ReductionProduct(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # 商品が注文に存在するか確認
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
    return redirect('order')

def RemoveProduct(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # 商品が注文に存在するか確認
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
    return redirect('order')

class OrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            context = {
                'order': order
            }
            return render(request, 'order.html', context)
        except ObjectDoesNotExist:
            return render(request, 'order.html')
        