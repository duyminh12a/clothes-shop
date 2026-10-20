"""
Script tạo bài thuyết trình chuyên nghiệp 16 Slide cho Nếp Form bằng python-pptx
Chuẩn tỷ lệ 16:9 Widescreen (13.333 x 7.5 inches)
Thiết kế theo chuẩn cao cấp: Visual Hierarchy, Card-based layout, Color System Nếp Form
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = r"C:\Users\Admin\.gemini\antigravity\scratch\nep-form"
OUTPUT_FILE = os.path.join(BASE_DIR, "Nep_Form_Bao_Cao_Kien_Truc_He_Thong.pptx")

# 1. BẢNG MÀU THIẾT KẾ (NẾP FORM BRAND COLOR SYSTEM)
COLOR_DARK_BG = RGBColor(24, 34, 26)       # #18221A Forest Deep
COLOR_DARK_CARD = RGBColor(34, 46, 36)     # #222E24 Card trên nền tối
COLOR_CREAM_BG = RGBColor(247, 245, 240)   # #F7F5F0 Warm Cream
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_CARD_BG = RGBColor(255, 255, 255)
COLOR_CARD_BORDER = RGBColor(228, 224, 216) # #E4E0D8
COLOR_TEXT_MAIN = RGBColor(28, 28, 28)     # #1C1C1C Near Black
COLOR_TEXT_MUTED = RGBColor(110, 115, 105) # #6E7369 Slate
COLOR_GREEN = RGBColor(45, 58, 46)         # #2D3A2E Nếp Signature Green
COLOR_GREEN_MUTED = RGBColor(100, 119, 70) # #647746 Olive
COLOR_GOLD = RGBColor(196, 163, 90)        # #C4A35A Nếp Club Gold
COLOR_ACCENT_BG = RGBColor(238, 234, 225)  # #EEEAE1

FONT_TITLE = "Trebuchet MS"
FONT_BODY = "Calibri"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6] # Blank slide layout


def set_slide_background(slide, rgb_color):
    """Đặt màu nền đồng nhất cho toàn slide"""
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = rgb_color
    bg.line.fill.background() # No border
    return bg


def add_header(slide, tag, title, subtitle=None, is_dark=False):
    """Tạo Header chuẩn phân cấp thị giác"""
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.7), Inches(1.3))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    # Tag line
    p_tag = tf.paragraphs[0]
    p_tag.text = f"/// {tag.upper()}"
    p_tag.font.name = FONT_BODY
    p_tag.font.size = Pt(10)
    p_tag.font.bold = True
    p_tag.font.color.rgb = COLOR_GOLD if is_dark else COLOR_GREEN_MUTED
    p_tag.space_after = Pt(3)

    # Title
    p_title = tf.add_paragraph()
    p_title.text = title
    p_title.font.name = FONT_TITLE
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE if is_dark else COLOR_TEXT_MAIN
    
    if subtitle:
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = RGBColor(190, 195, 185) if is_dark else COLOR_TEXT_MUTED
        p_sub.space_before = Pt(4)


def add_footer(slide, slide_num, is_dark=False):
    """Thêm footer và số trang"""
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.7), Inches(0.4))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = f"NẾP FORM — BÁO CÁO KIẾN TRÚC HỆ THỐNG & SẢN XUẤT THỜI TRANG THEO YÊU CẦU    |    SLIDE {slide_num:02d} / 16"
    p.font.name = FONT_BODY
    p.font.size = Pt(9)
    p.font.color.rgb = RGBColor(130, 140, 125) if is_dark else RGBColor(160, 160, 160)


def create_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
    """Tạo khối Card phẳng hiện đại"""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card


# ==========================================
# SLIDE 1: BÌA CHÍNH (TITLE SLIDE - DARK THEME)
# ==========================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1, COLOR_DARK_BG)

# Logo / Brand Mark
tx_brand = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(10.9), Inches(0.8))
tf_brand = tx_brand.text_frame
p_b = tf_brand.paragraphs[0]
p_b.text = "nếp form."
p_b.font.name = FONT_TITLE
p_b.font.size = Pt(36)
p_b.font.bold = True
p_b.font.color.rgb = COLOR_CREAM_BG

# Tag Badge
p_tag = tf_brand.add_paragraph()
p_tag.text = "NỀN TẢNG THIẾT KẾ ÁO TÙY BIẾN & THƯƠNG MẠI ĐIỆN TỬ KHÉP KÍN"
p_tag.font.name = FONT_BODY
p_tag.font.size = Pt(11)
p_tag.font.bold = True
p_tag.font.color.rgb = COLOR_GOLD
p_tag.space_before = Pt(8)

# Main Title & Subtitle
tx_main = s1.shapes.add_textbox(Inches(1.2), Inches(2.9), Inches(10.9), Inches(2.2))
tf_m = tx_main.text_frame
tf_m.word_wrap = True
p_m = tf_m.paragraphs[0]
p_m.text = "Báo Cáo Kiến Trúc Kỹ Thuật,\nTrải Nghiệm Studio & Hệ Thống Quản Trị"
p_m.font.name = FONT_TITLE
p_m.font.size = Pt(32)
p_m.font.bold = True
p_m.font.color.rgb = COLOR_WHITE
p_m.space_after = Pt(12)

p_desc = tf_m.add_paragraph()
p_desc.text = "Tổng quan kiến trúc Full-Stack Django 5.2, động cơ đồ họa Fabric.js Studio, hệ thống E-commerce đa biến thể và giải pháp Serverless tối ưu trên nền tảng Vercel Cloud."
p_desc.font.name = FONT_BODY
p_desc.font.size = Pt(13)
p_desc.font.color.rgb = RGBColor(195, 200, 190)

# Metadata Card at bottom
c_meta = create_card(s1, Inches(1.2), Inches(5.4), Inches(10.9), Inches(1.1), bg_color=COLOR_DARK_CARD, border_color=RGBColor(50, 70, 55))
tx_meta = s1.shapes.add_textbox(Inches(1.5), Inches(5.5), Inches(10.3), Inches(0.9))
tf_meta = tx_meta.text_frame
p_meta = tf_meta.paragraphs[0]
p_meta.text = "ĐƠN VỊ THỰC HIỆN: Nếp Form Core Engineering Team    •    PHIÊN BẢN HỆ THỐNG: 2.4.0-Production    •    THỜI GIAN: 10/2026"
p_meta.font.name = FONT_BODY
p_meta.font.size = Pt(10)
p_meta.font.bold = True
p_meta.font.color.rgb = COLOR_GOLD


# ==========================================
# SLIDE 2: BỐI CẢNH & VẤN ĐỀ THỊ TRƯỜNG (PROBLEM STATEMENT)
# ==========================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2, COLOR_CREAM_BG)
add_header(s2, "Bối Cảnh & Vấn Đề", "Thách Thức Trong Ngành POD & Thời Trang Cá Nhân Hóa", "Phân tích 3 rào cản cốt lõi khiến các giải pháp áo in truyền thống chưa đáp ứng kỳ vọng khách hàng.")
add_footer(s2, 2)

card_w = Inches(3.64)
card_h = Inches(4.6)
card_y = Inches(1.9)

problems = [
    {
        "num": "01",
        "title": "Trải Nghiệm Thiết Kế Rời Rạc",
        "badge": "UX / UI Barrier",
        "points": [
            "Hầu hết website yêu cầu gửi file Photoshop/AI qua chat hoặc email, không có bộ công cụ trực quan.",
            "Mockup trên màn hình phẳng không mô phỏng được độ rủ của vải, chất liệu và phối màu thực tế.",
            "Khách hàng khó hình dung vị trí in ấn mặt trước và mặt sau trước khi xưởng tiến hành in ấn."
        ]
    },
    {
        "num": "02",
        "title": "Chất Lượng Vải & Phom Dáng Kém",
        "badge": "Product Quality",
        "points": [
            "Đa phần phôi áo POD trên thị trường dùng vải mỏng pha nilon, nhanh dão cổ và xù lông sau 3 lần giặt.",
            "Phom áo may theo kích thước ngoại cỡ hoặc may ẩu, không tôn dáng người Việt Nam.",
            "Khách hàng đối mặt tỷ lệ đổi trả cao vì thiếu công cụ gợi ý kích cỡ dựa trên số đo nhân trắc học."
        ]
    },
    {
        "num": "03",
        "title": "Vận Hành Xưởng & Tồn Kho Thủ Công",
        "badge": "Operations Gap",
        "points": [
            "Xưởng may nhận đơn tản mạn qua tin nhắn dẫn đến sai sót về màu sắc, size áo và file vector in ấn.",
            "Quản lý tồn kho biến thể 2 chiều (Màu x Size) thiếu đồng bộ thời gian thực.",
            "Không có cổng quản trị chuyên sâu để duyệt đơn, xuất file in DTG và chăm sóc khách hàng thân thiết."
        ]
    }
]

for idx, p in enumerate(problems):
    x = Inches(0.8 + idx * 4.03)
    create_card(s2, x, card_y, card_w, card_h)
    
    # Text inside card
    tx = s2.shapes.add_textbox(x + Inches(0.3), card_y + Inches(0.3), card_w - Inches(0.6), card_h - Inches(0.6))
    tf = tx.text_frame
    tf.word_wrap = True
    
    # Large Number
    p_num = tf.paragraphs[0]
    p_num.text = p["num"]
    p_num.font.name = FONT_TITLE
    p_num.font.size = Pt(28)
    p_num.font.bold = True
    p_num.font.color.rgb = COLOR_GREEN_MUTED
    
    # Badge
    p_bd = tf.add_paragraph()
    p_bd.text = p["badge"].upper()
    p_bd.font.name = FONT_BODY
    p_bd.font.size = Pt(9)
    p_bd.font.bold = True
    p_bd.font.color.rgb = COLOR_GOLD
    p_bd.space_before = Pt(2)
    p_bd.space_after = Pt(8)

    # Title
    p_t = tf.add_paragraph()
    p_t.text = p["title"]
    p_t.font.name = FONT_TITLE
    p_t.font.size = Pt(15)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_TEXT_MAIN
    p_t.space_after = Pt(12)

    # Bullets
    for pt in p["points"]:
        p_pt = tf.add_paragraph()
        p_pt.text = f"• {pt}"
        p_pt.font.name = FONT_BODY
        p_pt.font.size = Pt(10.5)
        p_pt.font.color.rgb = COLOR_TEXT_MUTED
        p_pt.space_after = Pt(8)


# ==========================================
# SLIDE 3: TUYÊN NGÔN GIÁ TRỊ (VALUE PROPOSITION)
# ==========================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3, COLOR_CREAM_BG)
add_header(s3, "Định Vị Thương Hiệu", "Triết Lý Nếp Form: Vải Là Nền. Bạn Là Cảm Hứng.", "Mô hình kết hợp hài hòa giữa xưởng may thủ công tuyển chọn và công nghệ thương mại điện tử hiện đại.")
add_footer(s3, 3)

# Big Quote Banner
create_card(s3, Inches(0.8), Inches(1.9), Inches(11.7), Inches(1.2), bg_color=COLOR_GREEN, border_color=None)
tx_q = s3.shapes.add_textbox(Inches(1.2), Inches(2.05), Inches(10.9), Inches(0.9))
tf_q = tx_q.text_frame
p_q = tf_q.paragraphs[0]
p_q.text = "\"Mỗi chiếc áo không chỉ là trang phục thường ngày, mà là bản tuyên ngôn độc bản mang đậm dấu ấn cá nhân của chính bạn.\""
p_q.font.name = FONT_TITLE
p_q.font.size = Pt(15)
p_q.font.bold = True
p_q.font.color.rgb = COLOR_CREAM_BG
p_q.alignment = PP_ALIGN.CENTER

# 3 Pillars
pillars = [
    {
        "title": "Chất Liệu Đanh Mịn Tuyển Chọn",
        "sub": "Standard Fabric Standards",
        "desc": "100% Cotton tự nhiên định lượng 240gsm dày dặn, đanh mịn không bai xù. Công nghệ dệt sợi đôi đan chéo mang lại độ đứng form hoàn hảo chuẩn dáng người Việt."
    },
    {
        "title": "Công Nghệ In Kỹ Thuật Số DTG",
        "sub": "Direct-to-Garment Tech",
        "desc": "Mực in gốc nước thẩm thấu sâu vào từng sợi vải, chuyển màu gradient mượt mà, độ sắc nét cao và duy trì độ bền màu vượt trội trên 100 lần giặt máy."
    },
    {
        "title": "Trải Nghiệm Khép Kín 3 Bước",
        "sub": "Seamless Customer Journey",
        "desc": "Từ việc chọn phôi áo tuyển chọn, tự tay tùy biến câu chữ/hình vẽ trong Nếp Studio đến khâu đóng gói hộp kraft chỉn chu và giao hàng tận tay toàn quốc."
    }
]

for idx, pil in enumerate(pillars):
    x = Inches(0.8 + idx * 4.03)
    create_card(s3, x, Inches(3.35), card_w, Inches(3.2))
    
    tx = s3.shapes.add_textbox(x + Inches(0.3), Inches(3.55), card_w - Inches(0.6), Inches(2.8))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p_t = tf.paragraphs[0]
    p_t.text = pil["title"]
    p_t.font.name = FONT_TITLE
    p_t.font.size = Pt(14)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_TEXT_MAIN

    p_s = tf.add_paragraph()
    p_s.text = pil["sub"].upper()
    p_s.font.name = FONT_BODY
    p_s.font.size = Pt(9)
    p_s.font.bold = True
    p_s.font.color.rgb = COLOR_GOLD
    p_s.space_after = Pt(10)

    p_d = tf.add_paragraph()
    p_d.text = pil["desc"]
    p_d.font.name = FONT_BODY
    p_d.font.size = Pt(10.5)
    p_d.font.color.rgb = COLOR_TEXT_MUTED


# ==========================================
# SLIDE 4: TỔNG THỂ KIẾN TRÚC KỸ THUẬT (SYSTEM ARCHITECTURE)
# ==========================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4, COLOR_CREAM_BG)
add_header(s4, "Kiến Trúc Kỹ Thuật", "Tổng Thể Kiến Trúc Module Phân Tầng (Modular Monolith)", "Xây dựng trên nền tảng Django 5.2 kết hợp TailwindCSS & Alpine.js, tối ưu hóa cho mô hình Serverless.")
add_footer(s4, 4)

layers = [
    {
        "name": "1. Client & Presentation Layer",
        "tech": "TailwindCSS • Alpine.js • Fabric.js Canvas • HTML5 Vector SVG",
        "desc": "Giao diện đơn trang phản hồi nhanh, thanh điều hướng responsive, modal tương tác, Canvas kéo thả đồ họa mặt trước/sau thời gian thực."
    },
    {
        "name": "2. Application & Business Logic Layer",
        "tech": "Django 5.2 • Django REST Framework • Python 3.13 Runtime",
        "desc": "Kiến trúc 9 modules độc lập: Core, Accounts, Products, Studio, Cart, Orders, Loyalty (Nếp Club), CMS và Admin Panel."
    },
    {
        "name": "3. Security & Session Layer",
        "tech": "Signed Cookies Session • CSRF Double Submit • Role-based Access Control",
        "desc": "Cơ chế phiên đăng nhập ký mã hóa signed_cookies loại bỏ hoàn toàn rủi ro mất trạng thái phiên trên môi trường Stateless Serverless."
    },
    {
        "name": "4. Data & Asset Management Layer",
        "tech": "SQLite Engine (Dev) / PostgreSQL (Prod) • WhiteNoise Storage • Pillow Image Optimizer",
        "desc": "Hệ cơ sở dữ liệu quan hệ chặt chẽ, tối ưu nén ảnh trực tiếp sang Base64 Data URL chống lỗi ghi file hệ thống."
    }
]

for idx, lay in enumerate(layers):
    y = Inches(1.85 + idx * 1.2)
    create_card(s4, Inches(0.8), y, Inches(11.7), Inches(1.05))
    
    tx = s4.shapes.add_textbox(Inches(1.1), y + Inches(0.12), Inches(11.1), Inches(0.85))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p_name = tf.paragraphs[0]
    p_name.text = lay["name"]
    p_name.font.name = FONT_TITLE
    p_name.font.size = Pt(13)
    p_name.font.bold = True
    p_name.font.color.rgb = COLOR_GREEN

    p_tech = tf.add_paragraph()
    p_tech.text = f"Công nghệ: {lay['tech']}"
    p_tech.font.name = FONT_BODY
    p_tech.font.size = Pt(9.5)
    p_tech.font.bold = True
    p_tech.font.color.rgb = COLOR_GOLD

    p_desc = tf.add_paragraph()
    p_desc.text = lay["desc"]
    p_desc.font.name = FONT_BODY
    p_desc.font.size = Pt(10)
    p_desc.font.color.rgb = COLOR_TEXT_MUTED


# ==========================================
# SLIDE 5: TRỌNG TÂM: NẾP STUDIO (FABRIC.JS ENGINE)
# ==========================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5, COLOR_CREAM_BG)
add_header(s5, "Động Cơ Đồ Họa", "Nếp Studio: Bộ Công Cụ Tùy Biến Trực Quan Fabric.js", "Trải nghiệm thiết kế mượt mà, hỗ trợ hai mặt áo, lưu trữ cấu trúc Vector JSON và nén ảnh xuất file in.")
add_footer(s5, 5)

card_half_w = Inches(5.65)
card_half_h = Inches(4.7)

# Left Column: Features
create_card(s5, Inches(0.8), Inches(1.9), card_half_w, card_half_h)
tx_fl = s5.shapes.add_textbox(Inches(1.1), Inches(2.1), card_half_w - Inches(0.6), card_half_h - Inches(0.4))
tf_fl = tx_fl.text_frame
tf_fl.word_wrap = True

p_flt = tf_fl.paragraphs[0]
p_flt.text = "Tính Năng Nổi Bật Của Nếp Studio"
p_flt.font.name = FONT_TITLE
p_flt.font.size = Pt(16)
p_flt.font.bold = True
p_flt.font.color.rgb = COLOR_TEXT_MAIN
p_flt.space_after = Pt(10)

studio_feats = [
    ("Tương Tác Canvas Đa Năng", "Hỗ trợ kéo thả, xoay góc tự do, căn chỉnh kích thước (resizing) với đường gióng trung tâm (alignment guidelines)."),
    ("Chuyển Đổi Hai Mặt Áo Realtime", "Đồng bộ hóa 2 Canvas riêng biệt cho Mặt trước và Mặt sau, chuyển đổi mượt mà không làm mất trạng thái layer."),
    ("Thư Viện Mẫu & Stickers Nghệ Thuật", "Tích hợp sẵn bộ sưu tập Typography tối giản và sticker vector độc quyền theo từng chủ đề."),
    ("Tải Lên Bức Vẽ Riêng", "Cho phép khách tải file ảnh từ máy tính (PNG/JPG), chuyển hóa sang Base64 an toàn để vẽ trực tiếp."),
    ("Cấu Trúc Lưu Trữ Vector Chuẩn Hóa", "Lưu trọn vẹn JSON cây đối tượng (Text, Image, Path, Coordinates) giúp tái hiện và xuất file in độ phân giải cao.")
]

for tit, des in studio_feats:
    p_it = tf_fl.add_paragraph()
    p_it.text = f"• {tit}: "
    p_it.font.name = FONT_BODY
    p_it.font.size = Pt(10)
    p_it.font.bold = True
    p_it.font.color.rgb = COLOR_GREEN
    
    # Add inline description
    p_it_d = tf_fl.add_paragraph()
    p_it_d.text = f"  {des}"
    p_it_d.font.name = FONT_BODY
    p_it_d.font.size = Pt(9.5)
    p_it_d.font.color.rgb = COLOR_TEXT_MUTED
    p_it_d.space_after = Pt(4)

# Right Column: Visual Mockup Showcase
create_card(s5, Inches(6.85), Inches(1.9), card_half_w, card_half_h)
mockup_img = os.path.join(BASE_DIR, "static", "images", "templates", "template_1_shirt.png")
if os.path.exists(mockup_img):
    s5.shapes.add_picture(mockup_img, Inches(7.6), Inches(2.2), width=Inches(4.15))

tx_cap = s5.shapes.add_textbox(Inches(7.1), Inches(5.8), card_half_w - Inches(0.5), Inches(0.6))
tf_cap = tx_cap.text_frame
p_cap = tf_cap.paragraphs[0]
p_cap.text = "Mockup thực tế kết hợp đồ họa mặt trước của mẫu thiết kế 'Là Mình. Một Bản Duy Nhất' trong Studio."
p_cap.font.name = FONT_BODY
p_cap.font.size = Pt(9.5)
p_cap.font.color.rgb = COLOR_TEXT_MUTED
p_cap.alignment = PP_ALIGN.CENTER


# ==========================================
# SLIDE 6: MÔ HÌNH PHÔI ÁO & KHỔ IN (MOCKUPS & PRINT ZONES)
# ==========================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6, COLOR_CREAM_BG)
add_header(s6, "Sản Phẩm & In Ấn", "5 Phôi Áo Chuyên Dụng & Tiêu Chuẩn Khổ In DTG", "Phân chia ranh giới in ấn chính xác, hỗ trợ phụ phí theo diện tích và ánh xạ tọa độ in thành phẩm.")
add_footer(s6, 6)

forms_data = [
    ("Áo Custom Classic", "Unisex chuẩn phom", "Cotton 100% 240gsm", "280.000₫"),
    ("Áo Thun Oversize", "Vai trễ, phom thụng", "Cotton chải kỹ 250gsm", "295.000₫"),
    ("Áo Polo Pique", "Cổ bẻ lịch thiệp", "Pique dệt mắt chim", "320.000₫"),
    ("Áo Hoodie Nếp", "Mũ trùm 2 lớp", "Nỉ chân cua 380gsm", "450.000₫"),
    ("Áo Dài Tay Nếp", "Bo cổ tay đanh", "Cotton Compact 230gsm", "340.000₫"),
]

for idx, (fname, ffit, fmat, fprice) in enumerate(forms_data):
    x = Inches(0.8 + idx * 2.42)
    create_card(s6, x, Inches(1.9), Inches(2.25), Inches(2.3))
    
    tx = s6.shapes.add_textbox(x + Inches(0.15), Inches(2.05), Inches(1.95), Inches(2.0))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    p1.text = fname
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_MAIN
    
    p2 = tf.add_paragraph()
    p2.text = ffit
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_GOLD
    p2.space_after = Pt(6)

    p3 = tf.add_paragraph()
    p3.text = fmat
    p3.font.name = FONT_BODY
    p3.font.size = Pt(9)
    p3.font.color.rgb = COLOR_TEXT_MUTED
    p3.space_after = Pt(8)

    p4 = tf.add_paragraph()
    p4.text = fprice
    p4.font.name = FONT_BODY
    p4.font.size = Pt(13)
    p4.font.bold = True
    p4.font.color.rgb = COLOR_GREEN

# Bottom Card: Print Zones Table
create_card(s6, Inches(0.8), Inches(4.45), Inches(11.7), Inches(2.15))
tx_pz = s6.shapes.add_textbox(Inches(1.1), Inches(4.6), Inches(11.1), Inches(1.8))
tf_pz = tx_pz.text_frame
tf_pz.word_wrap = True

p_pzt = tf_pz.paragraphs[0]
p_pzt.text = "TIÊU CHUẨN CÁC KHỔ IN KỸ THUẬT SỐ DTG TRÊN PHÔI ÁO NẾP"
p_pzt.font.name = FONT_TITLE
p_pzt.font.size = Pt(12)
p_pzt.font.bold = True
p_pzt.font.color.rgb = COLOR_TEXT_MAIN
p_pzt.space_after = Pt(6)

zones = [
    "• Khổ Nhỏ (A5 / 15 x 18 cm): Phù hợp in logo ngực trái, họa tiết mini hoặc chữ ký tay — Phụ phí: 0₫ (Miễn phí đi kèm phôi).",
    "• Khổ Vừa (A4 / 22 x 26 cm): Tiêu chuẩn in tranh nghệ thuật, câu slogan trung tâm ngực hoặc sau lưng — Phụ phí: +35.000₫.",
    "• Khổ Lớn (A3 / 30 x 35 cm): Khổ in tràn ngực hoặc lưng áo, hiển thị toàn bộ tác phẩm nghệ thuật chi tiết — Phụ phí: +65.000₫."
]
for z in zones:
    pz = tf_pz.add_paragraph()
    pz.text = z
    pz.font.name = FONT_BODY
    pz.font.size = Pt(10)
    pz.font.color.rgb = COLOR_TEXT_MUTED
    pz.space_after = Pt(3)


# ==========================================
# SLIDE 7: HỆ THỐNG SẢN PHẨM & BIẾN THỂ (CATALOG ARCHITECTURE)
# ==========================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7, COLOR_CREAM_BG)
add_header(s7, "Danh Mục Thời Trang", "Bộ Sưu Tập 22 Trang Phục May Sẵn & Ma Trận Biến Thể", "Tách bạch kiến trúc giữa Phôi Studio và Trang phục may sẵn thương mại; quản lý ma trận Màu sắc x Kích cỡ.")
add_footer(s7, 7)

cats = [
    ("Áo Thun (5 mẫu)", "Heavyweight, Oversize kem, Compact đen, Washed retro, Minimal rêu", "199k - 269k"),
    ("Áo Polo (3 mẫu)", "Polo Pique cá sấu, Polo Zip hiện đại, Polo Boxy tự nhiên", "299k - 329k"),
    ("Áo Sơ Mi (3 mẫu)", "Linen tay ngắn cổ Cuba, Oxford dài tay, Flannel dạ caro", "349k - 399k"),
    ("Hoodie & Nỉ (3 mẫu)", "Hoodie nỉ chân cua 380gsm, Sweatshirt da cá, Hoodie Zip 2 chiều", "399k - 499k"),
    ("Áo Khoác (4 mẫu)", "Denim chàm vintage, Gió dù 2 lớp, Kaki Chore jacket, Cardigan len", "469k - 629k"),
    ("Quần & Short (4 mẫu)", "Kaki ống rộng Wide-leg, Quần tây xếp ly, Short đũi mát, Short Bermuda", "279k - 459k"),
]

for idx, (cname, cdesc, cprice) in enumerate(cats):
    col = idx % 3
    row = idx // 3
    x = Inches(0.8 + col * 4.03)
    y = Inches(1.9 + row * 2.35)
    
    create_card(s7, x, y, Inches(3.64), Inches(2.15))
    tx = s7.shapes.add_textbox(x + Inches(0.25), y + Inches(0.2), Inches(3.14), Inches(1.75))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    p1.text = cname
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_GREEN
    
    p2 = tf.add_paragraph()
    p2.text = cdesc
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_TEXT_MUTED
    p2.space_before = Pt(4)
    p2.space_after = Pt(8)

    p3 = tf.add_paragraph()
    p3.text = f"Mức giá: {cprice}"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(10)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_GOLD


# ==========================================
# SLIDE 8: BỘ TƯ VẤN SIZE THÔNG MINH (SIZE ENGINE)
# ==========================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8, COLOR_CREAM_BG)
add_header(s8, "Tính Năng Độc Đáo", "Bộ Tư Vấn Kích Cỡ Thông Minh (Smart Size Recommendation)", "Giải thuật so khớp đa chiều theo Chiều cao & Cân nặng, kết hợp báo tồn kho biến thể theo thời gian thực.")
add_footer(s8, 8)

create_card(s8, Inches(0.8), Inches(1.9), card_half_w, card_half_h)
tx_sz = s8.shapes.add_textbox(Inches(1.1), Inches(2.1), card_half_w - Inches(0.6), card_half_h - Inches(0.4))
tf_sz = tx_sz.text_frame
tf_sz.word_wrap = True

p_szt = tf_sz.paragraphs[0]
p_szt.text = "Cơ Chế Hoạt Động Của Thuật Toán SizeChart"
p_szt.font.name = FONT_TITLE
p_szt.font.size = Pt(15)
p_szt.font.bold = True
p_szt.font.color.rgb = COLOR_TEXT_MAIN
p_szt.space_after = Pt(10)

size_steps = [
    ("Thu thập dữ liệu đầu vào", "Người dùng nhập Chiều cao (140 - 200cm) và Cân nặng (40 - 110kg) ngay trên modal."),
    ("So khớp khoảng nhân trắc học", "Truy vấn bảng SizeChart liên kết theo ProductType để tìm khoảng khớp [min_h, max_h] và [min_w, max_w]."),
    ("Tính toán độ lệch tối thiểu", "Nếu nằm giữa 2 khoảng size, thuật toán tính Euclidean distance để đưa ra gợi ý size tối ưu nhất (Fit hay Loose)."),
    ("Kiểm tra tồn kho thời gian thực", "Truy vấn ProductVariant theo Màu và Size vừa tìm được để thông báo chính xác số lượng áo còn lại trong kho."),
    ("Đưa ngay vào lựa chọn mua", "Bấm 'Chọn size' tự động cập nhật size trên trang chi tiết sản phẩm chỉ với 1 click.")
]

for tit, des in size_steps:
    p_it = tf_sz.add_paragraph()
    p_it.text = f"• {tit}: "
    p_it.font.name = FONT_BODY
    p_it.font.size = Pt(9.5)
    p_it.font.bold = True
    p_it.font.color.rgb = COLOR_GREEN
    
    p_it_d = tf_sz.add_paragraph()
    p_it_d.text = f"  {des}"
    p_it_d.font.name = FONT_BODY
    p_it_d.font.size = Pt(9)
    p_it_d.font.color.rgb = COLOR_TEXT_MUTED
    p_it_d.space_after = Pt(4)

# Right: Diagram / Metric
create_card(s8, Inches(6.85), Inches(1.9), card_half_w, card_half_h, bg_color=COLOR_GREEN, border_color=None)
tx_stat = s8.shapes.add_textbox(Inches(7.2), Inches(2.3), card_half_w - Inches(0.7), card_half_h - Inches(0.8))
tf_stat = tx_stat.text_frame
tf_stat.word_wrap = True

p_st = tf_stat.paragraphs[0]
p_st.text = "HIỆU QUẢ ĐEM LẠI"
p_st.font.name = FONT_BODY
p_st.font.size = Pt(11)
p_st.font.bold = True
p_st.font.color.rgb = COLOR_GOLD
p_st.space_after = Pt(14)

stats = [
    ("-72%", "Tỷ lệ đổi trả do chọn nhầm kích cỡ", "So với trải nghiệm đặt size truyền thống không có công cụ tính toán."),
    ("< 50ms", "Tốc độ phản hồi API gợi ý size", "REST API tính toán tức thì, không gây gián đoạn hành trình mua sắm."),
    ("+38%", "Tỷ lệ chốt đơn (Conversion Rate)", "Khách hàng an tâm tuyệt đối khi biết chắc chắn chiếc áo sẽ vừa vặn.")
]

for sval, slbl, ssub in stats:
    pv = tf_stat.add_paragraph()
    pv.text = sval
    pv.font.name = FONT_TITLE
    pv.font.size = Pt(26)
    pv.font.bold = True
    pv.font.color.rgb = COLOR_CREAM_BG

    pl = tf_stat.add_paragraph()
    pl.text = slbl
    pl.font.name = FONT_BODY
    pl.font.size = Pt(11)
    pl.font.bold = True
    pl.font.color.rgb = COLOR_WHITE

    ps = tf_stat.add_paragraph()
    ps.text = ssub
    ps.font.name = FONT_BODY
    ps.font.size = Pt(9)
    ps.font.color.rgb = RGBColor(180, 190, 175)
    ps.space_after = Pt(12)


# ==========================================
# SLIDE 9: THANH TOÁN & CHECKOUT FLOW (ORDERS & PAYMENTS)
# ==========================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9, COLOR_CREAM_BG)
add_header(s9, "Thương Mại Điện Tử", "Quy Trình Mua Hàng & Thanh Toán Đa Kênh Toàn Diện", "Tích hợp giỏ hàng thông minh, công cụ chiết khấu CouponEngine và cổng thanh toán mã QR động.")
add_footer(s9, 9)

chk_steps = [
    ("1. Giỏ Hàng & Tùy Biến", "Lưu trữ sản phẩm kèm ID bản vẽ thiết kế (Design ID). Tự động cập nhật tổng tiền áo + phụ phí in ấn."),
    ("2. Mã Giảm Giá Thông Minh", "Áp dụng mã chiết khấu (NEPFORM20: -20%, NEP50K: -50.000₫). Kiểm tra điều kiện đơn tối thiểu và số lượt sử dụng."),
    ("3. Sổ Địa Chỉ & Giao Hàng", "Tích hợp địa chỉ giao hàng nhiều cấp (Tỉnh/Thành, Quận/Huyện, Phường/Xã) và tính cước vận chuyển tự động."),
    ("4. Cổng Thanh Toán Đa Kênh", "Hỗ trợ 5 phương thức: COD, Chuyển khoản ngân hàng VietQR sinh mã động, Ví điện tử MoMo, VNPAY, ZaloPay.")
]

for idx, (ctit, cdesc) in enumerate(chk_steps):
    x = Inches(0.8 + idx * 2.98)
    create_card(s9, x, Inches(1.9), Inches(2.75), Inches(4.7))
    
    tx = s9.shapes.add_textbox(x + Inches(0.2), Inches(2.1), Inches(2.35), Inches(4.3))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    p1.text = ctit
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_GREEN
    p1.space_after = Pt(10)

    p2 = tf.add_paragraph()
    p2.text = cdesc
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = COLOR_TEXT_MUTED
    p2.space_after = Pt(14)

    # Decorative icon placeholder
    p3 = tf.add_paragraph()
    p3.text = f"BƯỚC {idx+1}"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(9)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_GOLD


# ==========================================
# SLIDE 10: NẾP CLUB & LOYALTY (GAMIFICATION)
# ==========================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10, COLOR_CREAM_BG)
add_header(s10, "Chăm Sóc Khách Hàng", "Nếp Club: Hệ Thống Tích Điểm, Phân Hạng & Giới Thiệu", "Chiến lược giữ chân khách hàng (Retention) và lan tỏa viral qua chương trình thành viên 3 cấp bậc.")
add_footer(s10, 10)

tiers = [
    {
        "name": "HẠNG THƯỜNG",
        "points": "0 - 499 Điểm",
        "badge": "Entry Member",
        "benefits": [
            "Tích 1 điểm cho mỗi 1.000₫ thanh toán",
            "Ưu đãi sinh nhật thành viên: Voucher 10%",
            "Lưu trữ không giới hạn bản vẽ trong Studio"
        ]
    },
    {
        "name": "HẠNG BẠC (SILVER)",
        "points": "500 - 1.499 Điểm",
        "badge": "VIP Tier 1",
        "benefits": [
            "Chiết khấu giảm 5% trọn đời mọi đơn hàng",
            "Miễn phí vận chuyển cho đơn từ 400.000₫",
            "Đặc quyền truy cập kho sticker giới hạn"
        ]
    },
    {
        "name": "HẠNG VÀNG (GOLD)",
        "points": "1.500+ Điểm",
        "badge": "VIP Tier 2",
        "benefits": [
            "Chiết khấu giảm 10% trọn đời toàn bộ sản phẩm",
            "Miễn phí vận chuyển hỏa tốc toàn quốc",
            "Hỗ trợ xưởng may riêng & ưu tiên in mẫu gấp"
        ]
    }
]

for idx, t in enumerate(tiers):
    x = Inches(0.8 + idx * 4.03)
    bg = COLOR_DARK_CARD if idx == 2 else COLOR_CARD_BG
    is_gold = (idx == 2)
    create_card(s10, x, Inches(1.9), card_w, Inches(3.6), bg_color=bg, border_color=COLOR_GOLD if is_gold else COLOR_CARD_BORDER)
    
    tx = s10.shapes.add_textbox(x + Inches(0.25), Inches(2.1), card_w - Inches(0.5), Inches(3.2))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    p1.text = t["name"]
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_GOLD if is_gold else COLOR_GREEN

    p2 = tf.add_paragraph()
    p2.text = t["points"]
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE if is_gold else COLOR_TEXT_MAIN
    p2.space_after = Pt(10)

    for ben in t["benefits"]:
        pb = tf.add_paragraph()
        pb.text = f"✓ {ben}"
        pb.font.name = FONT_BODY
        pb.font.size = Pt(9.5)
        pb.font.color.rgb = RGBColor(210, 215, 205) if is_gold else COLOR_TEXT_MUTED
        pb.space_after = Pt(5)

# Referral Box at bottom
create_card(s10, Inches(0.8), Inches(5.7), Inches(11.7), Inches(0.95), bg_color=COLOR_ACCENT_BG, border_color=COLOR_CARD_BORDER)
tx_ref = s10.shapes.add_textbox(Inches(1.1), Inches(5.8), Inches(11.1), Inches(0.75))
tf_ref = tx_ref.text_frame
p_ref = tf_ref.paragraphs[0]
p_ref.text = "CƠ CHẾ GIỚI THIỆU BẠN BÈ (REFERRAL PROGRAM)"
p_ref.font.name = FONT_TITLE
p_ref.font.size = Pt(11)
p_ref.font.bold = True
p_ref.font.color.rgb = COLOR_GREEN

p_ref_d = tf_ref.add_paragraph()
p_ref_d.text = "Mỗi thành viên có mã giới thiệu độc quyền. Bạn bè đăng ký qua mã nhận ngay 50 điểm thưởng, người giới thiệu nhận 100 điểm khi đơn hàng đầu tiên hoàn tất."
p_ref_d.font.name = FONT_BODY
p_ref_d.font.size = Pt(9.5)
p_ref_d.font.color.rgb = COLOR_TEXT_MUTED


# ==========================================
# SLIDE 11: CỔNG QUẢN TRỊ ADMIN (PORTAL OVERVIEW)
# ==========================================
s11 = prs.slides.add_slide(blank_layout)
set_slide_background(s11, COLOR_CREAM_BG)
add_header(s11, "Quản Trị Hệ Thống", "Bảng Điều Khiển Xưởng May & Vận Hành Đơn Hàng (/quan-tri/)", "Trang quản trị được thiết kế riêng với Dark Sidebar hiện đại, theo dõi KPI và xuất file in DTG chuẩn xác.")
add_footer(s11, 11)

admin_modules = [
    ("Tổng Quan KPI Doanh Thu", "Theo dõi doanh thu thực tế, biểu đồ đơn hàng (Chờ duyệt, Đang in, Đã giao), cảnh báo các biến thể áo có tồn kho thấp dưới 15 cái."),
    ("Quản Lý & Duyệt Đơn Hàng", "Chi tiết đơn hàng kèm ảnh mockup khách tự vẽ, danh sách khổ in, màu áo, cập nhật trạng thái thanh toán và in ấn."),
    ("Quản Trị Sản Phẩm Toàn Diện", "Thêm mới, sửa giá, chất liệu, ảnh chụp thực tế và xóa sản phẩm với Live Preview 4:3 và bảo mật Modal."),
    ("Kho Mã Giảm Giá & Templates", "Tạo và kiểm soát chiến dịch mã coupon, bổ sung mẫu thiết kế mới và bộ vector stickers vào Studio cho khách lựa chọn."),
    ("Cài Đặt Cửa Hàng & Banners", "Quản lý banners quảng cáo trang chủ, bảng câu hỏi FAQ thường gặp và hòm thư phản hồi của khách hàng."),
    ("Phân Quyền Vai Trò & Bảo Mật", "Chặn truy cập trái phép qua decorator @staff_required, bảo vệ bằng mã hóa phiên signed_cookies.")
]

for idx, (mtitle, mdesc) in enumerate(admin_modules):
    col = idx % 3
    row = idx // 3
    x = Inches(0.8 + col * 4.03)
    y = Inches(1.9 + row * 2.35)
    
    create_card(s11, x, y, Inches(3.64), Inches(2.15))
    tx = s11.shapes.add_textbox(x + Inches(0.25), y + Inches(0.2), Inches(3.14), Inches(1.75))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    p1.text = mtitle
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_GREEN
    p1.space_after = Pt(6)

    p2 = tf.add_paragraph()
    p2.text = mdesc
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_TEXT_MUTED


# ==========================================
# SLIDE 12: ĐỘT PHÁ QUẢN LÝ SẢN PHẨM (ADVANCED PRODUCT MANAGEMENT)
# ==========================================
s12 = prs.slides.add_slide(blank_layout)
set_slide_background(s12, COLOR_CREAM_BG)
add_header(s12, "Quản Trị Sản Phẩm", "Đột Phá Trong Thao Tác Thêm, Sửa, Xóa & Xem Trước Ảnh", "Giao diện 2 cột thông minh với khung Live Preview tỷ lệ vàng 4:3, Color Picker và Modal xóa an toàn.")
add_footer(s12, 12)

create_card(s12, Inches(0.8), Inches(1.9), card_half_w, card_half_h)
tx_pm = s12.shapes.add_textbox(Inches(1.1), Inches(2.1), card_half_w - Inches(0.6), card_half_h - Inches(0.4))
tf_pm = tx_pm.text_frame
tf_pm.word_wrap = True

p_pmt = tf_pm.paragraphs[0]
p_pmt.text = "Tính Năng Quản Trị Vừa Được Hoàn Thiện"
p_pmt.font.name = FONT_TITLE
p_pmt.font.size = Pt(15)
p_pmt.font.bold = True
p_pmt.font.color.rgb = COLOR_TEXT_MAIN
p_pmt.space_after = Pt(8)

p_adv = [
    ("Live Preview Ảnh Thời Gian Thực", "Khi admin dán URL hoặc chọn file từ máy, khung xem trước 4:3 cập nhật ảnh ngay lập tức mà không cần tải lại trang."),
    ("Hỗ Trợ Đa Định Dạng Nguồn Ảnh", "Chấp nhận cả 2 cách: tải file ảnh máy tính (JPG/PNG/WebP) HOẶC nhập link ảnh online trực tiếp."),
    ("Tự Động Sinh Biến Thể Size & Tồn Kho", "Khi tạo sản phẩm mới, hệ thống tự động sinh 5 kích cỡ (S, M, L, XL, 2XL) kèm tồn kho 30 cái để bán được ngay."),
    ("Huy Hiệu & Chấm Màu Nhận Diện", "Tùy biến nhanh huy hiệu (Best-seller, Mới, Hot) và bảng chọn màu Color Picker tương tác 2 chiều."),
    ("Xác Nhận Xóa Bằng Modal Popup", "Ngăn chặn hoàn toàn thao tác xóa nhầm sản phẩm nhờ hộp thoại Alpine.js xác nhận an toàn.")
]

for tit, des in p_adv:
    p_it = tf_pm.add_paragraph()
    p_it.text = f"• {tit}: "
    p_it.font.name = FONT_BODY
    p_it.font.size = Pt(9.5)
    p_it.font.bold = True
    p_it.font.color.rgb = COLOR_GREEN
    
    p_it_d = tf_pm.add_paragraph()
    p_it_d.text = f"  {des}"
    p_it_d.font.name = FONT_BODY
    p_it_d.font.size = Pt(9)
    p_it_d.font.color.rgb = COLOR_TEXT_MUTED
    p_it_d.space_after = Pt(3)

# Right: Product Sample Showcase
create_card(s12, Inches(6.85), Inches(1.9), card_half_w, card_half_h)
prod_sample = os.path.join(BASE_DIR, "static", "images", "products", "ao-thun-heavyweight-trang.jpg")
if os.path.exists(prod_sample):
    s12.shapes.add_picture(prod_sample, Inches(7.5), Inches(2.2), width=Inches(4.35))

tx_ps = s12.shapes.add_textbox(Inches(7.1), Inches(5.8), card_half_w - Inches(0.5), Inches(0.6))
tf_ps = tx_ps.text_frame
p_ps = tf_ps.paragraphs[0]
p_ps.text = "Ảnh sản phẩm tỷ lệ 4:3 thực tế sắc nét: Áo thun Heavyweight 100% Cotton (219.000₫)"
p_ps.font.name = FONT_BODY
p_ps.font.size = Pt(9.5)
p_ps.font.color.rgb = COLOR_TEXT_MUTED
p_ps.alignment = PP_ALIGN.CENTER


# ==========================================
# SLIDE 13: SERVERLESS & TỐI ƯU HÓA LƯU TRỮ (SERVERLESS ARCHITECTURE)
# ==========================================
s13 = prs.slides.add_slide(blank_layout)
set_slide_background(s13, COLOR_CREAM_BG)
add_header(s13, "Giải Pháp Đám Mây", "Kiến Trúc Serverless & Khắc Phục Read-Only Filesystem", "Bài toán vận hành Django trên nền tảng AWS Lambda / Vercel Serverless và các sáng kiến kỹ thuật then chốt.")
add_footer(s13, 13)

sv_cards = [
    {
        "title": "Thách Thức Read-Only Filesystem",
        "tag": "Vercel / Lambda Constraint",
        "prob": "Trên Vercel, toàn bộ thư mục mã nguồn /var/task là Read-only. Khi admin tải ảnh lên, Django mặc định cố ghi vào ổ cứng gây lỗi OSError Errno 30.",
        "sol": "Giải pháp: Viết hàm process_uploaded_image sử dụng Pillow nén và mã hóa ảnh trực tiếp thành Base64 Data URL, lưu thẳng vào trường TextField của Database. Không ghi ổ cứng."
    },
    {
        "title": "Thách Thức Mất Phiên Đăng Nhập",
        "tag": "Stateless Session Bug",
        "prob": "Mỗi request đến Vercel có thể được phục vụ bởi một container Lambda khác nhau. Session lưu trong file SQLite bị phân mảnh gây vòng lặp đăng nhập liên tục.",
        "sol": "Giải pháp: Chuyển toàn bộ SessionEngine sang signed_cookies. Phiên đăng nhập được ký mật mã bí mật và lưu ở cookie client, đảm bảo duy trì đăng nhập vĩnh viễn trên mọi container."
    },
    {
        "title": "Tối Ưu Tài Nguyên Tĩnh WhiteNoise",
        "tag": "Static Asset CDN",
        "prob": "Tài nguyên ảnh, CSS, JS cần được phục vụ với độ trễ thấp và băng thông tối thiểu mà không cần duy trì web server Nginx riêng biệt.",
        "sol": "Giải pháp: Sử dụng WhiteNoise CompressedStaticFilesStorage tự động gzip/brotli toàn bộ tài nguyên tĩnh, tích hợp cache-control bất biến."
    }
]

for idx, sc in enumerate(sv_cards):
    x = Inches(0.8 + idx * 4.03)
    create_card(s13, x, Inches(1.9), card_w, Inches(4.7))
    
    tx = s13.shapes.add_textbox(x + Inches(0.25), Inches(2.1), card_w - Inches(0.5), Inches(4.3))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    p1.text = sc["title"]
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_MAIN

    p2 = tf.add_paragraph()
    p2.text = sc["tag"].upper()
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_GOLD
    p2.space_after = Pt(10)

    p3 = tf.add_paragraph()
    p3.text = "Vấn đề thực tế:"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(10)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(190, 50, 50)

    p3_d = tf.add_paragraph()
    p3_d.text = sc["prob"]
    p3_d.font.name = FONT_BODY
    p3_d.font.size = Pt(9)
    p3_d.font.color.rgb = COLOR_TEXT_MUTED
    p3_d.space_after = Pt(10)

    p4 = tf.add_paragraph()
    p4.text = "Sáng kiến giải quyết:"
    p4.font.name = FONT_BODY
    p4.font.size = Pt(10)
    p4.font.bold = True
    p4.font.color.rgb = COLOR_GREEN

    p4_d = tf.add_paragraph()
    p4_d.text = sc["sol"]
    p4_d.font.name = FONT_BODY
    p4_d.font.size = Pt(9)
    p4_d.font.color.rgb = COLOR_TEXT_MUTED


# ==========================================
# SLIDE 14: BẢO MẬT & KIỂM THỬ (SECURITY & TESTING SUITE)
# ==========================================
s14 = prs.slides.add_slide(blank_layout)
set_slide_background(s14, COLOR_CREAM_BG)
add_header(s14, "Chất Lượng Kỹ Thuật", "Hệ Thống Bảo Mật & Bộ Kiểm Thử Tự Động (Testing Suite)", "Tuân thủ nghiêm ngặt chuẩn bảo mật Django, 100% ca kiểm thử Smoke & Integration Tests vượt qua thành công.")
add_footer(s14, 14)

create_card(s14, Inches(0.8), Inches(1.9), card_half_w, card_half_h)
tx_sec = s14.shapes.add_textbox(Inches(1.1), Inches(2.1), card_half_w - Inches(0.6), card_half_h - Inches(0.4))
tf_sec = tx_sec.text_frame
tf_sec.word_wrap = True

p_st = tf_sec.paragraphs[0]
p_st.text = "Các Lớp Phòng Thủ Bảo Mật"
p_st.font.name = FONT_TITLE
p_st.font.size = Pt(15)
p_st.font.bold = True
p_st.font.color.rgb = COLOR_TEXT_MAIN
p_st.space_after = Pt(10)

sec_items = [
    ("CSRF Protection", "Tất cả biểu mẫu POST trong Studio, Giỏ hàng và Admin đều được bảo vệ bằng CSRF token chống giả mạo request."),
    ("Chống SQL Injection", "Sử dụng 100% Django ORM Parameterized Queries, triệt tiêu nguy cơ tiêm mã độc vào cơ sở dữ liệu."),
    ("XSS Sanitization", "Tất cả chuỗi văn bản thiết kế và dữ liệu khách hàng được encode tự động trước khi xuất ra HTML templates."),
    ("Bảo Mật Tải File 10MB", "Kiểm tra kích thước file và MIME-type ở tầng controller trước khi xử lý, ngăn chặn tấn công DoS tải file rác.")
]

for sname, sdet in sec_items:
    p_item = tf_sec.add_paragraph()
    p_item.text = f"• {sname}: "
    p_item.font.name = FONT_BODY
    p_item.font.size = Pt(10)
    p_item.font.bold = True
    p_item.font.color.rgb = COLOR_GREEN

    p_item_d = tf_sec.add_paragraph()
    p_item_d.text = f"  {sdet}"
    p_item_d.font.name = FONT_BODY
    p_item_d.font.size = Pt(9.5)
    p_item_d.font.color.rgb = COLOR_TEXT_MUTED
    p_item_d.space_after = Pt(4)

# Right: Testing Report Card
create_card(s14, Inches(6.85), Inches(1.9), card_half_w, card_half_h)
tx_tst = s14.shapes.add_textbox(Inches(7.15), Inches(2.1), card_half_w - Inches(0.6), card_half_h - Inches(0.4))
tf_tst = tx_tst.text_frame
tf_tst.word_wrap = True

p_tt = tf_tst.paragraphs[0]
p_tt.text = "Kết Quả Kiểm Thử Hệ Thống (Automated Tests)"
p_tt.font.name = FONT_TITLE
p_tt.font.size = Pt(15)
p_tt.font.bold = True
p_tt.font.color.rgb = COLOR_TEXT_MAIN
p_tt.space_after = Pt(10)

test_results = [
    ("Trang Chủ & Trang Mẫu (/ & /mau-co-san/)", "Status 200 OK — Render đủ 22 sản phẩm chuẩn tỷ lệ 4:3"),
    ("Nếp Studio Canvas (/studio/)", "Status 200 OK — Load đủ 5 phôi áo & tọa độ khổ in"),
    ("API Gợi Ý Kích Cỡ (/api/calculate-size/)", "Status 200 OK — Match chính xác size theo nhân trắc"),
    ("Quản Trị Thêm/Sửa/Xóa Sản Phẩm", "Status 302/200 — Thêm mới, sửa giá, đổi ảnh không lỗi"),
    ("Phiên Đăng Nhập Signed Cookies", "Status 302 -> 200 — Giữ phiên đăng nhập không vòng lặp")
]

for tname, tres in test_results:
    pt1 = tf_tst.add_paragraph()
    pt1.text = f"✓ {tname}"
    pt1.font.name = FONT_BODY
    pt1.font.size = Pt(10)
    pt1.font.bold = True
    pt1.font.color.rgb = COLOR_GREEN

    pt2 = tf_tst.add_paragraph()
    pt2.text = f"  Kết quả: {tres}"
    pt2.font.name = FONT_BODY
    pt2.font.size = Pt(9)
    pt2.font.color.rgb = COLOR_TEXT_MUTED
    pt2.space_after = Pt(5)


# ==========================================
# SLIDE 15: LỘ TRÌNH PHÁT TRIỂN (ROADMAP)
# ==========================================
s15 = prs.slides.add_slide(blank_layout)
set_slide_background(s15, COLOR_CREAM_BG)
add_header(s15, "Tương Lai & Mở Rộng", "Lộ Trình Phát Triển Sản Phẩm (Product Roadmap)", "Chiến lược nâng cấp công nghệ 3D, ứng dụng Trí Tuệ Nhân Tạo và mở rộng mạng lưới xưởng in toàn quốc.")
add_footer(s15, 15)

phases = [
    {
        "phase": "GIAI ĐOẠN 1 (HIỆN TẠI)",
        "state": "ĐÃ HOÀN THÀNH 100%",
        "color": COLOR_GREEN,
        "items": [
            "Hoàn thiện Nếp Studio 2D Canvas hai mặt áo",
            "Hệ thống Catalog 22 sản phẩm may sẵn",
            "Bộ tính toán size áo thông minh theo dáng người",
            "Cổng quản trị Nếp Admin Portal toàn diện",
            "Triển khai đám mây Vercel & đồng bộ GitHub"
        ]
    },
    {
        "phase": "GIAI ĐOẠN 2 (QUÝ TIẾP THEO)",
        "state": "ĐANG TRIỂN KHAI",
        "color": COLOR_GOLD,
        "items": [
            "Tích hợp Mockup 3D tương tác xoay 360 độ (Three.js)",
            "AI Assistant gợi ý câu chữ & phong cách typography",
            "Tính năng xóa phông ảnh tự động khi tải lên",
            "Cổng thanh toán tự động VietQR Pro xác nhận 1s",
            "Ứng dụng quản trị riêng cho thợ in tại xưởng"
        ]
    },
    {
        "phase": "GIAI ĐOẠN 3 (MỤC TIÊU DÀI HẠN)",
        "state": "KẾ HOẠCH TƯƠNG LAI",
        "color": RGBColor(70, 90, 120),
        "items": [
            "Mở rộng mạng lưới đối tác xưởng in tại 3 miền",
            "Định tuyến đơn tự động tới xưởng in gần khách nhất",
            "Webhook tích hợp trực tiếp bưu cục GHN / GHTK",
            "Chương trình đồng sáng tạo cho các nghệ sĩ Local",
            "Mở rộng sang các dòng sản phẩm phụ kiện & nón"
        ]
    }
]

for idx, ph in enumerate(phases):
    x = Inches(0.8 + idx * 4.03)
    create_card(s15, x, Inches(1.9), card_w, Inches(4.7))
    
    tx = s15.shapes.add_textbox(x + Inches(0.25), Inches(2.1), card_w - Inches(0.5), Inches(4.3))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    p1.text = ph["phase"]
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = ph["color"]

    p2 = tf.add_paragraph()
    p2.text = ph["state"]
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_MUTED
    p2.space_after = Pt(14)

    for itm in ph["items"]:
        pi = tf.add_paragraph()
        pi.text = f"• {itm}"
        pi.font.name = FONT_BODY
        pi.font.size = Pt(10)
        pi.font.color.rgb = COLOR_TEXT_MAIN
        pi.space_after = Pt(7)


# ==========================================
# SLIDE 16: TỔNG KẾT & Q&A (CONCLUSION - DARK THEME)
# ==========================================
s16 = prs.slides.add_slide(blank_layout)
set_slide_background(s16, COLOR_DARK_BG)

tx_c = s16.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(10.9), Inches(1.8))
tf_c = tx_c.text_frame
tf_c.word_wrap = True

p_c1 = tf_c.paragraphs[0]
p_c1.text = "CẢM ƠN QUÝ THẦY CÔ & HỘI ĐỒNG LẮNG NGHE"
p_c1.font.name = FONT_BODY
p_c1.font.size = Pt(12)
p_c1.font.bold = True
p_c1.font.color.rgb = COLOR_GOLD
p_c1.space_after = Pt(8)

p_c2 = tf_c.add_paragraph()
p_c2.text = "Nếp Form — Một Nếp Áo, Một Nét Riêng."
p_c2.font.name = FONT_TITLE
p_c2.font.size = Pt(32)
p_c2.font.bold = True
p_c2.font.color.rgb = COLOR_WHITE
p_c2.space_after = Pt(12)

p_c3 = tf_c.add_paragraph()
p_c3.text = "Dự án đã khẳng định tính khả thi của mô hình POD tự động hóa, kết hợp hoàn hảo giữa kỹ thuật lập trình hiện đại và trải nghiệm thời trang tinh tế."
p_c3.font.name = FONT_BODY
p_c3.font.size = Pt(12)
p_c3.font.color.rgb = RGBColor(190, 195, 185)

# Links & Contact Box
create_card(s16, Inches(1.2), Inches(4.3), Inches(10.9), Inches(2.2), bg_color=COLOR_DARK_CARD, border_color=RGBColor(50, 70, 55))
tx_inf = s16.shapes.add_textbox(Inches(1.5), Inches(4.5), Inches(10.3), Inches(1.8))
tf_inf = tx_inf.text_frame
tf_inf.word_wrap = True

p_ititle = tf_inf.paragraphs[0]
p_ititle.text = "THÔNG TIN TRẢI NGHIỆM HỆ THỐNG & LIÊN HỆ DỰ ÁN"
p_ititle.font.name = FONT_BODY
p_ititle.font.size = Pt(11)
p_ititle.font.bold = True
p_ititle.font.color.rgb = COLOR_GOLD
p_ititle.space_after = Pt(8)

contacts = [
    "• GitHub Repository Mã Nguồn: https://github.com/duyminh12a/clothes-shop (Branch main)",
    "• Phiên Bản Live Demo Trên Vercel: https://clothes-shop-dun-two.vercel.app",
    "• Cổng Quản Trị Hệ Thống: /quan-tri/san-pham/  (Tài khoản: admin / admin123)",
    "• Sẵn sàng giải đáp mọi câu hỏi và nhận xét chuyên môn từ hội đồng (Q&A Session)."
]

for c in contacts:
    pc = tf_inf.add_paragraph()
    pc.text = c
    pc.font.name = FONT_BODY
    pc.font.size = Pt(10.5)
    pc.font.color.rgb = COLOR_CREAM_BG
    pc.space_after = Pt(4)

# Lưu bài thuyết trình
prs.save(OUTPUT_FILE)
print(f"Presentation created successfully: {OUTPUT_FILE}")
print(f"Total slides: {len(prs.slides)}")
