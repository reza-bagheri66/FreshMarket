from django.db import models
from stores.models import Store

class Product(models.Model):
    # ارتباط با فروشگاه (هر محصول متعلق به یک سوپرمارکت خاص است)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products', verbose_name="فروشگاه")
    
    # اطلاعات محصول
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    slug = models.SlugField(unique=True, verbose_name="شناسه یکتا (Slug)")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات محصول")
    
    # قیمت و موجودی
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت (تومان)")
    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی انبار")
    is_available = models.BooleanField(default=True, verbose_name="موجود / فعال")
    
    # تصویر محصول (چون Pillow را نصب کردیم، ImageField بدون مشکل کار می‌کند)
    image = models.ImageField(upload_to='products/images/', blank=True, null=True, verbose_name="تصویر محصول")
    
    # تاریخ ایجاد
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    def __str__(self):
        return f"{self.name} - {self.store.name}"