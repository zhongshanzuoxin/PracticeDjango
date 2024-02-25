# Register your models here.
from django.contrib import admin
from .models import CustomUser, Order, Product, ProductImage, Category, Payment, OrderProduct

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # 新規で追加する空のフォームの数

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline,]

admin.site.register(CustomUser)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Product, ProductAdmin)  # ProductをProductAdminで登録
admin.site.register(Payment)
admin.site.register(Category)
