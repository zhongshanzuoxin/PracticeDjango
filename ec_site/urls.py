from django.urls import path
from .views import (
    Top,
    SignupFunc,
    LoginFunc,
    LogoutFunc,
    ProductListFunc,
    OrderDetailFunc,
    AddToFavoritesFunc,
    AddToCartFunc,
    OrderHistoryFunc,
    CancelOrderFunc,
    ConfirmOrderFunc,
    CreateCheckoutSessionFunc,
    PaymentSuccessFunc,
    PaymentCancelFunc,
)

urlpatterns = [
    path('', Top.as_view(), name='top'),
    path('signup/', SignupFunc.as_view(), name='signup'),
    path('login/', LoginFunc.as_view(), name='login'),
    path('logout/', LogoutFunc.as_view(), name='logout'),
    path('products/', ProductListFunc.as_view(), name='product_list'),
    path('order/<int:pk>/', OrderDetailFunc.as_view(), name='order_detail'),
    path('add_to_favorites/<int:product_id>/', AddToFavoritesFunc.as_view(), name='add_to_favorites'),
    path('add_to_cart/<int:product_id>/', AddToCartFunc.as_view(), name='add_to_cart'),
    path('order_history/', OrderHistoryFunc.as_view(), name='order_history'),
    path('cancel_order/<int:order_id>/', CancelOrderFunc.as_view(), name='cancel_order'),
    path('confirm_order/<int:order_id>/', ConfirmOrderFunc.as_view(), name='confirm_order'),
    path('create-checkout-session/', CreateCheckoutSessionFunc.as_view(), name='create_checkout_session'),
    path('success/', PaymentSuccessFunc.as_view(), name='success'),
    path('cancel/', PaymentCancelFunc.as_view(), name='cancel'),
]
