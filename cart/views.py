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
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1
        
    if quantity < 1:
        quantity = 1

    # بررسی مقدار فعلی این محصول در سبد خرید (به صورت ایمن برای جلوگیری از KeyError)
    current_quantity_in_cart = 0
    product_id_str = str(product.id)
    if product_id_str in cart.cart:
        current_quantity_in_cart = cart.cart[product_id_str].get('quantity', 0)
    
    total_requested = current_quantity_in_cart + quantity

    # بررسی موجودی انبار
    if total_requested > product.stock:
        error_msg = f'موجودی انبار کافی نیست. تنها {product.stock} عدد از این محصول موجود است.'
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': error_msg
            })
        messages.error(request, error_msg)
        return redirect(request.META.get('HTTP_REFERER', 'stores:store_list'))
    
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
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1
            
        if quantity > 0:
            # جلوگیری از آپدیت کردن به مقداری بیشتر از موجودی انبار
            if quantity > product.stock:
                messages.error(request, f'موجودی انبار کافی نیست. حداکثر مقدار قابل سفارش {product.stock} عدد است.')
                quantity = product.stock
                
            cart.add(product=product, quantity=quantity, override_quantity=True)
        else:
            cart.remove(product)
            
    return redirect('cart:cart_detail')