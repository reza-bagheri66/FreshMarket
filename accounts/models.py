from django.db import models
from django.contrib.auth.models import User

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='کاربر')
    title = models.CharField(max_length=100, verbose_name='عنوان آدرس (مثلاً منزل، محل کار)')
    full_name = models.CharField(max_length=100, verbose_name='نام تحویل‌گیرنده')
    phone_number = models.CharField(max_length=15, verbose_name='شماره تماس گیرنده')
    province = models.CharField(max_length=50, verbose_name='استان')
    city = models.CharField(max_length=50, verbose_name='شهر')
    address = models.TextField(verbose_name='آدرس پستی دقیق')
    postal_code = models.CharField(max_length=10, verbose_name='کد پستی')
    is_default = models.BooleanField(default=False, verbose_name='آدرس پیش‌فرض')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.city})"