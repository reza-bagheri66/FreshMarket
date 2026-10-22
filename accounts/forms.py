from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

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