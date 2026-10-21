from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stores.urls')),  # صفحه اصلی سایت
    path('orders/', include('orders.urls')),
    path('cart/', include('cart.urls')), 
]