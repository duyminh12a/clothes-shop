from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'points_balance', 'referral_code', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'phone', 'referral_code')
    fieldsets = UserAdmin.fieldsets + (
        ('Thông tin Nếp Club & Bổ sung', {'fields': ('phone', 'avatar', 'referral_code', 'referred_by', 'points_balance', 'language_pref')}),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'city', 'district', 'is_default')
    list_filter = ('city', 'is_default')
    search_fields = ('user__username', 'full_name', 'phone', 'street_address')
