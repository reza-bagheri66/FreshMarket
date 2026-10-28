from django import forms
from .models import Product, Store


class StoreRegisterForm(forms.ModelForm):

  class Meta:
    model = Store
    fields = [
        'name',
        'slug',
        'neighborhood',
        'address',
        'phone_number',
        'logo',
        'min_order_amount',
    ]
    labels = {
        'name': 'نام فروشگاه',
        'slug': 'شناسه متنی (نام لاتین در آدرس URL)',
        'neighborhood': 'محله / منطقه',
        'address': 'آدرس دقیق',
        'phone_number': 'شماره تماس فروشگاه',
        'logo': 'لوگوی فروشگاه',
        'min_order_amount': 'حداقل مبلغ سفارش (تومان)',
    }
    widgets = {
        'name': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'مثلاً: سوپرمارکت بهار'}
        ),
        'slug': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'مثلاً: bahar-market'}
        ),
        'neighborhood': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'مثلاً: گلشهر'}
        ),
        'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        'phone_number': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '۰۹۱۲...'}
        ),
        'logo': forms.FileInput(attrs={'class': 'form-control'}),
        'min_order_amount': forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': '۰'}
        ),
    }


class ProductForm(forms.ModelForm):

  class Meta:
    model = Product
    # اضافه شدن category و stock به فیلدهای فرم
    fields = [
        'category',
        'name',
        'price',
        'stock',
        'description',
        'image',
        'is_active',
    ]
    labels = {
        'category': 'دسته‌بندی',
        'name': 'نام محصول',
        'price': 'قیمت (تومان)',
        'stock': 'تعداد موجودی در انبار',  # لیبل فیلد موجودی
        'description': 'توضیحات',
        'image': 'تصویر محصول',
        'is_active': 'فعال / نمایش در سایت',
    }
    widgets = {
        'category': forms.Select(attrs={'class': 'form-select'}),
        'name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'مثلاً: گوجه‌فرنگی تازه',
            }
        ),
        'price': forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'مثلاً: ۲۵۰۰۰'}
        ),
        'stock': forms.NumberInput(
            attrs={'class': 'form-control', 'min': '0', 'placeholder': 'مثلاً: ۵۰'}
        ),  # ویجت فیلد موجودی
        'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        'image': forms.FileInput(attrs={'class': 'form-control'}),
        'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    }