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
    cart.add(product=product)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True, 
            'product_name': product.name,
            'cart_total': len(cart)  # این خط جدید برای ارسال تعداد کل سبد خرید اضافه شود
        })
    
    # حالت پیش‌فرض (اگر کسی بدون جاوا اسکریپت درخواست فرستاد)
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