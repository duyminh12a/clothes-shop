from django.contrib import admin
from .models import Banner, Review, FAQ, ContactMessage

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'link', 'button_text', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer_name', 'product', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved')
    list_editable = ('is_approved',)
    search_fields = ('reviewer_name', 'comment', 'product__name')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    list_editable = ('is_read',)
    search_fields = ('name', 'email', 'message')
