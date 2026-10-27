from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.cache import cache
from .forms import UserRegisterForm, UserLoginForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # لاگین خودکار کاربر جدید
            
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('stores:store_list')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        # ۲. استفاده از UserLoginForm به جای AuthenticationForm
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            # ۱. ذخیره موقت سبد خریدِ زمان مهمانی (قبل از لاگین)
            guest_cart = request.session.get('cart', {})
            
            login(request, user)
            
            # ۲. بازیابی سبد خرید ذخیره‌شده‌ی قبلی این کاربر از کش
            user_cart_key = f'cart_user_{user.id}'
            saved_cart = cache.get(user_cart_key, {})
            
            # ۳. ادغام هوشمند سبد خرید مهمان و سبد خرید قبلی کاربر
            final_cart = saved_cart.copy() # ابتدا سبد خرید قبلی کاربر را پایه قرار می‌دهیم
            
            if guest_cart:
                for product_id, item in guest_cart.items():
                    if product_id in final_cart:
                        # اگر محصول از قبل در سبد کاربر بود، تعدادش را با هم جمع می‌کنیم
                        final_cart[product_id]['quantity'] += item['quantity']
                    else:
                        # اگر محصول جدیدی است، آن را به سبد اضافه می‌کنیم
                        final_cart[product_id] = item
            
            # ۴. قرار دادن سبد نهایی در سشن و ذخیره در کش
            request.session['cart'] = final_cart
            if final_cart:
                cache.set(user_cart_key, final_cart, timeout=86400 * 30) # اعتبار ۳۰ روزه
            
            # هدایت کاربر پس از ورود
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('stores:store_list')
    else:
        # ۳. اینجا هم برای حالت GET از فرم سفارشی استفاده می‌کنیم
        form = UserLoginForm()
        
    return render(request, 'accounts/login.html', {'form': form})
def logout_view(request):
    if request.user.is_authenticated:
        # ۳. ذخیره سبد خرید در Cache (چون سشن با لاگ‌اوت کاملاً پاک می‌شود)
        if 'cart' in request.session:
            user_cart_key = f'cart_user_{request.user.id}'
            # ذخیره امن سبد خرید در حافظه موقت سرور بر اساس آیدی کاربر
            cache.set(user_cart_key, request.session['cart'], timeout=86400 * 30)
            
    logout(request)
    return redirect('stores:store_list')