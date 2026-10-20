from django.db import models
from core.models import TimeStampedModel
from django.conf import settings
from products.models import Product, Color, PrintZone

class TemplateCategory(TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name="Tên bộ sưu tập mẫu")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Danh mục mẫu thiết kế"
        verbose_name_plural = "Danh mục mẫu thiết kế"
        ordering = ['display_order', 'name']


class DesignTemplate(TimeStampedModel):
    category = models.ForeignKey(TemplateCategory, on_delete=models.CASCADE, related_name="templates", verbose_name="Danh mục")
    name = models.CharField(max_length=200, verbose_name="Tên mẫu thiết kế")
    slogan = models.CharField(max_length=200, blank=True, verbose_name="Slogan / Phụ đề")
    preview_image = models.ImageField(upload_to="templates/", blank=True, null=True, verbose_name="Ảnh preview")
    preview_url = models.CharField(max_length=500, blank=True, verbose_name="Hoặc URL ảnh preview")
    canvas_json_front = models.TextField(blank=True, default="{}", verbose_name="Dữ liệu Fabric.js mặt trước")
    canvas_json_back = models.TextField(blank=True, default="{}", verbose_name="Dữ liệu Fabric.js mặt sau")
    tags = models.CharField(max_length=255, blank=True, verbose_name="Thẻ tag (cách nhau dấu phẩy)")
    is_featured = models.BooleanField(default=True, verbose_name="Hiện trang chủ / nổi bật")

    def get_preview(self):
        if self.preview_image:
            return self.preview_image.url
        return self.preview_url or ""

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    class Meta:
        verbose_name = "Mẫu thiết kế có sẵn"
        verbose_name_plural = "Kho mẫu thiết kế (Templates)"


class StickerCategory(TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name="Danh mục sticker/icon")
    display_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Danh mục hình vẽ/Sticker"
        verbose_name_plural = "Danh mục hình vẽ/Sticker"


class Sticker(TimeStampedModel):
    category = models.ForeignKey(StickerCategory, on_delete=models.CASCADE, related_name="stickers", verbose_name="Danh mục")
    name = models.CharField(max_length=100, verbose_name="Tên hình vẽ")
    image = models.ImageField(upload_to="stickers/", blank=True, null=True, verbose_name="Ảnh PNG/SVG")
    svg_code = models.TextField(blank=True, verbose_name="Mã SVG trực tiếp")
    image_url = models.CharField(max_length=500, blank=True, verbose_name="Hoặc URL ảnh trực tiếp")
    is_featured = models.BooleanField(default=True)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return self.image_url or ""

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Hình vẽ / Sticker"
        verbose_name_plural = "Kho hình vẽ / Sticker"


class Design(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="designs", verbose_name="Người tạo")
    session_key = models.CharField(max_length=100, blank=True, null=True, verbose_name="Session nếu là khách vãng lai")
    name = models.CharField(max_length=200, default="Chiếc áo của tôi", verbose_name="Tên bản thiết kế")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="designs", verbose_name="Sản phẩm áp dụng")
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Màu áo đã chọn")
    
    print_zone_front = models.ForeignKey(PrintZone, on_delete=models.SET_NULL, null=True, blank=True, related_name="designs_front", verbose_name="Khổ in mặt trước")
    print_zone_back = models.ForeignKey(PrintZone, on_delete=models.SET_NULL, null=True, blank=True, related_name="designs_back", verbose_name="Khổ in mặt sau")

    canvas_json_front = models.TextField(default="{}", verbose_name="Canvas JSON mặt trước")
    canvas_json_back = models.TextField(default="{}", verbose_name="Canvas JSON mặt sau")
    
    preview_front = models.TextField(blank=True, verbose_name="Base64 hoặc URL ảnh preview trước")
    preview_back = models.TextField(blank=True, verbose_name="Base64 hoặc URL ảnh preview sau")
    
    is_saved = models.BooleanField(default=False, verbose_name="Đã lưu vào danh sách của tôi")

    def __str__(self):
        owner = self.user.username if self.user else "Khách"
        return f"{self.name} ({owner}) - {self.product.name}"

    class Meta:
        verbose_name = "Bản thiết kế"
        verbose_name_plural = "Bản thiết kế của người dùng"
        ordering = ['-updated_at']
