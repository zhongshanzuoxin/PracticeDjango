from django.test import TestCase
from django.utils import timezone
from ec_site.models import CustomUser, Product, Category, Order, OrderProduct, Payment, ShippingAddress

class TestModels(TestCase):

    def setUp(self):
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
        self.order = Order.objects.create(
            user=self.user,
            ordered_date=timezone.now(),
            ordered=False
        )
        self.order_product = OrderProduct.objects.create(
            user=self.user,
            ordered=False,
            product=self.product,
            quantity=1
        )
        self.payment = Payment.objects.create(
            stripe_charge_id='testchargeid',
            user=self.user,
            amount=1000,
            card_last4='4242',
            card_brand='Visa'
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

    def test_custom_user_str(self):
        self.assertEquals(str(self.user), 'test@example.com')

    def test_category_str(self):
        self.assertEquals(str(self.category), 'TestCategory')

    def test_product_str(self):
        self.assertEquals(str(self.product), 'TestProduct')

    def test_order_str(self):
        self.assertEquals(str(self.order), f"Order {self.order.id}")

    def test_order_product_str(self):
        self.assertEquals(str(self.order_product), f"{self.order_product.product.product_name} : {self.order_product.quantity}")

    def test_payment_str(self):
        self.assertEquals(str(self.payment), f"Payment {self.payment.id}")

    def test_shipping_address_str(self):
        expected_str = (
            f"{self.shipping_address.recipient_name}, "
            f"{self.shipping_address.postal_code}, "
            f"{self.shipping_address.prefectures}, "
            f"{self.shipping_address.city}, "
            f"{self.shipping_address.address_line1}, "
            f"{self.shipping_address.address_line2}, "
            f"{self.shipping_address.phone_number}"
        )
        self.assertEquals(str(self.shipping_address), expected_str)