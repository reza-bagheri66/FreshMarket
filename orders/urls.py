from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('track/', views.order_track, name='order_track'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('vendor-orders/<slug:store_slug>/', views.vendor_order_list, name='vendor_order_list'),
]