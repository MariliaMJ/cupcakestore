import uuid
from django.db import models

# Create your models here.
class Product(models.Model):
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
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.flavor} Cupcake com cobertura de {self.icing} e recheio de {self.filling}"