from django.contrib import admin
from .models import MembershipTier, PointTransaction, Referral, Coupon

@admin.register(MembershipTier)
class MembershipTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_points', 'discount_percent', 'free_shipping_threshold', 'badge_color', 'exclusive_access')

@admin.register(PointTransaction)
class PointTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'transaction_type', 'description', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('user__username', 'description')

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referrer', 'referee', 'points_awarded', 'is_completed', 'created_at')
    list_filter = ('is_completed',)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'min_order_amount', 'max_uses', 'used_count', 'is_active')
    list_filter = ('discount_type', 'is_active')
    search_fields = ('code',)
