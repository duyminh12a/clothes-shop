from django.contrib import admin
from .models import ProductType, Color, Size, Product, ProductImage, ProductVariant, PrintZone, SizeChart

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'display_order', 'is_active')
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
    list_display = ('name', 'product_type', 'base_price', 'fit_type', 'is_featured', 'is_active')
    list_filter = ('product_type', 'is_featured', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariantInline]

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
