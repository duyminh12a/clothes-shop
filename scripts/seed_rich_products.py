import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
BASE_DIR = r"C:\Users\Admin\.gemini\antigravity\scratch\nep-form"
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
django.setup()

from products.models import Product, ProductType, Color, Size, ProductVariant

# 1. Mark existing studio form types
studio_slugs = ['ao-custom-classic', 'ao-thun-oversize', 'ao-polo-pique', 'ao-hoodie-nep', 'ao-dai-tay-nep', 'tui-canvas-tote']
for s in studio_slugs:
    ProductType.objects.filter(slug=s).update(is_studio_form=True)

# Deactivate dummy products under studio types so they don't pollute the catalog
Product.objects.filter(product_type__is_studio_form=True).update(is_active=False)

# 2. Setup clean clothing categories (is_studio_form=False)
categories = [
    {'slug': 'ao-thun', 'name': 'Áo thun', 'order': 1},
    {'slug': 'ao-polo', 'name': 'Áo Polo', 'order': 2},
    {'slug': 'ao-so-mi', 'name': 'Áo Sơ mi', 'order': 3},
    {'slug': 'hoodie-ao-ni', 'name': 'Hoodie & Áo nỉ', 'order': 4},
    {'slug': 'ao-khoac', 'name': 'Áo khoác', 'order': 5},
    {'slug': 'quan-short', 'name': 'Quần & Short', 'order': 6},
]

type_map = {}
for c in categories:
    pt, _ = ProductType.objects.get_or_create(
        slug=c['slug'],
        defaults={'name': c['name'], 'display_order': c['order'], 'is_studio_form': False, 'is_active': True}
    )
    pt.name = c['name']
    pt.display_order = c['order']
    pt.is_studio_form = False
    pt.is_active = True
    pt.save()
    type_map[c['slug']] = pt

# 3. Clean up any previous broken cropped products
# Delete old products not in our new collection
new_slugs = [
    'ao-thun-heavyweight-trang', 'ao-thun-oversize-kem', 'ao-thun-cotton-den',
    'ao-thun-washed-vintage', 'ao-thun-minimal-earth',
    'ao-polo-pique-trang', 'ao-polo-zip-den', 'ao-polo-form-rong-be',
    'so-mi-linen-tay-ngan', 'so-mi-oxford-xanh', 'so-mi-flannel-caro',
    'hoodie-be-vai-roi', 'sweatshirt-xam-melange', 'hoodie-zip-den',
    'ao-khoac-denim-cham', 'ao-khoac-gio-den', 'ao-khoac-kaki-chore', 'cardigan-det-kim',
    'quan-kaki-ong-rong-olive', 'quan-tay-xep-ly-den', 'quan-short-dui-be', 'quan-short-kaki-reu'
]

# Delete old non-studio products not in new list
Product.objects.filter(product_type__is_studio_form=False).exclude(slug__in=new_slugs).delete()

products_data = [
    # 1. Áo thun
    {
        'slug': 'ao-thun-heavyweight-trang',
        'type_slug': 'ao-thun',
        'name': 'Áo thun Heavyweight 100% Cotton',
        'price': 219000,
        'badge': 'Best-seller',
        'color_hex': '#FFFFFF',
        'fabric': '100% Cotton 240gsm đanh mịn không xù',
        'fit': 'Regular fit chuẩn form người Việt',
        'is_featured': True,
    },
    {
        'slug': 'ao-thun-oversize-kem',
        'type_slug': 'ao-thun',
        'name': 'Áo thun Oversize vai trễ màu Kem',
        'price': 249000,
        'badge': 'Mới',
        'color_hex': '#F5F0E8',
        'fabric': 'Cotton hữu cơ tự nhiên 250gsm dệt dày',
        'fit': 'Oversize rộng rãi thoải mái',
        'is_featured': True,
    },
    {
        'slug': 'ao-thun-cotton-den',
        'type_slug': 'ao-thun',
        'name': 'Áo thun Cotton compact đen basic',
        'price': 199000,
        'badge': 'Hot',
        'color_hex': '#1C1C1C',
        'fabric': 'Cotton 100% định lượng 220gsm',
        'fit': 'Standard unisex fit',
        'is_featured': True,
    },
    {
        'slug': 'ao-thun-washed-vintage',
        'type_slug': 'ao-thun',
        'name': 'Áo thun Washed Vintage xám tiêu',
        'price': 269000,
        'badge': 'Mới',
        'color_hex': '#8E8E93',
        'fabric': 'Cotton wash axit nhẹ tạo hiệu ứng retro',
        'fit': 'Boxy phom vuông hiện đại',
        'is_featured': True,
    },
    {
        'slug': 'ao-thun-minimal-earth',
        'type_slug': 'ao-thun',
        'name': 'Áo thun Minimal Earth xanh rêu',
        'price': 229000,
        'badge': '',
        'color_hex': '#5E6E49',
        'fabric': 'Cotton dệt kim đơn 230gsm',
        'fit': 'Regular fit unisex',
        'is_featured': False,
    },

    # 2. Áo Polo
    {
        'slug': 'ao-polo-pique-trang',
        'type_slug': 'ao-polo',
        'name': 'Áo Polo Pique dệt mắt chim cao cấp',
        'price': 299000,
        'badge': 'Hot',
        'color_hex': '#FAF8F5',
        'fabric': 'Pique cá sấu cotton 100% thoáng mát',
        'fit': 'Slim-regular lịch sự',
        'is_featured': True,
    },
    {
        'slug': 'ao-polo-zip-den',
        'type_slug': 'ao-polo',
        'name': 'Áo Polo Zip cộc tay không cúc',
        'price': 329000,
        'badge': 'Mới',
        'color_hex': '#1C1C1C',
        'fabric': 'Cotton lụa co giãn 4 chiều mềm mịn',
        'fit': 'Modern boxy fit',
        'is_featured': False,
    },
    {
        'slug': 'ao-polo-form-rong-be',
        'type_slug': 'ao-polo',
        'name': 'Áo Polo Boxy dệt sợi tự nhiên',
        'price': 319000,
        'badge': '',
        'color_hex': '#E6DFD5',
        'fabric': 'Sợi bông tự nhiên đan dệt kim',
        'fit': 'Boxy vai rơi trẻ trung',
        'is_featured': False,
    },

    # 3. Áo Sơ mi
    {
        'slug': 'so-mi-linen-tay-ngan',
        'type_slug': 'ao-so-mi',
        'name': 'Sơ mi Linen tay ngắn cổ Cuba',
        'price': 349000,
        'badge': 'Best-seller',
        'color_hex': '#F4EFE6',
        'fabric': '100% Linen tự nhiên dệt thưa thoáng mát',
        'fit': 'Cổ bẻ Cuba phóng khoáng',
        'is_featured': True,
    },
    {
        'slug': 'so-mi-oxford-xanh',
        'type_slug': 'ao-so-mi',
        'name': 'Sơ mi Oxford Button-down dài tay',
        'price': 389000,
        'badge': '',
        'color_hex': '#C2D4E5',
        'fabric': 'Vải Oxford cotton dệt hạt gạo dày dặn',
        'fit': 'Regular tay dài cài cúc cổ',
        'is_featured': False,
    },
    {
        'slug': 'so-mi-flannel-caro',
        'type_slug': 'ao-so-mi',
        'name': 'Sơ mi Flannel caro sợi tự nhiên',
        'price': 399000,
        'badge': 'Mới',
        'color_hex': '#8D7B68',
        'fabric': 'Dạ nỉ Flannel chải bông 2 mặt êm ái',
        'fit': 'Overshirt khoác ngoài thoải mái',
        'is_featured': False,
    },

    # 4. Hoodie & Áo nỉ
    {
        'slug': 'hoodie-be-vai-roi',
        'type_slug': 'hoodie-ao-ni',
        'name': 'Hoodie chân cua nỉ bông vai rơi',
        'price': 479000,
        'badge': 'Best-seller',
        'color_hex': '#EADDCB',
        'fabric': 'Nỉ chân cua cotton 380gsm giữ ấm tối ưu',
        'fit': 'Oversize vai trễ nón 2 lớp dày dặn',
        'is_featured': True,
    },
    {
        'slug': 'sweatshirt-xam-melange',
        'type_slug': 'hoodie-ao-ni',
        'name': 'Sweatshirt cổ tròn nỉ da cá thêu nổi',
        'price': 399000,
        'badge': 'Hot',
        'color_hex': '#A0A0A0',
        'fabric': 'Nỉ da cá chéo 350gsm co giãn nhẹ',
        'fit': 'Drop shoulder phong cách tối giản',
        'is_featured': False,
    },
    {
        'slug': 'hoodie-zip-den',
        'type_slug': 'hoodie-ao-ni',
        'name': 'Hoodie Zip 2 chiều dáng rộng',
        'price': 499000,
        'badge': 'Mới',
        'color_hex': '#1A1A1A',
        'fabric': 'Cotton terry dệt dày dặn chống xù',
        'fit': 'Khoá kéo 2 chiều kim loại mạ mờ',
        'is_featured': False,
    },

    # 5. Áo khoác
    {
        'slug': 'ao-khoac-denim-cham',
        'type_slug': 'ao-khoac',
        'name': 'Áo khoác Denim chàm dệt thô vintage',
        'price': 599000,
        'badge': 'Mới',
        'color_hex': '#3B506D',
        'fabric': 'Denim cotton 100% 12.5oz dệt thô chéo',
        'fit': 'Trucker jacket phom boxy',
        'is_featured': True,
    },
    {
        'slug': 'ao-khoac-gio-den',
        'type_slug': 'ao-khoac',
        'name': 'Áo khoác Gió dù 2 lớp chống nước nhẹ',
        'price': 549000,
        'badge': 'Hot',
        'color_hex': '#1C1C1C',
        'fabric': 'Vải dù poly-nylon cản gió và chống nước trượt',
        'fit': 'Form đứng dây rút điều chỉnh gấu áo',
        'is_featured': False,
    },
    {
        'slug': 'ao-khoac-kaki-chore',
        'type_slug': 'ao-khoac',
        'name': 'Áo khoác Kaki Chore jacket túi hộp',
        'price': 629000,
        'badge': 'Mới',
        'color_hex': '#4B5320',
        'fabric': 'Kaki cotton dệt chéo bề mặt ráp phong trần',
        'fit': 'Chore jacket 4 túi hộp phong cách thợ mộc',
        'is_featured': False,
    },
    {
        'slug': 'cardigan-det-kim',
        'type_slug': 'ao-khoac',
        'name': 'Áo Cardigan dệt kim len mềm thư thái',
        'price': 469000,
        'badge': '',
        'color_hex': '#F2ECE4',
        'fabric': 'Len acrylic pha cotton mềm mịn không ngứa',
        'fit': 'Dáng suông cài cúc gừng phong cách vintage',
        'is_featured': False,
    },

    # 6. Quần & Short
    {
        'slug': 'quan-kaki-ong-rong-olive',
        'type_slug': 'quan-short',
        'name': 'Quần Kaki ống rộng Wide-leg',
        'price': 429000,
        'badge': 'Mới',
        'color_hex': '#556044',
        'fabric': 'Kaki cotton đanh dày đứng dáng',
        'fit': 'Wide-leg ống suông phủ gót',
        'is_featured': False,
    },
    {
        'slug': 'quan-tay-xep-ly-den',
        'type_slug': 'quan-short',
        'name': 'Quần Tây xếp ly dáng suông Relaxed',
        'price': 459000,
        'badge': 'Hot',
        'color_hex': '#1C1C1C',
        'fabric': 'Tuyết mưa Hàn Quốc rũ phẳng không nhăn',
        'fit': 'Xếp 2 ly trước, cạp cao tôn dáng',
        'is_featured': False,
    },
    {
        'slug': 'quan-short-dui-be',
        'type_slug': 'quan-short',
        'name': 'Quần Short đũi cạp chun dây rút',
        'price': 279000,
        'badge': 'Best-seller',
        'color_hex': '#E2DDD2',
        'fabric': 'Đũi lạnh xước tự nhiên thoáng mát hè',
        'fit': 'Cạp thun co giãn dây rút kim loại',
        'is_featured': False,
    },
    {
        'slug': 'quan-short-kaki-reu',
        'type_slug': 'quan-short',
        'name': 'Quần Short Kaki Bermuda túi nghiêng',
        'price': 299000,
        'badge': '',
        'color_hex': '#4A5B3D',
        'fabric': 'Kaki wash mềm thoải mái vận động',
        'fit': 'Chiều dài trên gối 3cm chuẩn mực',
        'is_featured': False,
    },
]

for p in products_data:
    pt = type_map[p['type_slug']]
    prod, created = Product.objects.update_or_create(
        slug=p['slug'],
        defaults={
            'product_type': pt,
            'name': p['name'],
            'base_price': p['price'],
            'badge': p['badge'],
            'color_hex': p['color_hex'],
            'thumbnail_url': f"/static/images/products/{p['slug']}.jpg",
            'fabric_info': p['fabric'],
            'fit_type': p['fit'],
            'is_featured': p['is_featured'],
            'is_active': True,
        }
    )
    status = "Created" if created else "Updated"
    print(f"[{status}] {prod.name} ({prod.base_price:,.0f}đ) -> {prod.thumbnail_url}")

print(f"Total ready-to-wear products active: {Product.objects.filter(is_active=True).count()}")
