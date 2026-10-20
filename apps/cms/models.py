from django.db import models
from core.models import TimeStampedModel
from django.conf import settings
from products.models import Product

class Banner(TimeStampedModel):
    title = models.CharField(max_length=200, verbose_name="Tiêu đề banner")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Phụ đề")
    image = models.ImageField(upload_to="banners/", blank=True, null=True, verbose_name="Ảnh banner")
    image_url = models.CharField(max_length=500, blank=True, verbose_name="Hoặc URL ảnh")
    link = models.CharField(max_length=255, default="/studio/", verbose_name="Link điều hướng")
    button_text = models.CharField(max_length=50, default="Bắt đầu thiết kế ↗", verbose_name="Chữ trên nút")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự")
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Banner trang chủ"
        verbose_name_plural = "Quản lý Banner"
        ordering = ['display_order']


class Review(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tài khoản")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", verbose_name="Sản phẩm")
    reviewer_name = models.CharField(max_length=100, verbose_name="Tên người đánh giá")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="Số sao (1 - 5)")
    comment = models.TextField(verbose_name="Nội dung đánh giá")
    is_approved = models.BooleanField(default=True, verbose_name="Được duyệt hiển thị")

    def __str__(self):
        return f"{self.reviewer_name} - {self.rating}★ cho {self.product.name}"

    class Meta:
        verbose_name = "Đánh giá của khách hàng"
        verbose_name_plural = "Quản lý Đánh giá"
        ordering = ['-created_at']


class FAQ(TimeStampedModel):
    question = models.CharField(max_length=255, verbose_name="Câu hỏi")
    answer = models.TextField(verbose_name="Câu trả lời")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Câu hỏi thường gặp (FAQ)"
        verbose_name_plural = "Câu hỏi thường gặp"
        ordering = ['display_order']


class ContactMessage(TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name="Họ và tên")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Số điện thoại")
    message = models.TextField(verbose_name="Nội dung tin nhắn")
    is_read = models.BooleanField(default=False, verbose_name="Đã đọc / Đã xử lý")

    def __str__(self):
        return f"{self.name} ({self.email}): {self.message[:40]}..."

    class Meta:
        verbose_name = "Tin nhắn liên hệ"
        verbose_name_plural = "Hộp thư liên hệ"
        ordering = ['-created_at']
