import os
import sys
import urllib.request
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\Admin\.gemini\antigravity\scratch\nep-form"
static_prod_dir = os.path.join(BASE_DIR, "static", "images", "products")
staticfiles_prod_dir = os.path.join(BASE_DIR, "staticfiles", "images", "products")
os.makedirs(static_prod_dir, exist_ok=True)
os.makedirs(staticfiles_prod_dir, exist_ok=True)

products_data = [
    # 1. Áo thun
    {
        'slug': 'ao-thun-heavyweight-trang',
        'type_slug': 'ao-thun',
        'type_name': 'Áo thun',
        'name': 'Áo thun Heavyweight 100% Cotton',
        'price': 219000,
        'badge': 'Best-seller',
        'color_name': 'Trắng',
        'color_hex': '#FFFFFF',
        'fabric': '100% Cotton 240gsm đanh mịn không xù',
        'fit': 'Regular fit chuẩn form',
        'img_url': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=85',
    },
    {
        'slug': 'ao-thun-oversize-kem',
        'type_slug': 'ao-thun',
        'type_name': 'Áo thun',
        'name': 'Áo thun Oversize vai trễ màu Kem',
        'price': 249000,
        'badge': 'Mới',
        'color_name': 'Kem',
        'color_hex': '#F5F0E8',
        'fabric': 'Cotton hữu cơ tự nhiên 250gsm',
        'fit': 'Oversize rộng rãi thoải mái',
        'img_url': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=85',
    },
    {
        'slug': 'ao-thun-cotton-den',
        'type_slug': 'ao-thun',
        'type_name': 'Áo thun',
        'name': 'Áo thun Cotton compact đen basic',
        'price': 199000,
        'badge': 'Hot',
        'color_name': 'Đen',
        'color_hex': '#1C1C1C',
        'fabric': 'Cotton 100% định lượng 220gsm',
        'fit': 'Standard unisex fit',
        'img_url': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=85',
    },
    {
        'slug': 'ao-thun-washed-vintage',
        'type_slug': 'ao-thun',
        'type_name': 'Áo thun',
        'name': 'Áo thun Washed Vintage xám tiêu',
        'price': 269000,
        'badge': 'Mới',
        'color_name': 'Xám tiêu',
        'color_hex': '#8E8E93',
        'fabric': 'Cotton wash axit nhẹ tạo hiệu ứng retro',
        'fit': 'Boxy phom vuông hiện đại',
        'img_url': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&auto=format&fit=crop&q=85',
    },
    {
        'slug': 'ao-thun-minimal-earth',
        'type_slug': 'ao-thun',
        'type_name': 'Áo thun',
        'name': 'Áo thun Minimal Earth xanh rêu',
        'price': 229000,
        'badge': '',
        'color_name': 'Xanh rêu',
        'color_hex': '#5E6E49',
        'fabric': 'Cotton dệt kim đơn 230gsm',
        'fit': 'Regular fit unisex',
        'img_url': 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800&auto=format&fit=crop&q=85',
    },

    # 2. Áo Polo
    {
        'slug': 'ao-polo-pique-trang',
        'type_slug': 'ao-polo',
        'type_name': 'Áo Polo',
        'name': 'Áo Polo Pique dệt mắt chim cao cấp',
        'price': 299000,
        'badge': 'Hot',
        'color_name': 'Trắng sữa',
        'color_hex': '#FAF8F5',
        'fabric': 'Pique cá sấu cotton 100% thoáng mát',
        'fit': 'Slim-regular lịch sự',
        'img_url': 'https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=800&auto=format&fit=crop&q=85',
    },
    {
        'slug': 'ao-polo-zip-den',
        'type_slug': 'ao-polo',
        'type_name': 'Áo Polo',
        'name': 'Áo Polo Zip cộc tay không cúc',
        'price': 329000,
        'badge': 'Mới',
        'color_name': 'Đen',
        'color_hex': '#1C1C1C',
        'fabric': 'Cotton lụa co giãn 4 chiều mềm mịn',
        'fit': 'Modern boxy fit',
        'img_url': 'https://images.unsplash.com/photo-1586363104862-3a5e2ab60d99?w=800&auto=format&fit=crop&q=85',
    },
    {
        'slug': 'ao-polo-form-rong-be',
        'type_slug': 'ao-polo',
        'type_name': 'Áo Polo',
        'name': 'Áo Polo Boxy dệt sợi tự nhiên',
        'price': 319000,
        'badge': '',
        'color_name': 'Be cát',
        'color_hex': '#E6DFD5',
        'fabric': 'Sợi bông tự nhiên đan dệt kim',
        'fit': 'Boxy vai rơi trẻ trung',
        'img_url': 'https://images.unsplash.com/photo-1626497764746-6dc36546b388?w=800&auto=format&fit=crop&q=85',
    },

    # 3. Áo Sơ mi
    {
        'slug': 'so-mi-linen-tay-ngan',
        'type_slug': 'ao-so-mi',
        'type_name': 'Áo Sơ mi',
        'name': 'Sơ mi Linen tay ngắn cổ Cuba',
        'price': 349000,
        'badge': 'Best-seller',
        'color_name': 'Kem tự nhiên',
        'color_hex': '#F4EFE6',
        'fabric': '100% Linen tự nhiên dệt thưa thoáng mát',
        'fit': 'Cổ bẻ Cuba phóng khoáng',
        'img_url': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=800&auto=format&fit=crop&q=85',
    },
    {
        'slug': 'so-mi-oxford-xanh',
        'type_slug': 'ao-so-mi',
        'type_name': 'Áo Sơ mi',
        'name': 'Sơ mi Oxford Button-down dài tay',
        'price': 389000,
        'badge': '',
        'color_name': 'Xanh nhạt',
        'color_hex': '#C2D4E5',
        'fabric': 'Vải Oxford cotton dệt hạt gạo dày dặn',
        'fit': 'Regular tay dài cài cúc cổ',
        'img_url': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800&auto=format&fit=crop&q=85',
    },
    {
        'slug': 'so-mi-flannel-caro',
        'type_slug': 'ao-so-mi',
        'type_name': 'Áo Sơ mi',
        'name': 'Sơ mi Flannel caro sợi tự nhiên',
        'price': 399000,
        'badge': 'Mới',
        'color_name': 'Nâu be',
        'color_hex': '#8D7B68',
        'fabric': 'Dạ nỉ Flannel chải bông 2 mặt êm ái',
        'fit': 'Overshirt khoác ngoài thoải mái',
        'img_url': 'https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=800&auto=format&fit=crop&q=85',
    },

    # 4. Hoodie & Áo nỉ
    {
        'slug': 'hoodie-be-vai-roi',
        'type_slug': 'hoodie-ao-ni',
        'type_name': 'Hoodie & Áo nỉ',
        'name': 'Hoodie chân cua nỉ bông vai rơi',
        'price': 479000,
        'badge': 'Best-seller',
        'color_name': 'Be ấm',
        'color_hex': '#EADDCB',
        'fabric': 'Nỉ chân cua cotton 380gsm giữ ấm tối ưu',
        'fit': 'Oversize vai trễ nón 2 lớp dày dặn',
        'img_url': 'https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=800&auto=format&fit=crop&q=85',
    },
    {
        'slug': 'sweatshirt-xam-melange',
        'type_slug': 'hoodie-ao-ni',
        'type_name': 'Hoodie & Áo nỉ',
        'name': 'Sweatshirt cổ tròn nỉ da cá thêu nổi',
        'price': 399000,
        'badge': 'Hot',
        'color_name': 'Xám melange',
        'color_hex': '#A0A0A0',
        'fabric': 'Nỉ da cá chéo 350gsm co giãn nhẹ',
        'fit': 'Drop shoulder phong cách tối giản',
        'img_url': 'https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=800&auto=format&fit=crop&q=85',
    },
    {
        'slug': 'hoodie-zip-den',
        'type_slug': 'hoodie-ao-ni',
        'type_name': 'Hoodie & Áo nỉ',
        'name': 'Hoodie Zip 2 chiều dáng rộng',
        'price': 499000,
        'badge': 'Mới',
        'color_name': 'Đen mờ',
        'color_hex': '#1A1A1A',
        'fabric': 'Cotton terry dệt dày dặn chống xù',
        'fit': 'Khoá kéo 2 chiều kim loại mạ mờ',
        'img_url': 'https://images.unsplash.com/photo-1509967419530-da38b4704bc6?w=800&auto=format&fit=crop&q=85',
    },

    # 5. Áo khoác
    {
        'slug': 'ao-khoac-denim-cham',
        'type_slug': 'ao-khoac',
        'type_name': 'Áo khoác',
        'name': 'Áo khoác Denim chàm dệt thô vintage',
        'price': 599000,
        'badge': 'Mới',
        'color_name': 'Xanh chàm',
        'color_hex': '#3B506D',
        'fabric': 'Denim cotton 100% 12.5oz dệt thô chéo',
        'fit': 'Trucker jacket phom boxy',
        'img_url': 'https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=800&auto=format&fit=crop&q=85',
    },
    {
        'slug': 'ao-khoac-gio-den',
        'type_slug': 'ao-khoac',
        'type_name': 'Áo khoác',
        'name': 'Áo khoác Gió dù 2 lớp chống nước nhẹ',
        'price': 549000,
        'badge': 'Hot',
        'color_name': 'Đen',
        'color_hex': '#1C1C1C',
        'fabric': 'Vải dù poly-nylon cản gió và chống nước trượt',
        'fit': 'Form đứng dây rút điều chỉnh gấu áo',
        'img_url': 'https://images.unsplash.com/photo-1544441893-675973e31985?w=800&auto=format&fit=crop&q=85',
    },
    {
        'slug': 'ao-khoac-kaki-chore',
        'type_slug': 'ao-khoac',
        'type_name': 'Áo khoác',
        'name': 'Áo khoác Kaki Chore jacket túi hộp',
        'price': 629000,
        'badge': 'Mới',
        'color_name': 'Olive',
        'color_hex': '#4B5320',
        'fabric': 'Kaki cotton dệt chéo bề mặt ráp phong trần',
        'fit': 'Chore jacket 4 túi hộp phong cách thợ mộc',
        'img_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&auto=format&fit=crop&q=85',
    },
    {
        'slug': 'cardigan-det-kim',
        'type_slug': 'ao-khoac',
        'type_name': 'Áo khoác',
        'name': 'Áo Cardigan dệt kim len mềm thư thái',
        'price': 469000,
        'badge': '',
        'color_name': 'Kem be',
        'color_hex': '#F2ECE4',
        'fabric': 'Len acrylic pha cotton mềm mịn không ngứa',
        'fit': 'Dáng suông cài cúc gừng phong cách vintage',
        'img_url': 'https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=800&auto=format&fit=crop&q=85',
    },

    # 6. Quần & Short
    {
        'slug': 'quan-kaki-ong-rong-olive',
        'type_slug': 'quan-short',
        'type_name': 'Quần & Short',
        'name': 'Quần Kaki ống rộng Wide-leg',
        'price': 429000,
        'badge': 'Mới',
        'color_name': 'Olive',
        'color_hex': '#556044',
        'fabric': 'Kaki cotton đanh dày đứng dáng',
        'fit': 'Wide-leg ống suông phủ gót',
        'img_url': 'https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=800&auto=format&fit=crop&q=85',
    },
    {
        'slug': 'quan-tay-xep-ly-den',
        'type_slug': 'quan-short',
        'type_name': 'Quần & Short',
        'name': 'Quần Tây xếp ly dáng suông Relaxed',
        'price': 459000,
        'badge': 'Hot',
        'color_name': 'Đen',
        'color_hex': '#1C1C1C',
        'fabric': 'Tuyết mưa Hàn Quốc rũ phẳng không nhăn',
        'fit': 'Xếp 2 ly trước, cạp cao tôn dáng',
        'img_url': 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=800&auto=format&fit=crop&q=85',
    },
    {
        'slug': 'quan-short-dui-be',
        'type_slug': 'quan-short',
        'type_name': 'Quần & Short',
        'name': 'Quần Short đũi cạp chun dây rút',
        'price': 279000,
        'badge': 'Best-seller',
        'color_name': 'Be cát',
        'color_hex': '#E2DDD2',
        'fabric': 'Đũi lạnh xước tự nhiên thoáng mát hè',
        'fit': 'Cạp thun co giãn dây rút kim loại',
        'img_url': 'https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=800&auto=format&fit=crop&q=85',
    },
    {
        'slug': 'quan-short-kaki-reu',
        'type_slug': 'quan-short',
        'type_name': 'Quần & Short',
        'name': 'Quần Short Kaki Bermuda túi nghiêng',
        'price': 299000,
        'badge': '',
        'color_name': 'Xanh rêu',
        'color_hex': '#4A5B3D',
        'fabric': 'Kaki wash mềm thoải mái vận động',
        'fit': 'Chiều dài trên gối 3cm chuẩn mực',
        'img_url': 'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=800&auto=format&fit=crop&q=85',
    },
]

print(f"Downloading and optimizing {len(products_data)} apparel images...")

for idx, p in enumerate(products_data, 1):
    slug = p['slug']
    target_filename = f"{slug}.jpg"
    target_path = os.path.join(static_prod_dir, target_filename)
    target_sf_path = os.path.join(staticfiles_prod_dir, target_filename)
    
    print(f"[{idx}/{len(products_data)}] Fetching {p['name']}...")
    req = urllib.request.Request(p['img_url'], headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw_data = resp.read()
            temp_raw = os.path.join(static_prod_dir, f"temp_{slug}.jpg")
            with open(temp_raw, 'wb') as f:
                f.write(raw_data)
                
            # Process and crop to standardized 4:3 aspect ratio
            with Image.open(temp_raw) as img:
                img = img.convert('RGB')
                w, h = img.size
                
                # Center crop to 4:3
                target_ratio = 4.0 / 3.0
                curr_ratio = w / h
                if curr_ratio > target_ratio:
                    new_w = int(h * target_ratio)
                    offset = (w - new_w) // 2
                    img = img.crop((offset, 0, offset + new_w, h))
                else:
                    new_h = int(w / target_ratio)
                    offset = (h - new_h) // 2
                    img = img.crop((0, offset, w, offset + new_h))
                    
                # Resize to standard 800x600 for sharp rendering on retina screens
                img = img.resize((800, 600), Image.Resampling.LANCZOS)
                img.save(target_path, 'JPEG', quality=88, optimize=True)
                img.save(target_sf_path, 'JPEG', quality=88, optimize=True)
                
            os.remove(temp_raw)
            print(f"    -> Saved {target_filename} (800x600)")
    except Exception as e:
        print(f"    -> Error downloading {slug}: {e}")

print("All apparel images downloaded and optimized successfully!")
