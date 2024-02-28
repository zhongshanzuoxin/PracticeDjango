from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    Top,
    SignupFunc,
    LoginFunc,
    LogoutFunc,
    ProfileView,
    ProfileEditView,
    AddShippingAddress,
    ShippingAddressList,
    ProductListFunc,
    ProductDetailFunc,
    AddProduct,
    ReductionProduct,
    RemoveProduct,
    OrderView,
    PaymentView,
    ThanksView,
)

urlpatterns = [
    path('', Top.as_view(), name='top'),
    path('accounts/signup/', SignupFunc.as_view(), name='signup'),
    path('accounts/login/', LoginFunc.as_view(), name='login'),
    path('logout/', LogoutFunc.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('add_shipping_address/', AddShippingAddress, name='add_shipping_address'),
    path('shipping_address_list/', ShippingAddressList.as_view(), name='shipping_address_list'),
    path('products/', ProductListFunc.as_view(), name='product_list'),
    path('product/<slug>/', ProductDetailFunc.as_view(), name='product_detail'),
    path('add_product/<slug>', AddProduct, name='add_product'),
    path('reduce/<slug:slug>/', ReductionProduct, name='reduction_product'),
    path('remove/<slug:slug>/', RemoveProduct, name='remove_product'),
    path('order/', OrderView.as_view(), name='order'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('thanks/', ThanksView.as_view(), name='thanks'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
