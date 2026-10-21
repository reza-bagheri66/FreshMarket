from django.contrib import admin
from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'neighborhood', 'owner', 'is_active', 'is_open', 'min_order_amount')
    list_editable = ('is_active',)  # امکان تایید یا رد سریع فروشگاه مستقیماً از جدول
    list_filter = ('is_active', 'is_open', 'neighborhood')
    search_fields = ('name', 'neighborhood', 'phone_number')
    prepopulated_fields = {'slug': ('name',)}