from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('thanh-toan/', views.checkout_view, name='checkout'),
    path('thanh-cong/<str:order_code>/', views.order_success_view, name='success'),
    path('don-hang-cua-toi/', views.my_orders_view, name='my_orders'),
]
