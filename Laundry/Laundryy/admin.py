from django.contrib import admin
from .models import UserP, Category, Service, Order, Payment, Notification


admin.site.register(Category)
admin.site.register(UserP)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Notification)
# Register your models here.
