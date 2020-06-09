from django.db import models
from django.contrib.auth.models import User
from product.models import Product
# Create your models here.


class Order(models.Model):
    orderid = models.CharField(max_length=20)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    shop_user = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default="notstarted")
    subtotal = models.DecimalField(default=0, max_digits=50, decimal_places=2)
    shipping = models.DecimalField(default=0, max_digits=50, decimal_places=2)
    finaltotal = models.DecimalField(default=0, max_digits=50, decimal_places=2)
    date = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0, max_digits=50, decimal_places=2)
    quantity = models.IntegerField()

