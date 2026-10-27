from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

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