from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import UserAddress

class UserLoginForm(AuthenticationForm):
    # فارسی‌سازی پیام‌های خطا
    error_messages = {
        'invalid_login': _("شماره موبایل یا رمز عبور اشتباه است. لطفاً دقت کنید."),
        'inactive': _("این حساب کاربری غیرفعال است."),
    }

class UserRegisterForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15,
        label='شماره موبایل',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً ۰۹۱۲۳۴۵۶۷۸۹'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        phone = self.cleaned_data['phone_number']
        user.username = phone  
        if commit:
            user.save()
        return user

class UserProfileEditForm(forms.ModelForm):
    # اضافه کردن فیلد شماره موبایل به صورت غیرقابل ویرایش در فرم پروفایل
    username = forms.CharField(
        label='شماره موبایل',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light', 
            'disabled': 'disabled',
            'readonly': 'readonly'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خود را وارد کنید'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی را وارد کنید'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@gmail.com'}),
        }
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'آدرس ایمیل',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # مقداردهی اولیه فیلد username با شماره موبایل فعلی کاربر هنگام باز شدن فرم
        if self.instance and self.instance.pk:
            self.fields['username'].initial = self.instance.username


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['title', 'full_name', 'phone_number', 'province', 'city', 'address', 'postal_code', 'is_default']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً منزل یا محل کار'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام و نام خانوادگی تحویل‌گیرنده'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره موبایل تماس'}),
            'province': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'استان'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شهر'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'آدرس پستی کامل'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد پستی ۱۰ رقمی'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

