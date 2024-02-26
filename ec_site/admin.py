# Register your models here.
from django.contrib import admin
from .models import CustomUser, ShippingAddress, Order, Product, ProductImage, Category, Payment, OrderProduct

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # 新規で追加する空のフォームの数

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline,]

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'postal_code', 'prefectures', 'city', 'address_line1', 'address_line2', 'phone_number')

class ShippingAddressInline(admin.TabularInline):
    model = ShippingAddress
    extra = 1  # 新規で追加する空のフォームの数

class CustomUserAdmin(admin.ModelAdmin):
    inlines = [ShippingAddressInline,]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Product, ProductAdmin)  # ProductをProductAdminで登録
admin.site.register(Payment)
admin.site.register(Category)
