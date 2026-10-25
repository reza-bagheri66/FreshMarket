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

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="اسلاگ / نام لاتین یا یکتا")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="تصویر دسته‌بندی")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products', verbose_name="فروشگاه")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name="دسته‌بندی")
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    description = models.TextField(blank=True, verbose_name="توضیحات محصول")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت (تومان)")
    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="تصویر محصول")
    is_active = models.BooleanField(default=True, verbose_name="فعال / موجود")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return f"{self.name} - {self.store.name}"