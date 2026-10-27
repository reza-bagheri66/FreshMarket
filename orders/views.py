from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem, Order
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
            # ۱. گرفتن اطلاعات پاکسازی‌شده و معتبر از فرم
            cd = form.cleaned_data

            # ۲. گروه‌بندی اقلام سبد خرید بر اساس شناسه فروشگاه
            cart_items_by_store = {}
            for item in cart:
                store = item['product'].store
                store_id = store.id
                if store_id not in cart_items_by_store:
                    cart_items_by_store[store_id] = {'store': store, 'items': []}
                cart_items_by_store[store_id]['items'].append(item)

            first_order_id = None

            # ۳. ساخت سفارش‌های کاملاً مجزا و مستقل برای هر فروشگاه با استفاده از اطلاعات فرم
            for store_id, data in cart_items_by_store.items():
                store_obj = data['store']
                items = data['items']

                # ایجاد یک رکورد کاملاً جدید و جداگانه در جدول Order
                order = Order.objects.create(
                    user=request.user,
                    store=store_obj,
                    first_name=cd['first_name'],
                    last_name=cd['last_name'],
                    phone_number=cd['phone_number'],
                    address=cd['address'],
                    paid=False,
                    status='pending'
                )

                for item in items:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )
                
                if not first_order_id:
                    first_order_id = order.id

            # ۴. هدایت به درگاه پرداخت تستی با شناسه اولین سفارش
            return redirect('orders:simulate_payment', order_id=first_order_id)
    else:
        form = OrderCreateForm()
        
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


@login_required
def simulate_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'success':
            # ۴. پرداخت و فعالسازی همزمانِ تمام سفارش‌های معلقِ این کاربر در دیتابیس
            Order.objects.filter(user=request.user, paid=False).update(
                paid=True,
                status='processing'
            )
            
            # ۵. پاک کردن سبد خرید بعد از تایید نهایی پرداخت
            cart = Cart(request)
            cart.clear()
            
            return render(request, 'orders/order/created.html', {'order': order})
        else:
            # تراکنش ناموفق یا انصراف کاربر
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
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'orders/order/my_orders.html', {'orders': orders})


@login_required
def vendor_order_list(request, store_slug):
    # بررسی مالکیت فروشگاه توسط کاربر جاری
    store = get_object_or_404(Store, slug=store_slug, owner=request.user)
    
    # استفاده از کوئری مستقیم و ایمن برای استخراج سفارش‌های این فروشگاه خاص
    orders = Order.objects.filter(store=store).order_by('-created')
    
    # اگر فروشنده خواست وضعیت سفارش را تغییر دهد
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        order = get_object_or_404(Order, id=order_id, store=store)
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            return redirect('orders:vendor_order_list', store_slug=store.slug)

    context = {
        'store': store,
        'orders': orders,
    }
    return render(request, 'orders/order/vendor_orders.html', context)