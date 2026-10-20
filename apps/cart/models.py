from django.db import models
from core.models import TimeStampedModel
from django.conf import settings
from products.models import ProductVariant, PrintZone
from studio.models import Design

class Cart(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="cart", verbose_name="Người dùng")
    session_key = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name="Session Key")

    def get_subtotal(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        owner = self.user.username if self.user else f"Session: {self.session_key}"
        return f"Giỏ hàng ({owner}) - {self.get_total_items()} món"

    class Meta:
        verbose_name = "Giỏ hàng"
        verbose_name_plural = "Giỏ hàng"


class CartItem(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name="Giỏ hàng")
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="cart_items", verbose_name="Biến thể áo")
    design = models.ForeignKey(Design, on_delete=models.SET_NULL, null=True, blank=True, related_name="cart_items", verbose_name="Bản thiết kế kèm theo")
    
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng")
    
    print_zone_front = models.ForeignKey(PrintZone, on_delete=models.SET_NULL, null=True, blank=True, related_name="cart_items_front", verbose_name="Khổ in trước")
    print_zone_back = models.ForeignKey(PrintZone, on_delete=models.SET_NULL, null=True, blank=True, related_name="cart_items_back", verbose_name="Khổ in sau")
    
    unit_base_price = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Giá phôi áo (VNĐ)")
    front_print_price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="Phí in mặt trước (VNĐ)")
    back_print_price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="Phí in mặt sau (VNĐ)")

    def get_unit_total_price(self):
        return self.unit_base_price + self.front_print_price + self.back_print_price

    def get_total_price(self):
        return self.get_unit_total_price() * self.quantity

    def save(self, *args, **kwargs):
        if not self.unit_base_price:
            self.unit_base_price = self.variant.get_price()
        if self.print_zone_front:
            self.front_print_price = self.print_zone_front.extra_price
        if self.print_zone_back:
            self.back_print_price = self.print_zone_back.extra_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.variant.product.name} ({self.variant.color.name}, Size {self.variant.size.name}) x {self.quantity}"

    class Meta:
        verbose_name = "Mục trong giỏ hàng"
        verbose_name_plural = "Mục trong giỏ hàng"
