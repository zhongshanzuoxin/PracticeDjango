from django.test import TestCase, Client
from django.urls import reverse
from ec_site.models import CustomUser, Product, Category, ShippingAddress

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='test@example.com', password='password123')
        self.category = Category.objects.create(name='TestCategory')
        self.product = Product.objects.create(
            category=self.category,
            product_name='TestProduct',
            description='Test Description',
            slug='test-product',
            price=1000,
            stock=10
        )
        self.shipping_address = ShippingAddress.objects.create(
            user=self.user,
            recipient_name='Test User',
            postal_code='1234567',
            prefectures='Tokyo',
            city='Shibuya',
            address_line1='Test Address 1',
            address_line2='Test Address 2',
            phone_number='08012345678'
        )

    def test_profile_view_GET(self):
        self.client.login(email='test@example.com', password='password123')
        response = self.client.get(reverse('profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_add_shipping_address_GET(self):
        self.client.login(email='test@example.com', password='password123')
        response = self.client.get(reverse('add_shipping_address'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_shipping_address.html')

    def test_edit_shipping_address_GET(self):
        self.client.login(email='test@example.com', password='password123')
        response = self.client.get(reverse('edit_shipping_address', args=[self.shipping_address.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_shipping_address.html')

    def test_delete_shipping_address_POST(self):
        self.client.login(email='test@example.com', password='password123')
        response = self.client.post(reverse('delete_shipping_address', args=[self.shipping_address.id]))
        self.assertRedirects(response, reverse('shipping_address_list'))

    def test_shipping_address_list_GET(self):
        self.client.login(email='test@example.com', password='password123')
        response = self.client.get(reverse('shipping_address_list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'shipping_address_list.html')

    def test_product_list_GET(self):
        response = self.client.get(reverse('product_list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')

    def test_product_detail_GET(self):
        response = self.client.get(reverse('product_detail', args=[self.product.slug]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_order_view_GET_not_logged_in(self):
        response = self.client.get(reverse('order'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'order.html')

    def test_order_view_GET_logged_in(self):
        self.client.login(email='test@example.com', password='password123')
        response = self.client.get(reverse('order'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'order.html')