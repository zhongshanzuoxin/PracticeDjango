from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ec_site.views import (
    ProfileView, 
    AddShippingAddress, 
    EditShippingAddress, 
    DeleteShippingAddress, 
    ShippingAddressList,
    SignupFunc,
    LoginFunc,
    LogoutFunc,
    ProductListFunc,
    ProductDetailFunc,
    AddProductToCart,
    ReductionProduct,
    RemoveProduct,
    OrderView,
    PaymentView,
    ThanksView,
    Search,
    SearchSuggest,
    OrderHistory,
    OrderDetail,
    NameEditView,
    CustomEmailView,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetFromKeyView,
    CustomPasswordResetFromKeyDoneView
)

class TestUrls(SimpleTestCase):

    def test_profile_url_resolves(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func.view_class, ProfileView)

    def test_add_shipping_address_url_resolves(self):
        url = reverse('add_shipping_address')
        self.assertEquals(resolve(url).func, AddShippingAddress)

    def test_edit_shipping_address_url_resolves(self):
        url = reverse('edit_shipping_address', args=[1])
        self.assertEquals(resolve(url).func, EditShippingAddress)

    def test_delete_shipping_address_url_resolves(self):
        url = reverse('delete_shipping_address', args=[1])
        self.assertEquals(resolve(url).func, DeleteShippingAddress)

    def test_shipping_address_list_url_resolves(self):
        url = reverse('shipping_address_list')
        self.assertEquals(resolve(url).func.view_class, ShippingAddressList)

    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func.view_class, SignupFunc)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, LoginFunc)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, LogoutFunc)

    def test_product_list_url_resolves(self):
        url = reverse('product_list')
        self.assertEquals(resolve(url).func.view_class, ProductListFunc)

    def test_product_detail_url_resolves(self):
        url = reverse('product_detail', args=['some-slug'])
        self.assertEquals(resolve(url).func.view_class, ProductDetailFunc)

    def test_add_product_to_cart_url_resolves(self):
        url = reverse('add_product', args=['some-slug'])
        self.assertEquals(resolve(url).func, AddProductToCart)

    def test_reduction_product_url_resolves(self):
        url = reverse('reduction_product', kwargs={'slug': 'some-slug'})
        self.assertEquals(resolve(url).func, ReductionProduct)

    def test_remove_product_url_resolves(self):
        url = reverse('remove_product', kwargs={'slug': 'some-slug'})
        self.assertEquals(resolve(url).func, RemoveProduct)

    def test_order_url_resolves(self):
        url = reverse('order')
        self.assertEquals(resolve(url).func.view_class, OrderView)

    def test_payment_url_resolves(self):
        url = reverse('payment')
        self.assertEquals(resolve(url).func.view_class, PaymentView)

    def test_thanks_url_resolves(self):
        url = reverse('thanks')
        self.assertEquals(resolve(url).func.view_class, ThanksView)

    def test_search_url_resolves(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func, Search)

    def test_search_suggest_url_resolves(self):
        url = reverse('search_suggest')
        self.assertEquals(resolve(url).func, SearchSuggest)

    def test_order_history_url_resolves(self):
        url = reverse('order_history')
        self.assertEquals(resolve(url).func, OrderHistory)

    def test_order_detail_url_resolves(self):
        url = reverse('order_detail', args=[1])
        self.assertEquals(resolve(url).func, OrderDetail)

    def test_name_edit_url_resolves(self):
        url = reverse('name_edit')
        self.assertEquals(resolve(url).func.view_class, NameEditView)

    def test_reset_email_url_resolves(self):
        url = reverse('account_email')
        self.assertEquals(resolve(url).func.view_class, CustomEmailView)

    def test_reset_password_url_resolves(self):
        url = reverse('account_reset_password')
        self.assertEquals(resolve(url).func.view_class, CustomPasswordResetView)

    def test_password_reset_done_url_resolves(self):
        url = reverse('password_reset_done')
        self.assertEquals(resolve(url).func.view_class, CustomPasswordResetDoneView)

    def test_password_reset_from_key_url_resolves(self):
        url = reverse('account_reset_password_from_key', args=['uidb64', 'token'])
        self.assertEquals(resolve(url).func.view_class, CustomPasswordResetFromKeyView)

    def test_password_reset_from_key_done_url_resolves(self):
        url = reverse('account_reset_password_from_key_done')
        self.assertEquals(resolve(url).func.view_class, CustomPasswordResetFromKeyDoneView)