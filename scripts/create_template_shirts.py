import os
import math
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"C:\Users\Admin\.gemini\antigravity\scratch\nep-form"
out_dir = os.path.join(BASE_DIR, "static", "images", "templates")
os.makedirs(out_dir, exist_ok=True)

# 1. TEMPLATE 1: Clean im1 (uploaded screenshot) by clearing the top-right badge
im1_path = r"C:\Users\Admin\.gemini\antigravity\brain\1f074714-ef18-4d32-9b36-7b68df54996d\.user_uploaded\media_1792469051239_c1d361ac.png"
im1 = Image.open(im1_path).convert("RGBA")
w1, h1 = im1.size
draw1 = ImageDraw.Draw(im1)
bg_color = (238, 234, 225, 255)
# Clear badge at top right
draw1.rectangle([int(w1 * 0.6), 0, w1, 85], fill=bg_color)
t1_path = os.path.join(out_dir, "template_1_shirt.png")
im1.save(t1_path)
print(f"Saved {t1_path} ({w1}x{h1})")

# 2. Base canvas for Template 2 and 3:
# Load blank mockup front_kem.png
mockup = Image.open(os.path.join(BASE_DIR, "static", "images", "mockups", "ao-custom-classic", "front_kem.png")).convert("RGBA")
# Resize mockup to fit nicely in 502x557
mw, mh = mockup.size
target_w, target_h = 502, 557
scale = 0.88
new_mw = int(mw * scale)
new_mh = int(mh * scale)
mockup_resized = mockup.resize((new_mw, new_mh), Image.Resampling.LANCZOS)

# Create base shirt image
def create_base_shirt():
    shirt_img = Image.new("RGBA", (target_w, target_h), bg_color)
    offset_x = (target_w - new_mw) // 2
    offset_y = (target_h - new_mh) // 2 + 20
    shirt_img.paste(mockup_resized, (offset_x, offset_y), mockup_resized)
    return shirt_img

# Helper to draw dashed rectangle
def draw_dashed_rect(draw, rect, color, dash_len=4, gap_len=4):
    x0, y0, x1, y1 = rect
    # Top and bottom
    for x in range(x0, x1, dash_len + gap_len):
        draw.line([(x, y0), (min(x + dash_len, x1), y0)], fill=color, width=1)
        draw.line([(x, y1), (min(x + dash_len, x1), y1)], fill=color, width=1)
    # Left and right
    for y in range(y0, y1, dash_len + gap_len):
        draw.line([(x0, y), (x0, min(y + dash_len, y1))], fill=color, width=1)
        draw.line([(x1, y), (x1, min(y + dash_len, y1))], fill=color, width=1)

# Helper to draw active transform handles (blue box)
def draw_transform_handles(draw, x0, y0, x1, y1):
    blue = (59, 130, 246, 255)
    white = (255, 255, 255, 255)
    draw.rectangle([x0, y0, x1, y1], outline=blue, width=1)
    
    # Rotation stalk
    mid_x = (x0 + x1) // 2
    draw.line([(mid_x, y0), (mid_x, y0 - 24)], fill=blue, width=1)
    
    # Handles at 8 points + rotation handle
    handle_size = 3
    points = [
        (x0, y0), (mid_x, y0), (x1, y0),
        (x0, (y0 + y1) // 2), (x1, (y0 + y1) // 2),
        (x0, y1), (mid_x, y1), (x1, y1),
        (mid_x, y0 - 24)
    ]
    for px, py in points:
        draw.rectangle([px - handle_size, py - handle_size, px + handle_size, py + handle_size], outline=blue, fill=white, width=1)

# Helper to draw daisy flower
def draw_daisy(draw, cx, cy, r_disk=14, petal_len=24, petal_w=8):
    yellow = (229, 193, 88, 255)
    green = (100, 119, 70, 255)
    
    # 8 petals
    for angle_deg in range(0, 360, 45):
        angle = math.radians(angle_deg)
        dist = r_disk + petal_len // 2
        px = cx + dist * math.cos(angle)
        py = cy + dist * math.sin(angle)
        
        # Draw petal as ellipse
        bbox = [px - petal_w, py - petal_len // 2, px + petal_w, py + petal_len // 2]
        # Rotate ellipse or draw polygon
        p1_x = cx + (r_disk - 2) * math.cos(angle)
        p1_y = cy + (r_disk - 2) * math.sin(angle)
        tip_x = cx + (r_disk + petal_len) * math.cos(angle)
        tip_y = cy + (r_disk + petal_len) * math.sin(angle)
        
        perp = angle + math.pi / 2
        w1_x = cx + dist * math.cos(angle) + petal_w * math.cos(perp)
        w1_y = cy + dist * math.sin(angle) + petal_w * math.sin(perp)
        w2_x = cx + dist * math.cos(angle) - petal_w * math.cos(perp)
        w2_y = cy + dist * math.sin(angle) - petal_w * math.sin(perp)
        
        draw.polygon([(p1_x, p1_y), (w1_x, w1_y), (tip_x, tip_y), (w2_x, w2_y)], fill=green)
        
    # Center disk
    draw.ellipse([cx - r_disk, cy - r_disk, cx + r_disk, cy + r_disk], fill=yellow)

# Helper to draw smiley badge
def draw_smiley(draw, cx, cy, radius=32):
    lime = (212, 225, 87, 255)
    black = (26, 26, 26, 255)
    
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=lime, outline=black, width=3)
    
    # Eyes
    eye_offset_x = radius * 0.35
    eye_offset_y = radius * 0.25
    eye_r = 4
    draw.ellipse([cx - eye_offset_x - eye_r, cy - eye_offset_y - eye_r, cx - eye_offset_x + eye_r, cy - eye_offset_y + eye_r], fill=black)
    draw.ellipse([cx + eye_offset_x - eye_r, cy - eye_offset_y - eye_r, cx + eye_offset_x + eye_r, cy - eye_offset_y + eye_r], fill=black)
    
    # Smile arc
    mouth_w = radius * 0.55
    mouth_y = cy + radius * 0.1
    draw.arc([cx - mouth_w, mouth_y - mouth_w * 0.5, cx + mouth_w, mouth_y + mouth_w * 0.5], 0, 180, fill=black, width=3)


# Fonts
try:
    font_serif_lg = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 26)
    font_serif_md = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 18)
    font_sans_bold = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 13)
    font_sans_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 24)
    font_sans_sm = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 10)
except Exception:
    font_serif_lg = font_serif_md = font_sans_bold = font_sans_title = font_sans_sm = ImageFont.load_default()

# 3. GENERATE TEMPLATE 2: CỨ NỞ THÔI
im2 = create_base_shirt()
draw2 = ImageDraw.Draw(im2)
# Dotted print box
center_x = target_w // 2
box_w, box_h = 220, 260
box_x0 = center_x - box_w // 2
box_y0 = 170
box_x1 = box_x0 + box_w
box_y1 = box_y0 + box_h
draw_dashed_rect(draw2, [box_x0, box_y0, box_x1, box_y1], (180, 175, 168, 255))

# Text: CỨ NỞ THÔI
text_top = "CỨ NỞ THÔI"
bb = draw2.textbbox((0, 0), text_top, font=font_serif_md)
tw = bb[2] - bb[0]
draw2.text((center_x - tw // 2, box_y0 + 25), text_top, fill=(45, 58, 46, 255), font=font_serif_md)

# Center Daisy Flower
flower_y = box_y0 + 120
draw_daisy(draw2, center_x, flower_y, r_disk=14, petal_len=22, petal_w=8)
# Blue transform box around flower
draw_transform_handles(draw2, center_x - 42, flower_y - 42, center_x + 42, flower_y + 42)

# Text: NỞ THEO CÁCH CỦA BẠN
text_bot = "NỞ THEO CÁCH CỦA BẠN"
bb = draw2.textbbox((0, 0), text_bot, font=font_sans_bold)
tw = bb[2] - bb[0]
draw2.text((center_x - tw // 2, box_y0 + 195), text_bot, fill=(45, 58, 46, 255), font=font_sans_bold)

# Subtitle: CỨ NỞ THÔI
text_sub = "CỨ NỞ THÔI"
bb = draw2.textbbox((0, 0), text_sub, font=font_sans_sm)
tw = bb[2] - bb[0]
draw2.text((center_x - tw // 2, box_y0 + 218), text_sub, fill=(100, 119, 70, 255), font=font_sans_sm)

t2_path = os.path.join(out_dir, "template_2_shirt.png")
im2.save(t2_path)
print(f"Saved {t2_path}")

# 4. GENERATE TEMPLATE 3: NẾP CLUB
im3 = create_base_shirt()
draw3 = ImageDraw.Draw(im3)
draw_dashed_rect(draw3, [box_x0, box_y0, box_x1, box_y1], (180, 175, 168, 255))

# Text: NẾP CLUB
text_top3 = "NẾP CLUB"
bb = draw3.textbbox((0, 0), text_top3, font=font_sans_title)
tw = bb[2] - bb[0]
draw3.text((center_x - tw // 2, box_y0 + 25), text_top3, fill=(26, 26, 26, 255), font=font_sans_title)

# Center Smiley Badge
smiley_y = box_y0 + 120
draw_smiley(draw3, center_x, smiley_y, radius=32)
draw_transform_handles(draw3, center_x - 40, smiley_y - 40, center_x + 40, smiley_y + 40)

# Text: HỘI MÌNH CÓ CHẤT
text_bot3 = "HỘI MÌNH CÓ CHẤT"
bb = draw3.textbbox((0, 0), text_bot3, font=font_sans_bold)
tw = bb[2] - bb[0]
draw3.text((center_x - tw // 2, box_y0 + 198), text_bot3, fill=(26, 26, 26, 255), font=font_sans_bold)

t3_path = os.path.join(out_dir, "template_3_shirt.png")
im3.save(t3_path)
print(f"Saved {t3_path}")
print("All 3 template shirt images created successfully!")
