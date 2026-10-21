from django.db import models
from django.contrib.auth.models import User
from stores.models import Store
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار پرداخت'),
        ('confirmed', 'تایید شده توسط فروشگاه'),
        ('sending', 'در حال ارسال'),
        ('delivered', 'تحویل داده شده'),
        ('cancelled', 'لغو شده'),
    )
    
    # اطلاعات ارتباطی سفارش
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="مشتی")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name="فروشگاه")
    
    # وضعیت و مبلغ
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت سفارش")
    total_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="مبلغ کل (تومان)")
    
    # اطلاعات ارسال
    address = models.TextField(verbose_name="آدرس تحویل گیرنده")
    phone_number = models.CharField(max_length=15, verbose_name="شماره تماس")
    
    # تاریخ ثبت
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت سفارش")

    def __str__(self):
        return f"سفارش #{self.id} - {self.user.username} ({self.get_status_display()})"

class OrderItem(models.Model):
    # اقلام موجود در هر سفارش
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="سفارش")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت در زمان خرید")
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")

    def __str__(self):
        return f"{self.quantity} عدد از {self.product.name} در سفارش #{self.order.id}"