from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import ProductType, Color, Size, Product, ProductImage, ProductVariant, PrintZone, SizeChart

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'display_order', 'is_studio_form', 'is_active')
    list_filter = ('is_studio_form', 'is_active')
    list_editable = ('display_order', 'is_studio_form', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_code', 'display_order')

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order')

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 2

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'product_type', 'base_price', 'badge', 'color_badge', 'is_featured', 'is_active')
    list_editable = ('base_price', 'badge', 'is_featured', 'is_active')
    list_filter = ('product_type', 'badge', 'is_featured', 'is_active')
    search_fields = ('name', 'description', 'fabric_info')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_preview_large',)
    inlines = [ProductImageInline, ProductVariantInline]
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'slug', 'product_type', 'base_price', 'badge')
        }),
        ('Hình ảnh & Màu sắc', {
            'fields': ('image_preview_large', 'thumbnail_image', 'thumbnail_url', 'color_hex')
        }),
        ('Chất liệu & Phom dáng', {
            'fields': ('fabric_info', 'fit_type', 'description')
        }),
        ('Cài đặt hiển thị', {
            'fields': ('is_featured', 'is_active')
        }),
    )

    @admin.display(description="Ảnh")
    def image_preview(self, obj):
        img_url = obj.get_main_image()
        if img_url:
            return mark_safe(f'<img src="{img_url}" style="width: 48px; height: 36px; object-fit: contain; border-radius: 6px; background: #f3f3f3; border: 1px solid #ddd;" />')
        return "-"

    @admin.display(description="Màu")
    def color_badge(self, obj):
        if obj.color_hex:
            return mark_safe(f'<span style="display: inline-block; width: 14px; height: 14px; border-radius: 50%; background: {obj.color_hex}; border: 1px solid #999; vertical-align: middle;"></span> <span style="font-size: 11px; color: #666;">{obj.color_hex}</span>')
        return "-"

    @admin.display(description="Xem trước ảnh hiện tại")
    def image_preview_large(self, obj):
        img_url = obj.get_main_image()
        if img_url:
            return mark_safe(f'<img src="{img_url}" style="max-height: 200px; max-width: 260px; object-fit: contain; border-radius: 12px; background: #f6f4f0; padding: 8px; border: 1px solid #e0e0e0;" />')
        return "Chưa có ảnh"

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size', 'get_price', 'stock_quantity', 'sku')
    list_filter = ('product', 'color', 'size')
    search_fields = ('sku', 'product__name')

@admin.register(PrintZone)
class PrintZoneAdmin(admin.ModelAdmin):
    list_display = ('product_type', 'name', 'dimensions', 'aspect_width', 'aspect_height', 'extra_price')
    list_filter = ('product_type',)

@admin.register(SizeChart)
class SizeChartAdmin(admin.ModelAdmin):
    list_display = ('product_type', 'size', 'min_height', 'max_height', 'min_weight', 'max_weight')
    list_filter = ('product_type', 'size')
