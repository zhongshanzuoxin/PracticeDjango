from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)  # お気に入り登録した日時

    class Meta:
        unique_together = ('user', 'product')  # 同じ商品を複数回お気に入り登録できないようにする

    def __str__(self):
        return f"{self.user.email} favorite {self.product.name}"


class ShippingAddress(models.Model):
    shipping_address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.full_name}, {self.address}"


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    order_status = models.CharField(max_length=50, choices=[('pending', '発送待ち'), ('shipped', '発送完了'), ('cancelled', 'キャンセル済み')], default='pending')
    stripe_payment_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=50, choices=[('pending', '処理中'), ('completed', '完了'), ('failed', '失敗')], default='pending')
    is_confirmed = models.BooleanField(default=False)  # 注文が確定したかどうかを示すフィールド
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.email}"

    def save(self, *args, **kwargs):
        # 注文が新しく確定された場合にのみ在庫を更新
        if self.is_confirmed and not Order.objects.filter(pk=self.pk, is_confirmed=True).exists():
            self.update_stock()
        super().save(*args, **kwargs)

    def update_stock(self):
        # 注文に関連するすべての商品の在庫を更新
        order_products = self.orderproduct_set.all()
        for op in order_products:
            op.product.stock -= op.quantity
            op.product.save()

    def confirm_order(self):
        # 在庫確認と更新処理
        if self.check_stock():
            self.update_stock()
            self.is_confirmed = True
            self.save()
            return True
        else:
            return False

    def check_stock(self):
        # 注文に関連するすべての商品の在庫をチェック
        order_products = self.orderproduct_set.all()
        for op in order_products:
            if op.product.stock < op.quantity:
                # 在庫不足
                return False
        return True

    def update_stock(self):
        # 注文に関連するすべての商品の在庫を更新
        order_products = self.orderproduct_set.all()
        for op in order_products:
            op.product.stock -= op.quantity
            op.product.save()

    def cancel_order(self):
        # 注文が「発送待ち」状態の場合のみキャンセルを許可
        if self.order_status == 'pending':
            self.order_status = 'cancelled'
            self.save()
            self.refund_stock()
            return True
        # それ以外の場合はキャンセル不可
        return False

    def refund_stock(self):
        # 注文に関連する商品の在庫を元に戻す
        for order_product in self.orderproduct_set.all():
            product = order_product.product
            product.stock += order_product.quantity
            product.save()



class OrderProduct(models.Model):
    order_product_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Cart {self.cart_id} for {self.user.email}"
