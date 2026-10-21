from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from stores.models import Store

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # پیدا کردن فروشگاه (در حال فرض می‌کنیم همه اقلام سبد خرید از یک فروشگاه هستند)
            store = None
            for item in cart:
                store = item['product'].store
                break
            
            if store:
                order = form.save(commit=False)
                order.store = store
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