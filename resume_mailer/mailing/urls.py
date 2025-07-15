from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_mailing, name='create_mailing'),
    path('success/', views.mailing_success, name='mailing_success'),
]
