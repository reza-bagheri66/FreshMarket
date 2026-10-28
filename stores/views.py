from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from .forms import ProductForm, StoreRegisterForm
from .models import Product, Store


def store_list(request):
  query = request.GET.get('q')
  stores = Store.objects.filter(is_active=True)
  products = None

  # اگر کاربر چیزی جستجو کرده بود، محصولات تمام فروشگاه‌ها را فیلتر کن
  if query:
    products = Product.objects.filter(store__is_active=True).filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )

  context = {
      'stores': stores,
      'products': products,
      'query': query,
  }
  return render(request, 'stores/store_list.html', context)


def store_detail(request, slug):
  # نمایش جزئیات فروشگاه بر اساس slug
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
  products = store.products.all()

  context = {
      'store': store,
      'products': products,
  }
  return render(request, 'stores/vendor_dashboard.html', context)


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


def product_detail(request, product_id):
  # نمایش صفحه جزئیات محصول (مورد نیاز برای سبد خرید)
  product = get_object_or_404(Product, id=product_id, is_active=True)
  related_products = Product.objects.filter(
      store=product.store, is_active=True
  ).exclude(id=product.id)[:4]

  context = {
      'product': product,
      'related_products': related_products,
  }
  return render(request, 'stores/product_detail.html', context)


@login_required
def product_edit(request, product_id):
  # بررسی اینکه محصول حتماً متعلق به فروشگاه کاربر جاری باشد
  product = get_object_or_404(
      Product, id=product_id, store__owner=request.user
  )

  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES, instance=product)
    if form.is_valid():
      form.save()
      return redirect('stores:vendor_dashboard')
  else:
    form = ProductForm(instance=product)

  context = {
      'form': form,
      'product': product,
  }
  return render(request, 'stores/product_edit.html', context)