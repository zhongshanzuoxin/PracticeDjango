from django.shortcuts import render
from django.views.generic.base import TemplateView
 

class Top(TemplateView):
    template_name = 'top.html'
