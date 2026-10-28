from django.db import models
from stores.models import Store
from stores.models import Product
from django.conf import settings

class Order(models.Model):
    """سفارش مادر (کل سبد خرید کاربر به عنوان یک تراکنش واحد)"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='orders', verbose_name='کاربر')
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    phone_number = models.CharField(max_length=15, verbose_name='شماره تماس')
    address = models.TextField(verbose_name='آدرس دقیق')
    
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    paid = models.BooleanField(default=False, verbose_name='پرداخت شده')

    class Meta:
        ordering = ['-created']
        verbose_name = 'سفارش مادر'
        verbose_name_plural = 'سفارش‌های مادر'

    def __str__(self):
        return f'سفارش مادر شماره {self.id}'

    def get_total_cost(self):
        # جمع کل مبلغ تمام مرسوله‌های این سفارش مادر
        return sum(sub_order.get_total_cost() for sub_order in self.vendor_orders.all())


class VendorOrder(models.Model):
    """زیرسفارش / مرسوله اختصاصی هر فروشگاه"""
    order = models.ForeignKey(Order, related_name='vendor_orders', on_delete=models.CASCADE, verbose_name='سفارش مادر')
    store = models.ForeignKey(Store, related_name='vendor_orders', on_delete=models.CASCADE, verbose_name='فروشگاه')
    
    STATUS_CHOICES = (
        ('pending', 'در حال بررسی'),
        ('processing', 'در حال آماده‌سازی'),
        ('shipped', 'ارسال شده'),
        ('completed', 'تحویل داده شده'),
        ('cancelled', 'لغو شده'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت مرسوله')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت') # اضافه شد

    class Meta:
        verbose_name = 'مرسوله فروشگاهی'
        verbose_name_plural = 'مرسوله‌های فروشگاهی'

    @property
    def tracking_code(self):
        vendor_orders = list(self.order.vendor_orders.all())
        try:
            index = vendor_orders.index(self) + 1
        except ValueError:
            index = 1
        # استفاده از اسلش و صفرِ پیشوند سه‌رقمی (مثلا 10/001)
        return f"{self.order.id}/{index:03d}"

    def __str__(self):
        return f"مرسوله {self.tracking_code} - فروشگاه {self.store.name}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """آیتم‌های داخل هر مرسوله فروشگاهی"""
    vendor_order = models.ForeignKey(VendorOrder, related_name='items', on_delete=models.CASCADE, verbose_name='مرسوله فروشگاهی')
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