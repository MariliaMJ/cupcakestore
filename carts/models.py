from dataclasses import dataclass
import uuid
from django.db import models
from store.models import Product

# Create your models here.


class Cart(models.Model):
    cart_id = models.UUIDField(primary_key=True, editable=False)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.cart_id)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.product.name


@dataclass
class CartView:
    cart_items: list
    total: float
