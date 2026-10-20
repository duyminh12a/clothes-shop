# 🧵 Nếp Form — Xưởng Áo Của Bạn

Nền tảng thiết kế áo thun, polo, hoodie và túi tote tùy biến trực tiếp, tích hợp hệ thống thương mại điện tử full-stack Django, công cụ vẽ trực quan Fabric.js, chương trình thành viên Nếp Club và bộ tính toán size áo thông minh.

---

## 🌟 Tính Năng Nổi Bật

1. **🎨 Nếp Studio (Fabric.js):**
   - Kéo thả, căn chỉnh chữ và hình vẽ tùy biến trên canvas.
   - Chuyển đổi mặt trước / mặt sau thời gian thực.
   - Thư viện mẫu thiết kế có sẵn và stickers nghệ thuật độc quyền.
   - Tải ảnh từ máy tính người dùng với kiểm tra an toàn.
   - Tùy chỉnh màu sắc áo (Kem, Trắng, Đen, Xanh rêu, Xám tiêu) với mockup sống động.
   - Tùy chọn khổ in (Nhỏ 15x18cm, Vừa 22x26cm, Lớn 30x35cm) kèm bảng giá tự động.

2. **📏 Bộ Tư Vấn Kích Cỡ Thông Minh (Size Calculator):**
   - Nhập Chiều cao (cm) và Cân nặng (kg) để gợi ý size chuẩn theo dáng người Việt.
   - Hiển thị tồn kho tức thời cho màu và size tương ứng.

3. **🛒 Thương Mại Điện Tử & Đặt Hàng:**
   - Giỏ hàng linh hoạt, thêm áo kèm hoặc không kèm bản thiết kế.
   - Áp dụng mã giảm giá (VD: `NEPFORM20` - giảm 20%, `NEP50K` - giảm 50.000₫).
   - Đa dạng phương thức thanh toán: COD, Chuyển khoản VietQR, VNPAY, MoMo, ZaloPay.

4. **🏆 Nếp Club (Loyalty Program):**
   - Tích 1 điểm cho mỗi 1.000₫ thanh toán.
   - Phân cấp hạng thành viên: Thường ➔ Bạc ➔ Vàng (giảm giá tới 10% trọn đời và Freeship).
   - Mã giới thiệu bạn bè nhận thưởng điểm 2 chiều.

5. **🛠️ Quản Trị Hệ Thống Toàn Diện:**
   - **Quản lý Trang phục & Phôi may sẵn (`/quan-tri/san-pham/`)**: Thêm mới, chỉnh sửa giá tiền, hình ảnh (tải file từ máy hoặc dán link URL với Live Preview 4:3), mô tả, chất liệu, phom dáng, huy hiệu (`Best-seller`, `Mới`, `Hot`), mã màu HEX và xóa sản phẩm an toàn.
   - **Quản trị đơn hàng & sản xuất**: Quản lý đơn hàng, duyệt trạng thái in ấn, thanh toán, xuất file in.
   - **Quản lý mã giảm giá, tồn kho biến thể và kho mẫu thiết kế Studio**.
   - Cung cấp song song cả **Dashboard Quản Trị Riêng (`/quan-tri/`)** và **Django Admin (`/admin/`)**.

---

## 🚀 Hướng Dẫn Khởi Chạy

### 1. Kích hoạt môi trường ảo:
```bash
# Windows PowerShell:
.venv\Scripts\activate
```

### 2. Chạy Server phát triển:
```bash
python manage.py runserver
```
Truy cập: `http://127.0.0.1:8000/`

---

## 🔑 Tài Khoản & Cổng Quản Trị Hệ Thống

1. **🌟 Trang Quản Trị Tùy Biến Riêng (Custom Dashboard UI):**
   - **Đường dẫn**: [http://127.0.0.1:8000/quan-tri/](http://127.0.0.1:8000/quan-tri/)
   - Giao diện trực quan hiện đại (TailwindCSS, KPI doanh thu, quản lý đơn hàng kèm file in, chỉnh nhanh tồn kho, tạo mã giảm giá, thêm mẫu Studio).

2. **⚙️ Trang Django Admin Mặc Định:**
   - **Đường dẫn**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
   - Đã được tùy biến tiêu đề, giao diện và cấu trúc bảng chuyên nghiệp.

- **Tên đăng nhập (Username)**: `admin`
- **Mật khẩu (Password)**: `admin123`
- **Email**: `admin@nepform.vn`


---

## 📁 Cấu Trúc Thư Mục

```
nep-form/
├── apps/
│   ├── core/         # Trang chủ, giới thiệu, câu hỏi, context processors
│   ├── accounts/     # Quản lý tài khoản, sổ địa chỉ, thiết kế đã lưu
│   ├── products/     # Danh mục sản phẩm, biến thể màu/size, size chart
│   ├── studio/       # Canvas Fabric.js, kho mẫu template, sticker
│   ├── cart/         # Giỏ hàng & coupon
│   ├── orders/       # Đơn hàng, thanh toán VietQR / VNPAY / MoMo
│   ├── loyalty/      # Nếp Club, điểm thưởng, mã giới thiệu
│   ├── blog/         # Bài viết & chia sẻ
│   └── cms/          # Banners, reviews, liên hệ
├── templates/        # Hệ thống giao diện HTML TailwindCSS & Alpine.js
├── static/           # Mockups SVG, CSS, JS
└── tests/            # Bộ kiểm thử tự động
```
