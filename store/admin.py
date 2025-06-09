from django.contrib import admin
from .models import Product
from .models import Order, OrderItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    fields = ('name', 'price', 'benefits', 'description', 'key_ingredients', 'image')

admin.site.register(Product)

from .models import Category

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)

