from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_category = models.CharField(max_length=50)
    product_price = models.DecimalField(max_digits=20, decimal_places=2)
    product_discount = models.DecimalField(max_digits=5, decimal_places=2)
    product_image = models.ImageField(upload_to='product_img')
    product_disc = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return str(self.product)
