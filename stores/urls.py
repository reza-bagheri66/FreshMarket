from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('', views.store_list, name='store_list'),
    path('register/', views.store_register, name='store_register'),  # مسیر ثبت‌نام فروشگاه
    path('store/<slug:slug>/', views.store_detail, name='store_detail'),  # مسیر جدید
]