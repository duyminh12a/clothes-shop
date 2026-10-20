from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('mau-co-san/', views.catalog_view, name='catalog'),
    path('san-pham/<slug:slug>/', views.product_detail_view, name='detail'),
    path('api/calculate-size/', views.calculate_size_api, name='calculate_size_api'),
]
