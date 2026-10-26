from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .models import Store, Product
from .forms import StoreRegisterForm, ProductForm
from django.db.models import Q

def store_list(request):
    query = request.GET.get('q')
    stores = Store.objects.filter(is_active=True)
    products = None
    
    # اگر کاربر چیزی جستجو کرده بود، محصولات تمام فروشگاه‌ها را فیلتر کن
    if query:
        products = Product.objects.filter(
            store__is_active=True
        ).filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        
    context = {
        'stores': stores,
        'products': products,
        'query': query,
    }
    return render(request, 'stores/store_list.html', context)

    
def store_detail(request, slug):
    # نمایش جزئیات فروشگاه بر اساس slug[cite: 3]
    store = get_object_or_404(Store, slug=slug, is_active=True)
    products = store.products.all()
    
    # دریافت کلمه جستجو شده از طریق متد GET
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    context = {
        'store': store,
        'products': products,
        'query': query,  # برای حفظ کلمه جستجو شده داخل باکس اینپوت
    }
    return render(request, 'stores/store_detail.html', context)


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


@login_required
def add_product(request):
    try:
        store = request.user.store
    except Store.DoesNotExist:
        return redirect('stores:store_register')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            return redirect('stores:vendor_dashboard')
    else:
        form = ProductForm()
    
    return render(request, 'stores/add_product.html', {'form': form})