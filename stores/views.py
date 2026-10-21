from django.shortcuts import render
from .models import Store

def store_list(request):
    # دریافت تمامی فروشگاه‌ها از دیتابیس
    stores = Store.objects.all()
    return render(request, 'stores/store_list.html', {'stores': stores})