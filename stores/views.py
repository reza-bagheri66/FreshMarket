from django.shortcuts import render, get_object_or_404
from .models import Store

def store_list(request):
    # دریافت تمامی فروشگاه‌ها برای صفحه اصلی
    stores = Store.objects.all()
    return render(request, 'stores/store_list.html', {'stores': stores})

def store_detail(request, slug):
    # دریافت فروشگاه بر اساس slug یا نمایش ارور 404
    store = get_object_or_404(Store, slug=slug)
    # دریافت محصولات مربوط به همین فروشگاه
    products = store.products.all()
    
    context = {
        'store': store,
        'products': products,
    }
    return render(request, 'stores/store_detail.html', context)
    from django.shortcuts import render, get_object_or_404

def store_detail(request, slug):
    # دریافت فروشگاه بر اساس slug یا نمایش ارور 404
    store = get_object_or_404(Store, slug=slug)
    # دریافت محصولات مربوط به همین فروشگاه
    products = store.products.all()
    
    context = {
        'store': store,
        'products': products,
    }
    return render(request, 'stores/store_detail.html', context)