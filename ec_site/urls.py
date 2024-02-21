from django.urls import path
from .views import Top, SignupFunc, LoginFunc
  
urlpatterns = [
    path('', Top.as_view(), name='top'),
    path('signup/', SignupFunc.as_view(), name='signup'),
    path('login/', LoginFunc.as_view(), name='login'),
    path('logout/', LoginFunc.as_view(), name='logout'),
]