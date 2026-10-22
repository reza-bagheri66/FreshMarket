from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('', views.store_list, name='store_list'),
    path('register/', views.store_register, name='store_register'),  # مسیر ثبت‌نام فروشگاه
    path('dashboard/', views.vendor_dashboard, name='vendor_dashboard'),  # مسیر جدید پنل فروشنده
    path('store/<slug:slug>/', views.store_detail, name='store_detail'),  # مسیر جدید
    path('dashboard/add-product/', views.add_product, name='add_product'),
]