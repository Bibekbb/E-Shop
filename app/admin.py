from django.contrib import admin
from app.models import  Category, SubCategory, Product, Contact_us, Order, Brand
# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(Contact_us)
admin.site.register(Order)
admin.site.register(Brand)
