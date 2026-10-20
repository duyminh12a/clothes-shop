from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import ProductType, Color, Size, Product, ProductVariant, PrintZone, SizeChart, ProductImage
from studio.models import TemplateCategory, DesignTemplate, StickerCategory, Sticker
from loyalty.models import MembershipTier, Coupon
from cms.models import Banner, FAQ
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = "Khởi tạo dữ liệu mẫu cho Nếp Form (Sản phẩm, Màu sắc, Bảng size, Templates, Stickers...)"

    def handle(self, *args, **kwargs):
        self.stdout.write("Bắt đầu nạp dữ liệu mẫu...")

        # 1. Tạo Superuser Admin
        if not User.objects.filter(username="admin").exists():
            admin_user = User.objects.create_superuser(
                username="admin",
                email="admin@nepform.vn",
                password="admin123",
                first_name="Admin",
                last_name="Nếp Form"
            )
            self.stdout.write(self.style.SUCCESS("✓ Đã tạo tài khoản admin: admin / admin123 (email: admin@nepform.vn)"))
        else:
            admin_user = User.objects.get(username="admin")

        # 2. Tạo Bảng màu
        colors_data = [
            ("Kem", "#F5F0E8", 1),
            ("Trắng", "#FFFFFF", 2),
            ("Đen", "#1A1A1A", 3),
            ("Xanh rêu", "#647746", 4),
            ("Xám tiêu", "#9E9E9E", 5),
        ]
        color_objs = {}
        for name, hex_code, order in colors_data:
            c, _ = Color.objects.get_or_create(name=name, defaults={"hex_code": hex_code, "display_order": order})
            color_objs[name] = c
        self.stdout.write(self.style.SUCCESS(f"✓ Đã tạo {len(color_objs)} màu sắc"))

        # 3. Tạo Kích cỡ (Size)
        sizes_data = [("S", 1), ("M", 2), ("L", 3), ("XL", 4), ("2XL", 5)]
        size_objs = {}
        for name, order in sizes_data:
            s, _ = Size.objects.get_or_create(name=name, defaults={"display_order": order})
            size_objs[name] = s
        self.stdout.write(self.style.SUCCESS(f"✓ Đã tạo {len(size_objs)} kích cỡ"))

        # 4. Tạo Loại sản phẩm
        types_data = [
            ("Áo custom Classic", "ao-custom-classic", "Phom áo suông vừa vặn chuẩn tỉ lệ cơ thể người Việt, viền cổ dệt kỹ bo tròn."),
            ("Áo thun Oversize", "ao-thun-oversize", "Form rộng thoải mái, phong cách streetwear trẻ trung, vai trễ."),
            ("Áo Polo Pique", "ao-polo-pique", "Chất liệu dệt Pique cao cấp, cổ bẻ lịch sự tôn dáng."),
            ("Áo Hoodie Nếp", "ao-hoodie-nep", "Chất nỉ bông mềm ấm, mũ 2 lớp đứng form kèm túi kangaroo."),
            ("Túi Canvas Tote", "tui-canvas-tote", "Vải canvas 100% mộc mạc bền bỉ, quai đeo may chéo chịu lực cao."),
        ]
        type_objs = {}
        for name, slug, desc in types_data:
            t, _ = ProductType.objects.get_or_create(slug=slug, defaults={"name": name, "description": desc})
            type_objs[slug] = t
        self.stdout.write(self.style.SUCCESS(f"✓ Đã tạo {len(type_objs)} loại sản phẩm"))

        # 5. Cấu hình Khổ in (Print Zones) cho Áo Classic
        classic_type = type_objs["ao-custom-classic"]
        print_zones = [
            ("Nhỏ", "15 × 18 cm", 150, 180, Decimal("0"), 1),
            ("Vừa", "22 × 26 cm", 220, 260, Decimal("25000"), 2),
            ("Lớn", "30 × 35 cm", 300, 350, Decimal("45000"), 3),
        ]
        for name, dims, w, h, fee, order in print_zones:
            PrintZone.objects.get_or_create(
                product_type=classic_type,
                name=name,
                defaults={"dimensions": dims, "aspect_width": w, "aspect_height": h, "extra_price": fee, "display_order": order}
            )
        self.stdout.write(self.style.SUCCESS("✓ Đã cấu hình các khổ in (Nhỏ, Vừa, Lớn)"))

        # 6. Bảng tư vấn size (Size Chart)
        size_ranges = [
            ("S", 150, 165, 42, 53, "Phom vừa vặn, người nhỏ nhắn mặc đẹp."),
            ("M", 160, 172, 52, 64, "Kích cỡ chuẩn phổ thông nhất."),
            ("L", 168, 178, 62, 75, "Gợi ý theo chiều cao và cân nặng trong bảng size tham khảo của Nếp. Phom rộng vừa có thể cho độ rộng khác nhau."),
            ("XL", 175, 185, 74, 86, "Dành cho người thích mặc rộng rãi hoặc có thể trạng cao to."),
            ("2XL", 180, 195, 85, 100, "Phom cực đại, độ che khuyết điểm tốt."),
        ]
        for s_name, min_h, max_h, min_w, max_w, note in size_ranges:
            SizeChart.objects.get_or_create(
                product_type=classic_type,
                size=size_objs[s_name],
                defaults={
                    "min_height": min_h,
                    "max_height": max_h,
                    "min_weight": min_w,
                    "max_weight": max_w,
                    "recommendation_note": note
                }
            )
        self.stdout.write(self.style.SUCCESS("✓ Đã nạp bảng tư vấn size thông minh"))

        # 7. Tạo Sản phẩm chính
        p1, _ = Product.objects.get_or_create(
            slug="ao-custom-classic",
            defaults={
                "product_type": classic_type,
                "name": "Áo custom Classic",
                "base_price": Decimal("280000"),
                "fabric_info": "Cotton 100% 2-chiều (định lượng 240gsm, xử lý chống co rút)",
                "fit_type": "Phối unisex",
                "description": "Chiếc áo phông căn bản nhưng chỉn chu từ thớ vải đến đường may. Vải cotton tự nhiên dệt dày dặn, thấm hút mồ hôi tốt và giữ form hoàn hảo sau nhiều lần giặt.",
                "is_featured": True,
            }
        )

        p2, _ = Product.objects.get_or_create(
            slug="ao-thun-den-basic",
            defaults={
                "product_type": classic_type,
                "name": "Áo thun đen basic",
                "base_price": Decimal("250000"),
                "fabric_info": "Cotton 100% thoáng mát",
                "fit_type": "Phối unisex",
                "description": "Gam màu đen tuyền cá tính, dễ phối đồ mọi hoàn cảnh.",
                "is_featured": True,
            }
        )

        # Tạo ProductVariants cho p1 (Classic) với tất cả các màu và size
        for color_name, color_obj in color_objs.items():
            for size_name, size_obj in size_objs.items():
                ProductVariant.objects.get_or_create(
                    product=p1,
                    color=color_obj,
                    size=size_obj,
                    defaults={"stock_quantity": 30, "price_override": None}
                )
        self.stdout.write(self.style.SUCCESS("✓ Đã tạo các biến thể sản phẩm (Màu x Size)"))

        # 8. Templates Nếp Studio
        cat_tuyenngon, _ = TemplateCategory.objects.get_or_create(name="Tuyên ngôn riêng", defaults={"slug": "tuyen-ngon-rieng", "display_order": 1})
        cat_cunuthoi, _ = TemplateCategory.objects.get_or_create(name="Cứ nở thôi", defaults={"slug": "cu-no-thoi", "display_order": 2})
        cat_nepclub, _ = TemplateCategory.objects.get_or_create(name="Hội mình có chất", defaults={"slug": "hoi-minh-co-chat", "display_order": 3})

        DesignTemplate.objects.get_or_create(
            category=cat_tuyenngon,
            name="LÀ MÌNH. MỘT BẢN DUY NHẤT",
            defaults={
                "slogan": "CÁCH CỦA BẠN",
                "tags": "chữ, typo, tối giản, cá tính",
                "is_featured": True
            }
        )

        DesignTemplate.objects.get_or_create(
            category=cat_cunuthoi,
            name="NỞ THEO CÁCH CỦA BẠN",
            defaults={
                "slogan": "Cứ nở thôi",
                "tags": "hoa, dễ thương, tích cực",
                "is_featured": True
            }
        )

        DesignTemplate.objects.get_or_create(
            category=cat_nepclub,
            name="NẾP CLUB",
            defaults={
                "slogan": "Hội mình có chất",
                "tags": "câu lạc bộ, hội nhóm, sticker",
                "is_featured": True
            }
        )
        self.stdout.write(self.style.SUCCESS("✓ Đã tạo kho mẫu thiết kế Nếp Studio"))

        # 9. Stickers
        stk_cat, _ = StickerCategory.objects.get_or_create(name="Biểu tượng Nếp", defaults={"display_order": 1})
        
        # SVG hoa cúc
        flower_svg = '''<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="14" fill="#E5C158"/>
            <path d="M50 12C55 12 58 24 50 32C42 24 45 12 50 12Z" fill="#647746"/>
            <path d="M50 88C45 88 42 76 50 68C58 76 55 88 50 88Z" fill="#647746"/>
            <path d="M12 50C12 45 24 42 32 50C24 58 12 55 12 50Z" fill="#647746"/>
            <path d="M88 50C88 55 76 58 68 50C76 42 88 45 88 50Z" fill="#647746"/>
            <path d="M23 23C27 20 36 29 37 37C29 36 20 27 23 23Z" fill="#647746"/>
            <path d="M77 77C73 80 64 71 63 63C71 64 80 73 77 77Z" fill="#647746"/>
            <path d="M23 77C20 73 29 64 37 63C36 71 27 80 23 77Z" fill="#647746"/>
            <path d="M77 23C80 27 71 36 63 37C64 29 73 20 77 23Z" fill="#647746"/>
        </svg>'''

        smiley_svg = '''<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="44" stroke="#1A1A1A" stroke-width="8" fill="#D4E157"/>
            <circle cx="35" cy="40" r="6" fill="#1A1A1A"/>
            <circle cx="65" cy="40" r="6" fill="#1A1A1A"/>
            <path d="M32 62C40 74 60 74 68 62" stroke="#1A1A1A" stroke-width="8" stroke-linecap="round"/>
        </svg>'''

        Sticker.objects.get_or_create(category=stk_cat, name="Hoa Nếp", defaults={"svg_code": flower_svg})
        Sticker.objects.get_or_create(category=stk_cat, name="Mặt cười Nếp", defaults={"svg_code": smiley_svg})
        self.stdout.write(self.style.SUCCESS("✓ Đã nạp sticker Vector trực quan"))

        # 10. Hạng thành viên Nếp Club
        MembershipTier.objects.get_or_create(
            name="Thường",
            defaults={"min_points": 0, "discount_percent": 0, "free_shipping_threshold": Decimal("500000"), "badge_color": "#9E9E9E"}
        )
        MembershipTier.objects.get_or_create(
            name="Bạc",
            defaults={"min_points": 500, "discount_percent": 5, "free_shipping_threshold": Decimal("300000"), "badge_color": "#C0C0C0"}
        )
        MembershipTier.objects.get_or_create(
            name="Vàng",
            defaults={"min_points": 2000, "discount_percent": 10, "free_shipping_threshold": Decimal("0"), "badge_color": "#C4A35A", "exclusive_access": True}
        )
        self.stdout.write(self.style.SUCCESS("✓ Đã cấu hình các hạng thành viên Nếp Club"))

        # 11. Mã giảm giá
        Coupon.objects.get_or_create(
            code="NEPFORM20",
            defaults={
                "discount_type": "PERCENT",
                "discount_value": Decimal("20"),
                "min_order_amount": Decimal("200000"),
                "max_discount_amount": Decimal("80000"),
                "max_uses": 500
            }
        )
        Coupon.objects.get_or_create(
            code="NEP50K",
            defaults={
                "discount_type": "FIXED",
                "discount_value": Decimal("50000"),
                "min_order_amount": Decimal("300000"),
                "max_uses": 200
            }
        )
        self.stdout.write(self.style.SUCCESS("✓ Đã tạo mã giảm giá: NEPFORM20 (-20%), NEP50K (-50k)"))

        # 12. Banners & FAQs
        Banner.objects.get_or_create(
            title="Mặc một điều rất riêng.",
            defaults={
                "subtitle": "Từ một câu bạn thích, một nét vẽ vu vơ. Tự tay tạo nên chiếc áo mang dấu ấn của mình.",
                "link": "/studio/",
                "button_text": "Bắt đầu thiết kế ↗",
                "display_order": 1
            }
        )

        FAQ.objects.get_or_create(
            question="Chất liệu áo của Nếp có bền không?",
            defaults={"answer": "Nếp sử dụng 100% Cotton định lượng 240gsm cao cấp, đã qua xử lý chống co rút, thoáng mát và co giãn êm ái.", "display_order": 1}
        )
        FAQ.objects.get_or_create(
            question="Hình in có bị bong tróc khi giặt máy không?",
            defaults={"answer": "Nếp áp dụng công nghệ in DTG kỹ thuật số mực Nhật Bản thấm sâu vào sợi vải, độ bền trên 100 lần giặt không bong tróc.", "display_order": 2}
        )

        self.stdout.write(self.style.SUCCESS("Hoàn tất nạp toàn bộ dữ liệu mẫu thành công! 🎉"))
