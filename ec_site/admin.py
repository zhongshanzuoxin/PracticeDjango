# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Order, OrderProduct, Product, ProductImage, Category
from .forms import CustomUserCreationForm, CustomUserChangeForm



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'is_active', 'is_staff']  # 管理画面で表示するフィールド
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        # 他のフィールドセット設定...
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'username'),
        }),
    )


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'total_amount', 'order_status', 'created_at')
    list_filter = ('order_status', 'created_at')
    search_fields = ('order_id', 'user__email')
    inlines = [OrderProductInline]

    actions = ['make_shipped']

    def make_shipped(self, request, queryset):
        queryset.update(order_status='shipped')
        self.message_user(request, "選択された注文を発送完了に更新しました。")
    make_shipped.short_description = "注文ステータスを「発送完了」に変更"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description', 'category__name')
    inlines = [ProductImageInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
