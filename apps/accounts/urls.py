from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('dang-nhap/', views.login_view, name='login'),
    path('dang-ky/', views.register_view, name='register'),
    path('dang-xuat/', views.logout_view, name='logout'),
    path('thiet-ke-cua-toi/', views.my_designs_view, name='my_designs'),
    path('ho-so/', views.profile_view, name='profile'),
]
