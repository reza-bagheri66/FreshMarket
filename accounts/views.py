from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.core.cache import cache
from .forms import UserRegisterForm, UserLoginForm, UserProfileEditForm, UserAddressForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserAddress

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
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            # ذخیره موقت سبد خریدِ زمان مهمانی (قبل از لاگین)
            guest_cart = request.session.get('cart', {})
            
            login(request, user)
            
            # بازیابی سبد خرید ذخیره‌شده‌ی قبلی این کاربر از کش
            user_cart_key = f'cart_user_{user.id}'
            saved_cart = cache.get(user_cart_key, {})
            
            # ادغام هوشمند سبد خرید مهمان و سبد خرید قبلی کاربر
            final_cart = saved_cart.copy()
            
            if guest_cart:
                for product_id, item in guest_cart.items():
                    if product_id in final_cart:
                        final_cart[product_id]['quantity'] += item['quantity']
                    else:
                        final_cart[product_id] = item
            
            # قرار دادن سبد نهایی در سشن و ذخیره در کش
            request.session['cart'] = final_cart
            if final_cart:
                cache.set(user_cart_key, final_cart, timeout=86400 * 30)
            
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('stores:store_list')
    else:
        form = UserLoginForm()
        
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        if 'cart' in request.session:
            user_cart_key = f'cart_user_{request.user.id}'
            cache.set(user_cart_key, request.session['cart'], timeout=86400 * 30)
            
    logout(request)
    return redirect('stores:store_list')


@login_required
def profile_view(request):
    # فرم‌های پیش‌فرض
    form = UserProfileEditForm(instance=request.user)
    address_form = UserAddressForm()

    if request.method == 'POST':
        # ۱. ویرایش مشخصات شخصی
        if 'edit_profile_submit' in request.POST:
            form = UserProfileEditForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'اطلاعات شخصی با موفقیت به‌روزرسانی شد!')
                return redirect('accounts:profile')

        # ۲. ثبت آدرس جدید
        elif 'add_address_submit' in request.POST:
            address_form = UserAddressForm(request.POST)
            if address_form.is_valid():
                new_address = address_form.save(commit=False)
                new_address.user = request.user
                if new_address.is_default:
                    request.user.addresses.all().update(is_default=False)
                new_address.save()
                messages.success(request, 'آدرس جدید با موفقیت ثبت شد!')
                return redirect('accounts:profile')

        # ۳. ویرایش آدرس موجود (بخش جدید)
        elif 'edit_address_submit' in request.POST:
            address_id = request.POST.get('address_id')
            address_instance = get_object_or_404(UserAddress, id=address_id, user=request.user)
            edit_address_form = UserAddressForm(request.POST, instance=address_instance)
            if edit_address_form.is_valid():
                edited_address = edit_address_form.save(commit=False)
                if edited_address.is_default:
                    request.user.addresses.all().exclude(id=address_id).update(is_default=False)
                edited_address.save()
                messages.success(request, 'آدرس با موفقیت ویرایش شد!')
                return redirect('accounts:profile')

    addresses = request.user.addresses.all()

    context = {
        'addresses': addresses,
        'form': form,
        'address_form': address_form,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def delete_address(request, address_id):
    address = get_object_or_404(UserAddress, id=address_id, user=request.user)
    address.delete()
    messages.success(request, 'آدرس با موفقیت حذف شد.')
    return redirect('accounts:profile')