from django.db import models
from django.contrib.auth.models import User
from stores.models import Product

class Cart(models.Model):
    # هر سبد خرید متعلق به یک کاربر است
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return f"سبد خرید {self.user.username}"

class CartItem(models.Model):
    # اقلام داخل سبد خرید
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="سبد خرید")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")

    def __str__(self):
        return f"{self.quantity} عدد از {self.product.name}"

    @property
    def total_price(self):
        """محاسبه قیمت کل برای این آیتم (تعداد × قیمت واحد محصول)"""
        return self.quantity * self.product.price