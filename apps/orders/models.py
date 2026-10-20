from django.db import models
from core.models import TimeStampedModel
from django.conf import settings
from products.models import ProductVariant
from studio.models import Design
import uuid

class Order(TimeStampedModel):
    STATUS_CHOICES = [
        ('PENDING', 'Chờ xử lý'),
        ('AWAITING_PAYMENT', 'Chờ thanh toán online'),
        ('CONFIRMED', 'Đã xác nhận đơn'),
        ('PROCESSING', 'Đang in ấn & xử lý'),
        ('SHIPPING', 'Đang giao hàng'),
        ('COMPLETED', 'Đã hoàn thành'),
        ('CANCELLED', 'Đã hủy'),
        ('REFUNDED', 'Đã hoàn tiền'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Thanh toán khi nhận hàng (COD)'),
        ('BANK', 'Chuyển khoản trực tiếp ngân hàng'),
        ('VNPAY', 'Cổng thanh toán VNPAY QR / Thẻ ATM'),
        ('MOMO', 'Ví điện tử MoMo'),
        ('ZALOPAY', 'Ví điện tử ZaloPay'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('UNPAID', 'Chưa thanh toán'),
        ('PAID', 'Đã thanh toán thành công'),
        ('FAILED', 'Thanh toán thất bại'),
        ('REFUNDED', 'Đã hoàn tiền'),
    ]

    order_code = models.CharField(max_length=32, unique=True, verbose_name="Mã đơn hàng")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders", verbose_name="Tài khoản mua")
    
    # Thông tin khách hàng
    customer_name = models.CharField(max_length=150, verbose_name="Tên khách hàng")
    customer_phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    customer_email = models.EmailField(blank=True, verbose_name="Email nhận thông báo")
    shipping_address = models.TextField(verbose_name="Địa chỉ nhận hàng đầy đủ")
    
    # Trạng thái
    order_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING', verbose_name="Trạng thái đơn hàng")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='COD', verbose_name="Phương thức thanh toán")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='UNPAID', verbose_name="Trạng thái thanh toán")
    
    # Giá trị
    subtotal = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Tiền hàng (VNĐ)")
    discount_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Tiền giảm giá (VNĐ)")
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=0, default=30000, verbose_name="Phí giao hàng (VNĐ)")
    total_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Tổng thanh toán (VNĐ)")
    
    # Điểm Nếp Club & Coupon
    coupon_code = models.CharField(max_length=50, blank=True, verbose_name="Mã giảm giá đã dùng")
    points_used = models.PositiveIntegerField(default=0, verbose_name="Điểm thưởng đã cấn trừ")
    points_earned = models.PositiveIntegerField(default=0, verbose_name="Điểm thưởng nhận được")
    
    note = models.TextField(blank=True, verbose_name="Ghi chú đơn hàng")

    def save(self, *args, **kwargs):
        if not self.order_code:
            self.order_code = f"NEP{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"#{self.order_code} - {self.customer_name} ({self.total_amount:,.0f}₫)"

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Quản lý Đơn hàng"
        ordering = ['-created_at']


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Đơn hàng")
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Biến thể gốc")
    design = models.ForeignKey(Design, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bản thiết kế áo")
    
    product_name = models.CharField(max_length=200, verbose_name="Tên áo")
    color_name = models.CharField(max_length=50, verbose_name="Màu áo")
    size_name = models.CharField(max_length=20, verbose_name="Size")
    
    print_zone_front_name = models.CharField(max_length=100, blank=True, verbose_name="Khổ in mặt trước")
    print_zone_back_name = models.CharField(max_length=100, blank=True, verbose_name="Khổ in mặt sau")
    
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng")
    unit_base_price = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Giá phôi áo")
    front_print_price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="Phí in trước")
    back_print_price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="Phí in sau")
    subtotal = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Thành tiền")

    # File vector/raster phân giải cao dành riêng cho xưởng in
    print_export_front = models.FileField(upload_to="print_exports/", blank=True, null=True, verbose_name="File in mặt trước (300dpi)")
    print_export_back = models.FileField(upload_to="print_exports/", blank=True, null=True, verbose_name="File in mặt sau (300dpi)")

    def save(self, *args, **kwargs):
        unit_price = self.unit_base_price + self.front_print_price + self.back_print_price
        self.subtotal = unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} - {self.color_name} / {self.size_name} x {self.quantity}"

    class Meta:
        verbose_name = "Chi tiết sản phẩm đặt"
        verbose_name_plural = "Chi tiết sản phẩm đặt"


class PaymentTransaction(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="transactions", verbose_name="Đơn hàng")
    gateway = models.CharField(max_length=30, verbose_name="Cổng thanh toán")
    transaction_id = models.CharField(max_length=100, verbose_name="Mã giao dịch cổng")
    amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Số tiền")
    status = models.CharField(max_length=30, verbose_name="Trạng thái giao dịch")
    raw_response = models.TextField(blank=True, verbose_name="Dữ liệu trả về (JSON)")

    def __str__(self):
        return f"{self.gateway} #{self.transaction_id} - {self.amount:,.0f}₫ ({self.status})"

    class Meta:
        verbose_name = "Giao dịch thanh toán"
        verbose_name_plural = "Nhật ký thanh toán"
