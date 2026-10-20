from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard_overview, name='overview'),
    path('don-hang/', views.order_list_view, name='orders'),
    path('don-hang/<str:order_code>/', views.order_detail_view, name='order_detail'),
    path('san-pham/', views.product_list_view, name='products'),
    path('san-pham/them/', views.product_create_view, name='product_create'),
    path('san-pham/<int:product_id>/sua/', views.product_edit_view, name='product_edit'),
    path('san-pham/<int:product_id>/xoa/', views.product_delete_view, name='product_delete'),
    path('san-pham/<int:product_id>/toggle-active/', views.product_toggle_active_api, name='product_toggle_active'),
    path('api/quick-update-stock/', views.quick_update_stock_api, name='quick_update_stock'),
    path('khuyen-mai/', views.coupon_list_view, name='coupons'),
    path('studio-mau/', views.templates_list_view, name='templates'),
    path('cai-dat/', views.settings_view, name='settings'),
]
