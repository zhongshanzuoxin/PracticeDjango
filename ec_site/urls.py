from django.urls import path
from .views import Top, SignupFunc, LoginFunc, LogoutFunc, OrderHistoryFunc
  
urlpatterns = [
    path('', Top.as_view(), name='top'),
    path('signup/', SignupFunc.as_view(), name='signup'),
    path('login/', LoginFunc.as_view(), name='login'),
    path('logout/', LogoutFunc.as_view(), name='logout'),
    path('order_history/', OrderHistoryFunc.as_view(), name='order_history'),
]