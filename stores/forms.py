from django import forms
from .models import Store

class StoreRegistrationForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'neighborhood', 'address', 'phone_number', 'logo', 'min_order_amount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام فروشگاه'}),
            'neighborhood': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'محله (مثلاً سعادت‌آباد)'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'آدرس دقیق پستی'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تماس مسئول فروشگاه'}),
            'min_order_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'حداقل مبلغ سفارش (تومان)'}),
        }