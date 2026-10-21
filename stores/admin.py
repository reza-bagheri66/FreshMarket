from django.contrib import admin
from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'neighborhood', 'owner', 'is_open', 'min_order_amount')
    list_filter = ('is_open', 'neighborhood')
    search_fields = ('name', 'neighborhood', 'phone_number')
    prepopulated_fields = {'slug': ('name',)}