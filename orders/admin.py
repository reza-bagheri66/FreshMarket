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
    list_display = ['id', 'user', 'first_name', 'last_name', 'phone_number', 'paid', 'created', 'get_total_cost_display']
    list_filter = ['paid', 'created']
    # search_fields موقتاً حذف شد
    inlines = [VendorOrderInline]

    @admin.display(description='مبلغ کل (تومان)')
    def get_total_cost_display(self, obj):
        return obj.get_total_cost()


@admin.register(VendorOrder)
class VendorOrderAdmin(admin.ModelAdmin):
    list_display = ['tracking_code', 'order', 'store', 'status', 'created', 'get_total_cost_display']
    list_filter = ['status', 'store', 'created']
    # search_fields موقتاً حذف شد
    inlines = [OrderItemInline]

    @admin.display(description='مبلغ کل (تومان)')
    def get_total_cost_display(self, obj):
        return obj.get_total_cost()