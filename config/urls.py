from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Tùy biến giao diện Django Admin mặc định cho đẹp và chuẩn thương hiệu
admin.site.site_header = "Nếp Form — Quản Trị Hệ Thống"
admin.site.site_title = "Nếp Form Admin"
admin.site.index_title = "Bảng điều khiển quản lý xưởng may & bán hàng"

urlpatterns = [
    # 1. Trang quản trị tùy biến riêng biệt (Custom Management Portal)
    path('quan-tri/', include('admin_panel.urls', namespace='admin_panel')),

    # 2. Django Admin mặc định (đã được đổi tên & tinh chỉnh)
    path('admin/', admin.site.urls),

    # 3. Các ứng dụng bán hàng & Studio khách hàng
    path('', include('core.urls', namespace='core')),
    path('studio/', include('studio.urls', namespace='studio')),
    path('', include('products.urls', namespace='products')),
    path('gio-hang/', include('cart.urls', namespace='cart')),
    path('don-hang/', include('orders.urls', namespace='orders')),
    path('tai-khoan/', include('accounts.urls', namespace='accounts')),
    path('', include('loyalty.urls', namespace='loyalty')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
