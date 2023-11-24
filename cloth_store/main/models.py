from django.db import models
from django.contrib.auth.models import User

class Admin_Signup(models.Model):
    username = models.CharField(max_length=50, default='athu123')
    password = models.CharField(max_length=128, default='12345678')

# new_user = Admin_Signup()
# new_user.save()

# class Customer(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # phone = models.CharField(max_length=20)
    # address = models.TextField()

    # def _str_(self):
    #     return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    size= models.CharField(max_length=20)
    image = models.ImageField(upload_to='product_images/',blank=True)


    def __str__(self):
        return self.name
    
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.pk} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - Qty: {self.quantity}"