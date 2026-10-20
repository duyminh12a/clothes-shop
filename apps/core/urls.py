from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('ve-nep/', views.about_view, name='about'),
    path('faq/', views.faq_view, name='faq'),
    path('lien-he/', views.contact_view, name='contact'),
]
