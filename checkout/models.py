from enum import Enum
from django.utils import timezone
import uuid
from django.db import models

from app.models import Customer
from store.models import Product

# Create your models here.
class OrderStatus(Enum):
    PENDENTE = "Pendente"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDO = "Concluído"
    CANCELADO = "Cancelado"


class ItemOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    value = models.DecimalField(null=False, decimal_places=2, max_digits=10)
    value_total = models.DecimalField(null=False, decimal_places=2, max_digits=10)
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="itens")

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


class Order(models.Model):
    order_id = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False
    )
    order_number = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    data = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=[(status.name, status.value) for status in OrderStatus],
        default=OrderStatus.PENDENTE.value,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def items_order(self):
        item_descriptions = []
        for item in self.itens.all():
            description = f"{item.quantity}x {item.product.name}"
            item_descriptions.append(description)
        return ", ".join(item_descriptions)

    items_order.short_description = "Itens do Order"

    def address_customer(self):
        return f"{self.customer.address} zip_code: {self.customer.address.zip_code} neighborhood: {self.customer.address.neighborhood}"

    address_customer.short_description = "Endereço do Usuário"

    def __str__(self):
        return f"Order {self.order_number} de {self.customer}"