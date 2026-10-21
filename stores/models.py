from django.db import models
from django.contrib.auth.models import User

class Store(models.Model):
    # صاحب فروشگاه (هر فروشگاه یک مدیر/فروشنده دارد)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="صاحب فروشگاه")
    
    # اطلاعات اصلی فروشگاه
    name = models.CharField(max_length=200, verbose_name="نام فروشگاه")
    slug = models.SlugField(unique=True, verbose_name="شناسه یکتا (Slug)")
    neighborhood = models.CharField(max_length=100, verbose_name="محله")
    address = models.TextField(verbose_name="آدرس دقیق")
    phone_number = models.CharField(max_length=15, verbose_name="شماره تماس")

    is_active = models.BooleanField(default=False, verbose_name="تایید شده توسط ادمین") # این فیلد برای تایید فروشگاه است
    
    # تصاویر و وضعیت‌ها
    logo = models.ImageField(upload_to='stores/logos/', blank=True, null=True, verbose_name="لوگوی فروشگاه")
    is_open = models.BooleanField(default=True, verbose_name="وضعیت (باز / بسته)")
    
    # شرایط خرید و ارسال
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="حداقل مبلغ سفارش (تومان)")
    
    # تاریخ ایجاد
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    def __str__(self):
        return f"{self.name} ({self.neighborhood})"