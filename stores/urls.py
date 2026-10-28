from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('', views.store_list, name='store_list'),
    path('register/', views.store_register, name='store_register'),  # مسیر ثبت‌نام فروشگاه
    path('dashboard/', views.vendor_dashboard, name='vendor_dashboard'),  # مسیر پنل فروشنده
    path('store/<slug:slug>/', views.store_detail, name='store_detail'), 
    path('dashboard/add-product/', views.add_product, name='add_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/edit/',views.product_edit,name='product_edit',),
]