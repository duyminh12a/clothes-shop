from django.contrib import admin
from .models import TemplateCategory, DesignTemplate, StickerCategory, Sticker, Design

@admin.register(TemplateCategory)
class TemplateCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'display_order')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(DesignTemplate)
class DesignTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slogan', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'slogan', 'tags')

@admin.register(StickerCategory)
class StickerCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order')

@admin.register(Sticker)
class StickerAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('name',)

@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'product', 'color', 'is_saved', 'created_at')
    list_filter = ('is_saved', 'product', 'color')
    search_fields = ('name', 'user__username', 'session_key')
