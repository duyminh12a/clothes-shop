import os
import sys
from PIL import Image, ImageFilter, ImageOps
from collections import deque

BASE_DIR = r'C:/Users/Admin/.gemini/antigravity/scratch/nep-form'
UPLOAD_DIR = r'C:/Users/Admin/.gemini/antigravity/brain/1f074714-ef18-4d32-9b36-7b68df54996d/.user_uploaded'
OUTPUT_DIR = os.path.join(BASE_DIR, 'static/images/mockups')

COLORS = {
    'kem': (245, 240, 232),
    'trang': (255, 255, 255),
    'den': (28, 28, 28),
    'xanh_reu': (94, 110, 73),
    'xam_tieu': (157, 157, 157)
}

TARGET_W, TARGET_H = 540, 620

def place_in_frame(img, target_w=TARGET_W, target_h=TARGET_H, y_offset=20):
    w, h = img.size
    scale = min((target_w - 40) / w, (target_h - 50) / h)
    new_w, new_h = int(w * scale), int(h * scale)
    scaled = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    frame = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))
    x = (target_w - new_w) // 2
    y = y_offset + (target_h - 40 - new_h) // 2
    frame.paste(scaled, (x, y), scaled)
    return frame

def multiply_color(white_img, rgb_color):
    w, h = white_img.size
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    out_pix = out.load()
    w_pix = white_img.load()
    cr, cg, cb = rgb_color
    
    for x in range(w):
        for y in range(h):
            wr, wg, wb, wa = w_pix[x, y]
            if wa > 0:
                nr = int(wr * (cr / 255.0))
                ng = int(wg * (cg / 255.0))
                nb = int(wb * (cb / 255.0))
                out_pix[x, y] = (nr, ng, nb, wa)
    return out

def invert_to_dark(white_img, target_dark_val=30):
    w, h = white_img.size
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    out_pix = out.load()
    w_pix = white_img.load()
    
    for x in range(w):
        for y in range(h):
            wr, wg, wb, wa = w_pix[x, y]
            if wa > 0:
                diff = (wr - 238)
                val = int(target_dark_val + diff * 0.7)
                val = max(12, min(80, val))
                out_pix[x, y] = (val, val, val, wa)
    return out

def bfs_extract_mask(crop, is_bg_fn, blur_radius=0.7):
    w, h = crop.size
    gray = crop.convert('L')
    pixels = gray.load()
    
    is_bg = [[is_bg_fn(pixels[x, y], x, y) for y in range(h)] for x in range(w)]
    visited = [[False for y in range(h)] for x in range(w)]
    
    q = deque([(x, 0) for x in range(w) if is_bg[x][0]] + 
              [(x, h-1) for x in range(w) if is_bg[x][h-1]] + 
              [(0, y) for y in range(h) if is_bg[0][y]] + 
              [(w-1, y) for y in range(h) if is_bg[w-1][y]])
    for x, y in q: visited[x][y] = True
    
    while q:
        cx, cy = q.popleft()
        for nx, ny in [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)]:
            if 0 <= nx < w and 0 <= ny < h and not visited[nx][ny] and is_bg[nx][ny]:
                visited[nx][ny] = True
                q.append((nx, ny))
                
    raw_mask = Image.new('L', (w, h), 0)
    rm_pix = raw_mask.load()
    for x in range(w):
        for y in range(h):
            if not visited[x][y]:
                rm_pix[x, y] = 255
                
    smooth_mask = raw_mask.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    return smooth_mask, pixels

def save_variant_set(out_dir, side, white_base, black_base):
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Trang
    white_frame = place_in_frame(white_base)
    white_frame.save(os.path.join(out_dir, f'{side}_trang.png'), optimize=True)
    
    # 2. Den
    black_frame = place_in_frame(black_base)
    black_frame.save(os.path.join(out_dir, f'{side}_den.png'), optimize=True)
    
    # 3. Kem, Xanh reu, Xam tieu
    for c_slug in ['kem', 'xanh_reu', 'xam_tieu']:
        col_img = multiply_color(white_base, COLORS[c_slug])
        col_frame = place_in_frame(col_img)
        col_frame.save(os.path.join(out_dir, f'{side}_{c_slug}.png'), optimize=True)
    print(f'Successfully saved 5 colors for {os.path.basename(out_dir)} [{side}]')


# ========================================================
# 1. GENERATE AO THUN OVERSIZE (from image 3)
# ========================================================
def generate_oversize_and_classic():
    img_path = os.path.join(UPLOAD_DIR, 'media_1792432526148_b3cb336f.png')
    im = Image.open(img_path)
    
    # --- Front ---
    f_crop = im.crop((0, 0, 500, im.height))
    f_mask, f_pix = bfs_extract_mask(f_crop, lambda p, x, y: p > 180)
    
    # Black base
    f_black = Image.new('RGBA', f_crop.size, (0, 0, 0, 0))
    f_black.paste(f_crop.convert('RGBA'), (0, 0), f_mask)
    f_bbox = f_black.getbbox()
    f_black = f_black.crop((f_bbox[0]-10, f_bbox[1]-10, f_bbox[2]+10, f_bbox[3]+10))
    
    # White base
    f_white = Image.new('RGBA', f_crop.size, (0, 0, 0, 0))
    w_pix = f_white.load()
    sm_pix = f_mask.load()
    w, h = f_crop.size
    for x in range(w):
        for y in range(h):
            a = sm_pix[x, y]
            if a > 0:
                v = f_pix[x, y]
                diff = (v - 32)
                val = int(238 + diff * 1.4)
                val = max(160, min(255, val))
                w_pix[x, y] = (val, val, val, a)
    f_white = f_white.crop((f_bbox[0]-10, f_bbox[1]-10, f_bbox[2]+10, f_bbox[3]+10))
    
    # --- Back ---
    b_crop = im.crop((500, 0, 1000, im.height))
    b_mask, b_pix = bfs_extract_mask(b_crop, lambda p, x, y: p > 180)
    
    b_black = Image.new('RGBA', b_crop.size, (0, 0, 0, 0))
    b_black.paste(b_crop.convert('RGBA'), (0, 0), b_mask)
    b_bbox = b_black.getbbox()
    b_black = b_black.crop((b_bbox[0]-10, b_bbox[1]-10, b_bbox[2]+10, b_bbox[3]+10))
    
    b_white = Image.new('RGBA', b_crop.size, (0, 0, 0, 0))
    bw_pix = b_white.load()
    sm_b_pix = b_mask.load()
    bw, bh = b_crop.size
    for x in range(bw):
        for y in range(bh):
            a = sm_b_pix[x, y]
            if a > 0:
                v = b_pix[x, y]
                diff = (v - 32)
                val = int(238 + diff * 1.4)
                val = max(160, min(255, val))
                bw_pix[x, y] = (val, val, val, a)
    b_white = b_white.crop((b_bbox[0]-10, b_bbox[1]-10, b_bbox[2]+10, b_bbox[3]+10))
    
    # Save Oversize
    out_dir_os = os.path.join(OUTPUT_DIR, 'ao-thun-oversize')
    save_variant_set(out_dir_os, 'front', f_white, f_black)
    save_variant_set(out_dir_os, 'back', b_white, b_black)
    
    # Save Classic (proportional trim for regular fit)
    out_dir_cl = os.path.join(OUTPUT_DIR, 'ao-custom-classic')
    # Classic is slightly regular-fit width
    cw_f_white = f_white.resize((int(f_white.width * 0.94), f_white.height), Image.Resampling.LANCZOS)
    cw_f_black = f_black.resize((int(f_black.width * 0.94), f_black.height), Image.Resampling.LANCZOS)
    cw_b_white = b_white.resize((int(b_white.width * 0.94), b_white.height), Image.Resampling.LANCZOS)
    cw_b_black = b_black.resize((int(b_black.width * 0.94), b_black.height), Image.Resampling.LANCZOS)
    save_variant_set(out_dir_cl, 'front', cw_f_white, cw_f_black)
    save_variant_set(out_dir_cl, 'back', cw_b_white, cw_b_black)


# ========================================================
# 2. GENERATE AO HOODIE NEP (from images 1 & 2)
# ========================================================
def generate_hoodie():
    im_w_path = os.path.join(UPLOAD_DIR, 'media_1792432377820_e889491c.png')
    im_b_path = os.path.join(UPLOAD_DIR, 'media_1792432422433_0b191c5e.png')
    im_w = Image.open(im_w_path)
    im_b = Image.open(im_b_path)
    w, h = im_w.size
    
    # --- Front Hoodie ---
    # Clear back hood from front crop
    f_crop_w = im_w.copy()
    f_pix_w = f_crop_w.load()
    f_crop_b = im_b.copy()
    f_pix_b = f_crop_b.load()
    
    for y in range(473, h):
        for x in range(140, 436):
            f_pix_w[x, y] = (255, 255, 255, 255)
            f_pix_b[x, y] = (255, 255, 255, 255)
    for y in range(515, h):
        for x in range(w):
            f_pix_w[x, y] = (255, 255, 255, 255)
            f_pix_b[x, y] = (255, 255, 255, 255)
            
    f_crop_w = f_crop_w.crop((0, 0, w, 515))
    f_crop_b = f_crop_b.crop((0, 0, w, 515))
    
    # White front mask
    f_mask_w, _ = bfs_extract_mask(f_crop_w, lambda p, x, y: p >= 253)
    f_hoodie_w = Image.new('RGBA', f_crop_w.size, (0, 0, 0, 0))
    f_hoodie_w.paste(f_crop_w.convert('RGBA'), (0, 0), f_mask_w)
    f_box = f_hoodie_w.getbbox()
    f_hoodie_w = f_hoodie_w.crop((f_box[0]-10, f_box[1]-10, f_box[2]+10, f_box[3]+10))
    
    # Black front mask
    f_mask_b, _ = bfs_extract_mask(f_crop_b, lambda p, x, y: p >= 180)
    f_hoodie_b = Image.new('RGBA', f_crop_b.size, (0, 0, 0, 0))
    f_hoodie_b.paste(f_crop_b.convert('RGBA'), (0, 0), f_mask_b)
    f_hoodie_b = f_hoodie_b.crop((f_box[0]-10, f_box[1]-10, f_box[2]+10, f_box[3]+10))
    
    # --- Back Hoodie ---
    b_crop_w = im_w.crop((0, 489, w, h))
    bw_pix = b_crop_w.load()
    b_crop_b = im_b.crop((0, 489, w, h))
    bb_pix = b_crop_b.load()
    bw_w, bw_h = b_crop_w.size
    for y in range(25):
        for x in range(bw_w):
            if x < 150 or x > 420:
                bw_pix[x, y] = (255, 255, 255, 255)
                bb_pix[x, y] = (255, 255, 255, 255)
                
    b_mask_w, _ = bfs_extract_mask(b_crop_w, lambda p, x, y: p >= 253)
    b_hoodie_w = Image.new('RGBA', b_crop_w.size, (0, 0, 0, 0))
    b_hoodie_w.paste(b_crop_w.convert('RGBA'), (0, 0), b_mask_w)
    b_box = b_hoodie_w.getbbox()
    b_hoodie_w = b_hoodie_w.crop((b_box[0]-10, b_box[1]-10, b_box[2]+10, b_box[3]+10))
    
    b_mask_b, _ = bfs_extract_mask(b_crop_b, lambda p, x, y: p >= 180)
    b_hoodie_b = Image.new('RGBA', b_crop_b.size, (0, 0, 0, 0))
    b_hoodie_b.paste(b_crop_b.convert('RGBA'), (0, 0), b_mask_b)
    b_hoodie_b = b_hoodie_b.crop((b_box[0]-10, b_box[1]-10, b_box[2]+10, b_box[3]+10))
    
    out_dir = os.path.join(OUTPUT_DIR, 'ao-hoodie-nep')
    save_variant_set(out_dir, 'front', f_hoodie_w, f_hoodie_b)
    save_variant_set(out_dir, 'back', b_hoodie_w, b_hoodie_b)


# ========================================================
# 3. GENERATE AO POLO PIQUE (from image 4)
# ========================================================
def generate_polo():
    img_path = os.path.join(UPLOAD_DIR, 'media_1792432632442_d6718ca6.png')
    im = Image.open(img_path)
    
    # Left: Front, Right: Back
    f_crop = im.crop((0, 0, 365, im.height))
    f_mask, f_pix = bfs_extract_mask(f_crop, lambda p, x, y: p >= 240)
    
    f_black = Image.new('RGBA', f_crop.size, (0, 0, 0, 0))
    f_black.paste(f_crop.convert('RGBA'), (0, 0), f_mask)
    f_bbox = f_black.getbbox()
    f_black = f_black.crop((f_bbox[0]-10, f_bbox[1]-10, f_bbox[2]+10, f_bbox[3]+10))
    
    # White base
    f_white = Image.new('RGBA', f_crop.size, (0, 0, 0, 0))
    w_pix = f_white.load()
    sm_pix = f_mask.load()
    w, h = f_crop.size
    # Median on garment
    g_vals = sorted([f_pix[x, y] for x in range(w) for y in range(h) if sm_pix[x, y] > 128])
    med = g_vals[len(g_vals)//2]
    
    for x in range(w):
        for y in range(h):
            a = sm_pix[x, y]
            if a > 0:
                v = f_pix[x, y]
                diff = (v - med)
                val = int(238 + diff * 1.5)
                val = max(150, min(255, val))
                w_pix[x, y] = (val, val, val, a)
    f_white = f_white.crop((f_bbox[0]-10, f_bbox[1]-10, f_bbox[2]+10, f_bbox[3]+10))
    
    # Back
    b_crop = im.crop((365, 0, im.width, im.height))
    b_mask, b_pix = bfs_extract_mask(b_crop, lambda p, x, y: p >= 240)
    
    b_black = Image.new('RGBA', b_crop.size, (0, 0, 0, 0))
    b_black.paste(b_crop.convert('RGBA'), (0, 0), b_mask)
    b_bbox = b_black.getbbox()
    b_black = b_black.crop((b_bbox[0]-10, b_bbox[1]-10, b_bbox[2]+10, b_bbox[3]+10))
    
    b_white = Image.new('RGBA', b_crop.size, (0, 0, 0, 0))
    bw_pix = b_white.load()
    sm_b_pix = b_mask.load()
    bw, bh = b_crop.size
    g_vals_b = sorted([b_pix[x, y] for x in range(bw) for y in range(bh) if sm_b_pix[x, y] > 128])
    med_b = g_vals_b[len(g_vals_b)//2]
    for x in range(bw):
        for y in range(bh):
            a = sm_b_pix[x, y]
            if a > 0:
                v = b_pix[x, y]
                diff = (v - med_b)
                val = int(238 + diff * 1.5)
                val = max(150, min(255, val))
                bw_pix[x, y] = (val, val, val, a)
    b_white = b_white.crop((b_bbox[0]-10, b_bbox[1]-10, b_bbox[2]+10, b_bbox[3]+10))
    
    out_dir = os.path.join(OUTPUT_DIR, 'ao-polo-pique')
    save_variant_set(out_dir, 'front', f_white, f_black)
    save_variant_set(out_dir, 'back', b_white, b_black)


# ========================================================
# 4. GENERATE AO DAI TAY NEP (from image 5)
# ========================================================
def generate_longsleeve():
    img_path = os.path.join(UPLOAD_DIR, 'media_1792432651329_b92174e5.png')
    im = Image.open(img_path)
    
    f_crop = im.crop((45, 55, 535, 470))
    f_mask, _ = bfs_extract_mask(f_crop, lambda p, x, y: p >= 253)
    # Clean speckles
    f_mask = f_mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.7))
    
    f_white = Image.new('RGBA', f_crop.size, (0, 0, 0, 0))
    f_white.paste(f_crop.convert('RGBA'), (0, 0), f_mask)
    f_bbox = f_white.getbbox()
    f_white = f_white.crop((f_bbox[0]-10, f_bbox[1]-10, f_bbox[2]+10, f_bbox[3]+10))
    f_black = invert_to_dark(f_white)
    
    b_crop = im.crop((45, 495, 535, 945))
    b_mask, _ = bfs_extract_mask(b_crop, lambda p, x, y: p >= 253)
    b_mask = b_mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.7))
    
    b_white = Image.new('RGBA', b_crop.size, (0, 0, 0, 0))
    b_white.paste(b_crop.convert('RGBA'), (0, 0), b_mask)
    b_bbox = b_white.getbbox()
    b_white = b_white.crop((b_bbox[0]-10, b_bbox[1]-10, b_bbox[2]+10, b_bbox[3]+10))
    b_black = invert_to_dark(b_white)
    
    out_dir = os.path.join(OUTPUT_DIR, 'ao-dai-tay-nep')
    save_variant_set(out_dir, 'front', f_white, f_black)
    save_variant_set(out_dir, 'back', b_white, b_black)


if __name__ == '__main__':
    print('Starting full realistic mockups generation...')
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generate_oversize_and_classic()
    generate_hoodie()
    generate_polo()
    generate_longsleeve()
    print('ALL REALISTIC MOCKUPS GENERATED SUCCESSFULLY!')
