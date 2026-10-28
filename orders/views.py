from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, VendorOrder, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from stores.models import Store

@login_required
def order_create(request):
    cart = Cart(request)
    if not cart:
        return redirect('stores:store_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # ۱. ساخت «سفارش مادر» (یک فاکتور واحد برای کل سبد خرید)
            master_order = Order.objects.create(
                user=request.user,
                first_name=cd['first_name'],
                last_name=cd['last_name'],
                phone_number=cd['phone_number'],
                address=cd['address'],
                paid=False
            )

            # ۲. گروه‌بندی اقلام سبد خرید بر اساس فروشگاه
            cart_items_by_store = {}
            for item in cart:
                store = item['product'].store
                if store not in cart_items_by_store:
                    cart_items_by_store[store] = []
                cart_items_by_store[store].append(item)

            # ۳. ساخت «مرسوله‌های فروشگاهی» (VendorOrder) به ازای هر فروشگاه
            for store, items in cart_items_by_store.items():
                vendor_order = VendorOrder.objects.create(
                    order=master_order,
                    store=store,
                    status='pending'
                )

                for item in items:
                    OrderItem.objects.create(
                        vendor_order=vendor_order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )

            # ۴. هدایت به درگاه پرداخت با شناسه سفارش مادر
            return redirect('orders:simulate_payment', order_id=master_order.id)
    else:
        form = OrderCreateForm()
        
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


@login_required
def simulate_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'success':
            
            try:
                with transaction.atomic():
                    # ۱. بررسی موجودی انبار برای تمام اقلام سفارش
                    order_items = OrderItem.objects.filter(vendor_order__order=order).select_related('product')
                    
                    for item in order_items:
                        product = item.product
                        if product.stock < item.quantity:
                            raise ValueError(f'متأسفانه محصول «{product.name}» در حین خرید شما به اتمام رسید یا موجودی آن کافی نیست.')

                    # ۲. کسر از انبار
                    for item in order_items:
                        product = item.product
                        product.stock -= item.quantity
                        product.save()

                    # ۳. ثبت پرداخت موفق
                    order.paid = True
                    order.save()
                    
                    order.vendor_orders.all().update(status='processing')

                # ۴. پاک کردن کل سبد خرید پس از پرداخت موفق و قطعی
                cart = Cart(request)
                cart.clear()
                
                return render(request, 'orders/order/created.html', {'order': order})

            except ValueError as e:
                # اگر موجودی کافی نبود، فقط کالاهای ناموجود را از سبد خرید پاک می‌کنیم
                cart = Cart(request)
                order_items = OrderItem.objects.filter(vendor_order__order=order).select_related('product')
                for item in order_items:
                    if item.product.stock < item.quantity:
                        cart.remove(item.product)

                error_msg = str(e)
                # ارسال مستقیم خطا به قالب بدون استفاده از سیستم messages جنگو
                return render(request, 'orders/order/payment_failed.html', {'order': order, 'error_message': error_msg})

        else:
            return render(request, 'orders/order/payment_failed.html', {'order': order})

    return render(request, 'orders/order/payment_gateway.html', {'order': order})


def order_track(request):
    order = None
    order_id = request.GET.get('order_id')
    if order_id:
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            order = None
    return render(request, 'orders/order/track.html', {'order': order})


@login_required(login_url='accounts:login')
def my_orders(request):
    # نمایش سفارش‌های مادر کاربر
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'orders/order/my_orders.html', {'orders': orders})


@login_required
def vendor_order_list(request, store_slug):
    # بررسی مالکیت فروشگاه توسط کاربر جاری
    store = get_object_or_404(Store, slug=store_slug, owner=request.user)
    
    # استخراج مرسوله‌های اختصاصی این فروشگاه با فیلتر دقیقِ store=store
    vendor_orders = VendorOrder.objects.filter(store=store).select_related('order', 'order__user', 'store').prefetch_related('items__product').order_by('-created')
    
    # تغییر وضعیت مرسوله توسط فروشنده
    if request.method == 'POST':
        vendor_order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        vendor_order = get_object_or_404(VendorOrder, id=vendor_order_id, store=store)
        if new_status in dict(VendorOrder.STATUS_CHOICES):
            vendor_order.status = new_status
            vendor_order.save()
            return redirect('orders:vendor_order_list', store_slug=store.slug)

    context = {
        'store': store,
        'orders': vendor_orders, # فقط مرسوله‌های مختصِ این فروشگاه نمایش داده می‌شوند
    }
    return render(request, 'orders/order/vendor_orders.html', context)


@login_required
def order_detail(request, order_id):
    # جزئیات سفارش مادر
    order = get_object_or_404(Order, id=order_id)
    
    # بررسی دسترسی (کاربر صاحب سفارش باشد یا صاحب حداقل یکی از فروشگاه‌های این سفارش)
    is_owner = order.user == request.user
    is_store_owner = order.vendor_orders.filter(store__owner=request.user).exists()
    
    if not is_owner and not is_store_owner:
        return redirect('stores:store_list')
        
    return render(request, 'orders/order/order_detail.html', {'order': order})


@login_required
def vendor_order_detail(request, vendor_order_id):
    # بررسی اینکه مرسوله متعلق به فروشگاه‌های خودِ این کاربر (فروشنده) باشد
    vendor_order = get_object_or_404(VendorOrder, id=vendor_order_id, store__owner=request.user)
    return render(request, 'orders/order/vendor_order_detail.html', {'vendor_order': vendor_order})