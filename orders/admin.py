from django.contrib import admin
from .models import Order, VendorOrder, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ['product']


class VendorOrderInline(admin.TabularInline):
    model = VendorOrder
    extra = 0
    readonly_fields = ('store', 'status')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'phone_number', 'paid', 'created', 'get_total_cost']
    list_filter = ['paid', 'created']
    search_fields = ['first_name', 'last_name', 'phone_number', 'id']
    inlines = [VendorOrderInline]


@admin.register(VendorOrder)
class VendorOrderAdmin(admin.ModelAdmin):
    list_display = ['tracking_code', 'order', 'store', 'status', 'created', 'get_total_cost']
    list_filter = ['status', 'store', 'created']  # اینجارو چک کن که 'created' باشد نه created_at
    search_fields = ['order__id', 'store__name']
    inlines = [OrderItemInline]