from django.db import models
import datetime
from django.contrib.auth.models import User

from django.conf import settings
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='static/images/')

    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE,related_name='products')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="customers")
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=250, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
