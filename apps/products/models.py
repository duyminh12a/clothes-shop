from django.db import models
from core.models import TimeStampedModel
from django.utils.text import slugify

class ProductType(TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name="Loại sản phẩm")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Mô tả")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự hiển thị")
    is_studio_form = models.BooleanField(default=False, verbose_name="Phôi dùng cho Studio")
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Loại sản phẩm"
        verbose_name_plural = "Các loại sản phẩm"
        ordering = ['display_order', 'name']


class Color(TimeStampedModel):
    name = models.CharField(max_length=50, verbose_name="Tên màu")
    hex_code = models.CharField(max_length=10, verbose_name="Mã màu HEX (VD: #F5F0E8)")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự")

    def __str__(self):
        return f"{self.name} ({self.hex_code})"

    class Meta:
        verbose_name = "Màu sắc"
        verbose_name_plural = "Bảng màu"
        ordering = ['display_order', 'name']


class Size(TimeStampedModel):
    name = models.CharField(max_length=20, verbose_name="Tên size (S, M, L, XL...)")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kích cỡ"
        verbose_name_plural = "Kích cỡ (Size)"
        ordering = ['display_order']


class Product(TimeStampedModel):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name="products", verbose_name="Loại sản phẩm")
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    base_price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Giá cơ bản (VNĐ)")
    fabric_info = models.CharField(max_length=200, default="Cotton 100% (định lượng 240gsm)", verbose_name="Chất liệu vải")
    fit_type = models.CharField(max_length=100, default="Phối unisex", verbose_name="Phom dáng")
    description = models.TextField(blank=True, verbose_name="Mô tả sản phẩm")
    badge = models.CharField(max_length=50, blank=True, verbose_name="Huy hiệu (VD: Mới)")
    color_hex = models.CharField(max_length=20, blank=True, default="#F5F0E8", verbose_name="Mã màu đại diện")
    thumbnail_url = models.TextField(blank=True, verbose_name="Ảnh đại diện trực tiếp hoặc Data URL")
    thumbnail_image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Hoặc tải file ảnh lên")
    is_featured = models.BooleanField(default=False, verbose_name="Nổi bật trang chủ")
    is_active = models.BooleanField(default=True, verbose_name="Đang bán")

    def get_main_image(self):
        if self.thumbnail_url:
            return self.thumbnail_url
        if self.thumbnail_image:
            try:
                return self.thumbnail_image.url
            except Exception:
                pass
        img = self.images.filter(is_front=True).first() or self.images.first()
        if img:
            return img.get_image_url()
        return f"/static/images/products/{self.slug}.png"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.base_price:,.0f}₫"

    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Danh mục sản phẩm"


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="Sản phẩm")
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, related_name="mockups", verbose_name="Màu áo tương ứng")
    is_front = models.BooleanField(default=True, verbose_name="Mặt trước")
    is_back = models.BooleanField(default=False, verbose_name="Mặt sau")
    image = models.ImageField(upload_to="mockups/", blank=True, null=True, verbose_name="Ảnh mockup (PNG nền trong suốt)")
    image_url = models.CharField(max_length=500, blank=True, verbose_name="Hoặc URL ảnh trực tiếp")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự")

    def get_image_url(self):
        if self.image:
            return self.image.url
        return self.image_url or "/static/images/mockups/tshirt_front_cream.png"

    def __str__(self):
        side = "Trước" if self.is_front else "Sau"
        return f"{self.product.name} - {self.color.name if self.color else 'Mặc định'} ({side})"

    class Meta:
        verbose_name = "Ảnh mockup sản phẩm"
        verbose_name_plural = "Ảnh mockup sản phẩm"


class ProductVariant(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants", verbose_name="Sản phẩm")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name="Màu")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name="Size")
    price_override = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name="Giá riêng biệt (nếu có)")
    stock_quantity = models.PositiveIntegerField(default=50, verbose_name="Tồn kho")
    sku = models.CharField(max_length=50, unique=True, blank=True, verbose_name="Mã SKU")

    def get_price(self):
        return self.price_override if self.price_override is not None else self.product.base_price

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"{self.product.id}-{self.color.id}-{self.size.id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} / {self.color.name} / {self.size.name} ({self.stock_quantity} cái)"

    class Meta:
        verbose_name = "Biến thể sản phẩm (SKU)"
        verbose_name_plural = "Các biến thể sản phẩm"
        unique_together = ('product', 'color', 'size')


class PrintZone(TimeStampedModel):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name="print_zones", verbose_name="Loại sản phẩm")
    name = models.CharField(max_length=50, verbose_name="Tên khổ in (Nhỏ, Vừa, Lớn)")
    dimensions = models.CharField(max_length=50, verbose_name="Kích thước thực tế (VD: 22 × 26 cm)")
    aspect_width = models.PositiveIntegerField(default=220, verbose_name="Chiều rộng vùng in trên canvas (px)")
    aspect_height = models.PositiveIntegerField(default=260, verbose_name="Chiều cao vùng in trên canvas (px)")
    extra_price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="Phí in thêm (VNĐ)")
    display_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product_type.name} - Khổ {self.name} ({self.dimensions})"

    class Meta:
        verbose_name = "Vùng in / Khổ in"
        verbose_name_plural = "Cấu hình vùng in"
        ordering = ['display_order']


class SizeChart(TimeStampedModel):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name="size_charts", verbose_name="Loại sản phẩm")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name="Size gợi ý")
    min_height = models.PositiveIntegerField(verbose_name="Chiều cao tối thiểu (cm)")
    max_height = models.PositiveIntegerField(verbose_name="Chiều cao tối đa (cm)")
    min_weight = models.PositiveIntegerField(verbose_name="Cân nặng tối thiểu (kg)")
    max_weight = models.PositiveIntegerField(verbose_name="Cân nặng tối đa (kg)")
    recommendation_note = models.CharField(max_length=255, blank=True, default="Gợi ý theo chiều cao và cân nặng trong bảng size tham khảo của Nếp.")

    def __str__(self):
        return f"{self.product_type.name} - Size {self.size.name} ({self.min_height}-{self.max_height}cm, {self.min_weight}-{self.max_weight}kg)"

    class Meta:
        verbose_name = "Bảng tư vấn kích cỡ (Size Chart)"
        verbose_name_plural = "Bảng tư vấn kích cỡ"
