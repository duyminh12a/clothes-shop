from django.db import models
from core.models import TimeStampedModel
from django.conf import settings

class MembershipTier(TimeStampedModel):
    name = models.CharField(max_length=50, verbose_name="Tên hạng (Thường, Bạc, Vàng)")
    min_points = models.PositiveIntegerField(default=0, verbose_name="Điểm tối thiểu đạt hạng")
    discount_percent = models.PositiveIntegerField(default=0, verbose_name="% Giảm giá đơn hàng")
    free_shipping_threshold = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Miễn phí ship cho đơn từ (VNĐ)")
    badge_color = models.CharField(max_length=20, default="#C4A35A", verbose_name="Màu huy hiệu")
    exclusive_access = models.BooleanField(default=False, verbose_name="Được mua sản phẩm độc quyền")

    def __str__(self):
        return f"Hạng {self.name} (từ {self.min_points} điểm - giảm {self.discount_percent}%)"

    class Meta:
        verbose_name = "Hạng thành viên Nếp Club"
        verbose_name_plural = "Cấu hình Hạng thành viên"
        ordering = ['min_points']


class PointTransaction(TimeStampedModel):
    TYPE_CHOICES = [
        ('EARN', 'Tích điểm đơn hàng'),
        ('SPEND', 'Đổi điểm giảm giá'),
        ('REFERRAL', 'Thưởng giới thiệu bạn bè'),
        ('BONUS', 'Quà tặng sinh nhật / Sự kiện'),
        ('EXPIRE', 'Điểm hết hạn'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="point_history", verbose_name="Thành viên")
    points = models.IntegerField(verbose_name="Số điểm (+ hoặc -)")
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Loại giao dịch")
    description = models.CharField(max_length=255, verbose_name="Mô tả")

    def __str__(self):
        sign = "+" if self.points > 0 else ""
        return f"{self.user.username}: {sign}{self.points} điểm ({self.get_transaction_type_display()})"

    class Meta:
        verbose_name = "Lịch sử điểm Nếp Club"
        verbose_name_plural = "Lịch sử điểm Nếp Club"
        ordering = ['-created_at']


class Referral(TimeStampedModel):
    referrer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_referrals", verbose_name="Người giới thiệu")
    referee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_referral", verbose_name="Người được giới thiệu")
    points_awarded = models.PositiveIntegerField(default=50, verbose_name="Điểm đã cộng")
    is_completed = models.BooleanField(default=False, verbose_name="Đã hoàn thành đơn đầu")

    def __str__(self):
        return f"{self.referrer.username} -> {self.referee.username} (Đơn đầu: {self.is_completed})"

    class Meta:
        verbose_name = "Lượt giới thiệu bạn bè"
        verbose_name_plural = "Quản lý Giới thiệu bạn bè"


class Coupon(TimeStampedModel):
    TYPE_CHOICES = [
        ('PERCENT', 'Giảm theo phần trăm (%)'),
        ('FIXED', 'Giảm số tiền cố định (VNĐ)'),
    ]

    code = models.CharField(max_length=30, unique=True, verbose_name="Mã giảm giá (VD: NEPNEW)")
    discount_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='PERCENT', verbose_name="Loại giảm")
    discount_value = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Giá trị giảm (% hoặc VNĐ)")
    min_order_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Đơn hàng tối thiểu (VNĐ)")
    max_discount_amount = models.DecimalField(max_digits=12, decimal_places=0, default=100000, verbose_name="Mức giảm tối đa (nếu giảm %)")
    max_uses = models.PositiveIntegerField(default=100, verbose_name="Số lượt sử dụng tối đa")
    used_count = models.PositiveIntegerField(default=0, verbose_name="Đã dùng")
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")

    def calculate_discount(self, order_subtotal):
        if not self.is_active or order_subtotal < self.min_order_amount or self.used_count >= self.max_uses:
            return 0
        if self.discount_type == 'PERCENT':
            val = (order_subtotal * self.discount_value) / 100
            return min(val, self.max_discount_amount)
        else:
            return min(self.discount_value, order_subtotal)

    def __str__(self):
        val_display = f"{self.discount_value}%" if self.discount_type == 'PERCENT' else f"{self.discount_value:,.0f}₫"
        return f"{self.code} (-{val_display})"

    class Meta:
        verbose_name = "Mã giảm giá (Coupon)"
        verbose_name_plural = "Quản lý Mã giảm giá"
