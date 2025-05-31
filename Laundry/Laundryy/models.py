# models.py
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class UserP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    def __str__(self):
        return f'{self.user.get_full_name()} ({self.phone})'

class Service(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    def __str__(self):
        return self.name

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Credit Card'),
        ('telebirr', 'TeleBirr'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f'Payment #{self.id} - {self.amount} ({self.method})'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    @property
    def total_price(self):
        return self.service.price * self.quantity

    def __str__(self):
        return f'Order #{self.id} - {self.service.name} x{self.quantity}'

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return f'Notification to {self.user.username}'