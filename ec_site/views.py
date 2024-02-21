from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
 

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

