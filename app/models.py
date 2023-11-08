from enum import Enum
from django.db import models
from django.utils import timezone
import uuid


class Cupcake(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    flavor = models.CharField(max_length=100)
    icing = models.TextField()
    filling = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.URLField(max_length=200)
    inventory = models.IntegerField(editable=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.flavor} Cupcake com cobertura de {self.icing} e recheio de {self.filling}"


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    street = models.CharField(max_length=255)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=9)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.street


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    username = models.CharField(max_length=30)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class OrderStatus(Enum):
    PENDENTE = "Pendente"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDO = "Concluído"
    CANCELADO = "Cancelado"


class ItemOrder(models.Model):
    cupcake = models.ForeignKey(Cupcake, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    value = models.DecimalField(null=False, decimal_places=2, max_digits=10)
    value_total = models.DecimalField(null=False, decimal_places=2, max_digits=10)
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="itens")

    def __str__(self):
        return f"{self.cupcake.name} ({self.quantity})"


class Order(models.Model):
    order_number = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    data = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=[(status.name, status.value) for status in OrderStatus],
        default=OrderStatus.PENDENTE.value,
    )

    def items_order(self):
        item_descriptions = []
        for item in self.itens.all():
            description = f"{item.quantity}x {item.cupcake.name}"
            item_descriptions.append(description)
        return ", ".join(item_descriptions)

    items_order.short_description = "Itens do Order"

    def address_customer(self):
        return f"{self.customer.address} zip_code: {self.customer.address.zip_code} neighborhood: {self.customer.address.neighborhood}"

    address_customer.short_description = "Endereço do Usuário"

    def __str__(self):
        return f"Order {self.order_number} de {self.customer}"
