from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'price', 'stock', 'is_available')
    list_filter = ('is_available', 'store')
    search_fields = ('name', 'store__name')
    prepopulated_fields = {'slug': ('name',)}