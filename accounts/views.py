from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # لاگین خودکار کاربر جدید
            
            # بررسی اینکه آیا از صفحه خاصی هدایت شده است یا خیر
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
                
            # اگر از جای خاصی نیامده بود، به صفحه اصلی سایت می‌رود
            return redirect('stores:store_list')
    else:
        form = UserRegisterForm()
        
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # بررسی پارامتر next برای بازگشت به صفحه قبلی
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
                
            # بازگشت به صفحه اصلی سایت به عنوان پیش‌فرض
            return redirect('stores:store_list')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('stores:store_list') # پس از خروج، کاربر به صفحه اصلی هدایت می‌شود