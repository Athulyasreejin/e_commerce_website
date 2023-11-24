from django.db import models
from main.models import Product
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=12)
    email = models.EmailField(max_length=50)
    address = models.TextField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


    def __str__(self):
        return self.user.username
    


class CartItem(models.Model):
    item=models.ForeignKey(Product,on_delete=models.CASCADE)
    date=models.DateField(auto_now=True)
    quantity=models.IntegerField()
    price=models.FloatField()
    is_ordered=models.BooleanField(default=False)

    def total(self):
        return (self.quantity*self.item.price)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    items=models.ManyToManyField(CartItem)

def total(self):
        total_price = 0
        for cart_item in self.items.all():
            total_price += cart_item.total()
        return (total_price)