from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse 
from stores.models import Product
from .cart import Cart

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # خواندن تعداد انتخابی کاربر از فرم (پیش‌فرض ۱ است)
    quantity = int(request.POST.get('quantity', 1))
    
    # افزودن محصول همراه با تعداد دلخواه به سبد خرید
    cart.add(product=product, quantity=quantity)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'product_name': product.name,
            'cart_total': len(cart)
        })

    return redirect(request.META.get('HTTP_REFERER', 'stores:store_list'))

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart.add(product=product, quantity=quantity, override_quantity=True)
        else:
            cart.remove(product)
            
    return redirect('cart:cart_detail')