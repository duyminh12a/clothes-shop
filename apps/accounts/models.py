from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import TimeStampedModel
import uuid

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số điện thoại")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Ảnh đại diện")
    referral_code = models.CharField(max_length=12, unique=True, blank=True, null=True, verbose_name="Mã giới thiệu")
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="referrals", verbose_name="Người giới thiệu")
    points_balance = models.PositiveIntegerField(default=0, verbose_name="Điểm Nếp Club")
    language_pref = models.CharField(max_length=5, default="vi", choices=[("vi", "Tiếng Việt"), ("en", "English")], verbose_name="Ngôn ngữ")

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name() or self.username or self.email

    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"


class Address(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses", verbose_name="Người dùng")
    full_name = models.CharField(max_length=150, verbose_name="Họ và tên người nhận")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    city = models.CharField(max_length=100, verbose_name="Tỉnh / Thành phố")
    district = models.CharField(max_length=100, verbose_name="Quận / Huyện")
    ward = models.CharField(max_length=100, verbose_name="Phường / Xã")
    street_address = models.CharField(max_length=255, verbose_name="Địa chỉ cụ thể (Số nhà, tên đường)")
    is_default = models.BooleanField(default=False, verbose_name="Địa chỉ mặc định")

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def full_address(self):
        return f"{self.street_address}, {self.ward}, {self.district}, {self.city}"

    def __str__(self):
        return f"{self.full_name} - {self.phone} ({self.street_address}, {self.city})"

    class Meta:
        verbose_name = "Địa chỉ nhận hàng"
        verbose_name_plural = "Sổ địa chỉ"
