from django.urls import path
from . import views

app_name = 'studio'

urlpatterns = [
    path('', views.studio_view, name='index'),
    path('api/templates/', views.get_templates_api, name='api_templates'),
    path('api/stickers/', views.get_stickers_api, name='api_stickers'),
    path('api/upload-image/', views.upload_image_api, name='api_upload_image'),
    path('api/save-design/', views.save_design_api, name='api_save_design'),
]
