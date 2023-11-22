from django.contrib import admin
from .models import Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "inventory", "created_at", "updated_at", "is_available")


admin.site.register(Product, ProductAdmin)