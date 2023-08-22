from django.contrib import admin
# from ecommerceweb.models import Customer,Product,Order,OrderItem,ShippingAddress
from .models import *

# # Register your models here.

admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Offers)