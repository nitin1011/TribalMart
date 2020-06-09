from django.db import models
from django.contrib.auth.models import User
from product.models import Product
# Create your models here.


class CartItem(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    line_total = models.DecimalField(default=0, max_digits=50, decimal_places=2)

    def __str__(self):
        return str(self.product.product_name)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    item_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)
