# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'is_active', 'is_staff']  # 管理画面で表示するフィールド
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('任意の追加フィールド',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
            (None, {'fields': ('任意の追加フィールド',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
