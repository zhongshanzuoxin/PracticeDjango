from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from .forms import CustomUserCreationForm
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Order
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
 

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
    template_name = 'login.html'
    next_page = reverse_lazy('login')

class OrderHistoryFunc(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order_history.html'

    def get_queryset(self):
        # ログインしているユーザーの注文のみを取得
        return Order.objects.filter(user=self.request.user).order_by('-order_id')
    
class CancelOrderView(View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Order, pk=order_id, user=request.user)

        if order.cancel_order():
            messages.success(request, "注文がキャンセルされました。")
        else:
            messages.error(request, "この注文はキャンセルできません。")

        return HttpResponseRedirect(reverse('order_detail', args=[order_id]))