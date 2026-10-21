from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .models import Store
from .forms import StoreRegistrationForm

def store_list(request):
    # نمایش لیست فروشگاه‌های تایید شده
    stores = Store.objects.filter(is_active=True)
    return render(request, 'stores/store_list.html', {'stores': stores})

def store_detail(request, slug):
    # نمایش جزئیات یک فروشگاه خاص بر اساس slug
    store = get_object_or_404(Store, slug=slug, is_active=True)
    
    # دریافت محصولات مربوط به این فروشگاه
    # (اگر در مدل Product کلید خارجی با related_name='products' به Store متصل شده است)
    products = store.products.all()  # اگر related_name ندارید، از store.product_set.all() استفاده کنید
    
    context = {
        'store': store,
        'products': products,
    }
    return render(request, 'stores/store_detail.html', context)

@login_required
def store_register(request):
    # ثبت‌نام مستقیم فروشگاه توسط فروشنده
    if request.method == 'POST':
        form = StoreRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user  # اختصاص کاربر لاگین‌شده به عنوان صاحب فروشگاه
            store.is_active = False     # پیش‌فرض غیرفعال در انتظار تایید ادمین
            
            # تولید slug یکتا بر اساس نام فروشگاه
            base_slug = slugify(store.name, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Store.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            store.slug = slug
            
            store.save()
            return render(request, 'stores/store_register_done.html', {'store': store})
    else:
        form = StoreRegistrationForm()
    
    return render(request, 'stores/store_register.html', {'form': form})