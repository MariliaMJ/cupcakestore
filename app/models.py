from django.db import models
import uuid 

class Cupcake(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sabor = models.CharField(max_length=100)
    cobertura = models.TextField()
    recheio = models.TextField()
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sabor} Cupcake com Cobertura de {self.cobertura} e Recheio de {self.recheio}"

class Usuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sabor = models.CharField(max_length=100)
    cobertura = models.TextField()
    recheio = models.TextField()
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 