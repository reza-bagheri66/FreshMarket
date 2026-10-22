from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .models import Store, Product
from .forms import StoreRegisterForm, ProductForm

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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StoreRegisterForm
from .models import Store

@login_required
def store_register(request):
    # اگر کاربر از قبل فروشگاه ثبت کرده، هدایتش می‌کنیم به داشبورد خودش
    if Store.objects.filter(owner=request.user).exists():
        return redirect('stores:vendor_dashboard')

    if request.method == 'POST':
        form = StoreRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user  # کاربر جاری به عنوان مالک ثبت می‌شود
            store.save()
            return redirect('stores:vendor_dashboard')
    else:
        form = StoreRegisterForm()

    return render(request, 'stores/store_register.html', {'form': form})

   
@login_required
def vendor_dashboard(request):
    # بررسی اینکه آیا کاربر لاگین‌شده صاحب فروشگاهی هست یا خیر
    try:
        store = Store.objects.get(owner=request.user)
    except Store.DoesNotExist:
        # اگر فروشگاه نداشت، به صفحه ثبت‌نام هدایت می‌شود
        return redirect('stores:store_register')

    # دریافت لیست محصولات فروشگاه
    products = store.products.all()  # یا store.product_set.all() بر اساس مدل Product شما

    context = {
        'store': store,
        'products': products,
    }
    return render(request, 'stores/vendor_dashboard.html', context)

@login_required
def add_product(request):
    store = get_object_or_404(Store, owner=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            return redirect('stores:vendor_dashboard')
    else:
        form = ProductForm()
        
    return render(request, 'stores/add_product.html', {'form': form, 'store': store})