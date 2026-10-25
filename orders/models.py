from django.db import models
from stores.models import Store
from stores.models import Product
from django.conf import settings

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name='کاربر')
    STATUS_CHOICES = (
        ('pending', 'در حال بررسی'),
        ('processing', 'در حال آماده‌سازی'),
        ('shipped', 'ارسال شده'),
        ('completed', 'تحویل داده شده'),
    )
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    phone_number = models.CharField(max_length=15, verbose_name='شماره تماس')
    address = models.TextField(verbose_name='آدرس دقیق')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders', verbose_name='فروشگاه')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    paid = models.BooleanField(default=False, verbose_name='پرداخت شده')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت سفارش')

    class Meta:
        ordering = ['-created']
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش‌ها'

    def __str__(self):
        return f'سفارش شماره {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='سفارش')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='محصول')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='قیمت واحد')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity


