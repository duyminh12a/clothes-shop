import os
import sys
import django

# Set UTF-8 encoding for standard output
sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
django.setup()

from products.models import Product, ProductType, Color, Size, ProductVariant

product_types_data = [
    {'name': 'Áo thun', 'slug': 'ao-thun', 'order': 1},
    {'name': 'Sơ mi', 'slug': 'so-mi', 'order': 2},
    {'name': 'Hoodie', 'slug': 'hoodie', 'order': 3},
    {'name': 'Áo khoác', 'slug': 'ao-khoac', 'order': 4},
    {'name': 'Quần dài', 'slug': 'quan-dai', 'order': 5},
    {'name': 'Quần short', 'slug': 'quan-short', 'order': 6},
]

type_map = {}
for pt_data in product_types_data:
    pt, _ = ProductType.objects.get_or_create(
        slug=pt_data['slug'],
        defaults={'name': pt_data['name'], 'display_order': pt_data['order'], 'is_active': True}
    )
    type_map[pt_data['slug']] = pt

items = [
    {
        'type_slug': 'ao-thun',
        'name': 'Áo thun kem cổ tròn',
        'slug': 'ao-thun-kem-co-tron',
        'price': 199000,
        'badge': '',
        'color_hex': '#F5EFEB',
        'fabric': '100% Cotton 220gsm đanh mịn',
        'fit': 'Regular fit unisex',
    },
    {
        'type_slug': 'ao-thun',
        'name': 'Áo thun đen basic',
        'slug': 'ao-thun-den-basic',
        'price': 219000,
        'badge': '',
        'color_hex': '#1E1E1E',
        'fabric': '100% Cotton 240gsm đứng phom',
        'fit': 'Regular fit unisex',
    },
    {
        'type_slug': 'so-mi',
        'name': 'Sơ mi kem tay ngắn',
        'slug': 'so-mi-kem-tay-ngan',
        'price': 349000,
        'badge': '',
        'color_hex': '#F5EFEB',
        'fabric': 'Linen pha cotton tự nhiên thoáng khí',
        'fit': 'Boxy phom rộng',
    },
    {
        'type_slug': 'hoodie',
        'name': 'Hoodie be vai rơi',
        'slug': 'hoodie-be-vai-roi',
        'price': 479000,
        'badge': '',
        'color_hex': '#EBE6DD',
        'fabric': 'Chân cua nỉ bông 380gsm giữ ấm',
        'fit': 'Oversize vai trễ',
    },
    {
        'type_slug': 'ao-khoac',
        'name': 'Áo khoác denim chàm',
        'slug': 'ao-khoac-denim-cham',
        'price': 599000,
        'badge': 'Mới',
        'color_hex': '#3B506D',
        'fabric': 'Denim thô dệt chéo 12oz phong cách vintage',
        'fit': 'Loose fit jacket',
    },
    {
        'type_slug': 'quan-dai',
        'name': 'Quần dài olive ống rộng',
        'slug': 'quan-dai-olive-ong-rong',
        'price': 429000,
        'badge': 'Mới',
        'color_hex': '#556044',
        'fabric': 'Kaki cotton dày dặn đứng phom',
        'fit': 'Wide-leg ống suông',
    },
    {
        'type_slug': 'quan-short',
        'name': 'Quần short be dây rút',
        'slug': 'quan-short-be-day-rut',
        'price': 279000,
        'badge': 'Mới',
        'color_hex': '#E2DDD2',
        'fabric': 'Đũi lạnh thoáng nhẹ',
        'fit': 'Cạp chun dây rút tiện lợi',
    },
    {
        'type_slug': 'ao-khoac',
        'name': 'Áo khoác đen khóa kéo',
        'slug': 'ao-khoac-den-khoa-keo',
        'price': 549000,
        'badge': 'Mới',
        'color_hex': '#1E1E1E',
        'fabric': 'Gió dù 2 lớp chống gió cản nước nhẹ',
        'fit': 'Zip jacket thể thao',
    },
]

for it in items:
    pt = type_map[it['type_slug']]
    prod, created = Product.objects.update_or_create(
        slug=it['slug'],
        defaults={
            'product_type': pt,
            'name': it['name'],
            'base_price': it['price'],
            'badge': it['badge'],
            'color_hex': it['color_hex'],
            'thumbnail_url': f"/static/images/products/{it['slug']}.png",
            'fabric_info': it['fabric'],
            'fit_type': it['fit'],
            'is_featured': True,
            'is_active': True,
        }
    )
    status_text = "Created" if created else "Updated"
    print(f"{status_text}: {prod.name} ({prod.base_price:,.0f}₫) - Badge: {prod.badge}")

print("All 8 products seeded successfully!")
