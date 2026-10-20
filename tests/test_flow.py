from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product, Color, Size, SizeChart, PrintZone, ProductType, ProductVariant
from studio.models import Design
from cart.models import Cart
from orders.models import Order
from decimal import Decimal
import json

class NepFormEndToEndTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.ptype, _ = ProductType.objects.get_or_create(slug="ao-custom-classic", defaults={"name": "Áo custom Classic"})
        self.color, _ = Color.objects.get_or_create(hex_code="#F5F0E8", defaults={"name": "Kem"})
        self.size_l, _ = Size.objects.get_or_create(name="L", defaults={"display_order": 3})
        self.size_m, _ = Size.objects.get_or_create(name="M", defaults={"display_order": 2})
        
        self.product, _ = Product.objects.get_or_create(
            slug="ao-thun-den-basic",
            defaults={
                "product_type": self.ptype,
                "name": "Áo thun đen basic",
                "base_price": Decimal("250000"),
                "is_active": True
            }
        )

        self.variant, _ = ProductVariant.objects.get_or_create(
            product=self.product,
            color=self.color,
            size=self.size_l,
            defaults={"stock_quantity": 50}
        )

        self.size_chart = SizeChart.objects.create(
            product_type=self.ptype,
            size=self.size_l,
            min_height=168,
            max_height=178,
            min_weight=65,
            max_weight=75,
            recommendation_note="Gợi ý theo chiều cao và cân nặng trong bảng size tham khảo của Nếp."
        )

        self.print_zone = PrintZone.objects.create(
            product_type=self.ptype,
            name="Vừa",
            dimensions="22 × 26 cm",
            aspect_width=220,
            aspect_height=260,
            extra_price=Decimal("25000")
        )

    def test_homepage_loads(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "nếp form.")
        self.assertContains(res, "Mặc một điều")

    def test_studio_page_loads(self):
        res = self.client.get('/studio/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "nếp studio.")
        self.assertContains(res, "Chiếc áo của tôi")

    def test_size_calculator_api_matches_reference_image(self):
        # Image 2 test: 170cm, 70kg -> suggested size L
        res = self.client.get('/api/calculate-size/?height=170&weight=70')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['suggested_size'], 'L')
        self.assertIn("Gợi ý theo chiều cao và cân nặng", data['note'])

    def test_cart_add_and_checkout_flow(self):
        # 1. Add to cart
        payload = {
            'product_id': self.product.id,
            'color_id': self.color.id,
            'size_id': self.size_l.id,
            'quantity': 2,
            'print_zone_front_id': self.print_zone.id
        }
        res = self.client.post(
            '/gio-hang/api/add/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['status'], 'success')

        # 2. View cart
        res = self.client.get('/gio-hang/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Áo thun đen basic")

        # 3. Checkout
        checkout_data = {
            'customer_name': 'Khách Hàng Thử Nghiệm',
            'customer_phone': '0901234567',
            'customer_email': 'test@nepform.vn',
            'city': 'Hồ Chí Minh',
            'district': 'Quận 1',
            'ward': 'Phường Bến Nghé',
            'street_address': '123 Lê Lợi',
            'payment_method': 'BANK',
            'note': 'Áo in nét đẹp giúp mình nhé'
        }
        res = self.client.post('/don-hang/thanh-toan/', data=checkout_data, follow=True)
        self.assertEqual(res.status_code, 200)
        
        # Verify order in DB
        order = Order.objects.filter(customer_name='Khách Hàng Thử Nghiệm').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.payment_method, 'BANK')
        self.assertEqual(order.order_status, 'AWAITING_PAYMENT')

    def test_admin_panel_dashboard_access(self):
        # 1. Anonymous user cannot access /quan-tri/
        res = self.client.get('/quan-tri/')
        self.assertEqual(res.status_code, 302)

        # 2. Staff user can access /quan-tri/
        from accounts.models import User
        staff_user = User.objects.create_user(
            username='staff_test',
            email='staff@nepform.vn',
            password='password123',
            is_staff=True
        )
        self.client.force_login(staff_user)
        res = self.client.get('/quan-tri/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Tổng quan Hoạt động Kinh doanh")
        self.assertContains(res, "Đơn đặt áo")

        # 3. Can access orders and products management
        res_orders = self.client.get('/quan-tri/don-hang/')
        self.assertEqual(res_orders.status_code, 200)
        self.assertContains(res_orders, "Quản lý Đơn hàng Khách Đặt")

        res_products = self.client.get('/quan-tri/san-pham/')
        self.assertEqual(res_products.status_code, 200)
        self.assertContains(res_products, "Danh mục phôi áo xưởng Nếp")

    def test_form_and_size_selection_flow(self):
        # Create an Oversize product type and product
        pt_oversize, _ = ProductType.objects.get_or_create(slug="ao-thun-oversize", defaults={"name": "Áo thun Oversize"})
        prod_oversize, _ = Product.objects.get_or_create(
            slug="ao-thun-oversize",
            defaults={
                "product_type": pt_oversize,
                "name": "Áo thun Oversize",
                "base_price": Decimal("295000"),
                "fit_type": "Streetwear oversize",
                "is_active": True
            }
        )
        size_xl, _ = Size.objects.get_or_create(name="XL", defaults={"display_order": 4})
        variant_xl, _ = ProductVariant.objects.get_or_create(
            product=prod_oversize,
            color=self.color,
            size=size_xl,
            defaults={"stock_quantity": 30}
        )

        # Studio page should contain both forms in forms_json
        res = self.client.get('/studio/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Áo thun Oversize")
        self.assertContains(res, "ao-thun-oversize")

        # Add to cart with Oversize form and size XL
        payload = {
            'product_id': prod_oversize.id,
            'color_id': self.color.id,
            'size_id': size_xl.id,
            'quantity': 1,
            'print_zone_front_id': self.print_zone.id
        }
        res_add = self.client.post('/gio-hang/api/add/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res_add.status_code, 200)
        self.assertEqual(res_add.json()['status'], 'success')

        # Check cart detail displays Oversize and size XL
        res_cart = self.client.get('/gio-hang/')
        self.assertEqual(res_cart.status_code, 200)
        self.assertContains(res_cart, "Áo thun Oversize")
        self.assertContains(res_cart, "Size: <strong class=\"text-nep-dark\">XL</strong>")

    def test_realistic_mockups_assets_and_studio_integration(self):
        import os
        from django.conf import settings

        mockup_base = os.path.join(settings.BASE_DIR, 'static', 'images', 'mockups')
        form_slugs = ['ao-thun-oversize', 'ao-custom-classic', 'ao-polo-pique', 'ao-hoodie-nep', 'ao-dai-tay-nep']
        color_slugs = ['kem', 'trang', 'den', 'xanh_reu', 'xam_tieu']
        sides = ['front', 'back']

        for f in form_slugs:
            for c in color_slugs:
                for s in sides:
                    file_path = os.path.join(mockup_base, f, f"{s}_{c}.png")
                    self.assertTrue(os.path.exists(file_path), f"Missing mockup file: {file_path}")

        # Check studio template has mockup helpers
        res = self.client.get('/studio/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "getMockupImage")
        self.assertContains(res, "getZoneTop")
        self.assertContains(res, "preloadMockups")

