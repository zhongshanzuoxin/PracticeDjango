from django.urls import path
from .views import Top
  
urlpatterns = [
    path('', Top.as_view(), name='top'),
]