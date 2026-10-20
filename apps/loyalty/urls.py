from django.urls import path
from . import views

app_name = 'loyalty'

urlpatterns = [
    path('nep-club/', views.nep_club_view, name='club'),
]
