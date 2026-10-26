from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from stores.models import Store

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # پیدا کردن فروشگاه (در حال فرض میکنیم همه اقلام سبد خرید از یک فروشگاه هستند)
            store = None
            for item in cart:
                store = item['product'].store
                break
            
            if store:
                order = form.save(commit=False)
                order.store = store
                order.user = request.user  # ست کردن کاربر لاگین شده
                order.save()
                
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )
                
                # پاک کردن سبد خرید پس از ثبت سفارش
                cart.clear()
                return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
        
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

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