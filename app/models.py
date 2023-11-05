from enum import Enum
from django.db import models
from django.utils import timezone
import uuid 

class Cupcake(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100)
    sabor = models.CharField(max_length=100)
    cobertura = models.TextField()
    recheio = models.TextField()
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    imagem = models.URLField(max_length=200)
    estoque = models.IntegerField(editable=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sabor} Cupcake com Cobertura de {self.cobertura} e Recheio de {self.recheio}"

class Endereco(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    logradouro = models.CharField(max_length=100)
    rua = models.CharField(max_length=255)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    cep = models.CharField(max_length=9)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rua

class Usuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    username = models.CharField(max_length=30)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class StatusPedido(Enum):
    PENDENTE = 'Pendente'
    EM_ANDAMENTO = 'Em Andamento'
    CONCLUIDO = 'Concluído'
    CANCELADO = 'Cancelado'


class ItemPedido(models.Model):
    cupcake = models.ForeignKey(Cupcake, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    valor = models.DecimalField(null=False, decimal_places=2, max_digits=10)
    valor_total = models.DecimalField(null=False, decimal_places=2, max_digits=10)
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE, related_name="itens")

    def __str__(self):
        return f"{self.cupcake.nome} ({self.quantidade})"


class Pedido(models.Model):
    numero_pedido = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=[(status.name, status.value) for status in StatusPedido],
        default=StatusPedido.PENDENTE.value
    )
    
    def itens_pedido(self):
        item_descriptions = []
        for item in self.itens.all():
            description = f"{item.quantidade}x {item.cupcake.nome}"
            item_descriptions.append(description)
        return ", ".join(item_descriptions)
    itens_pedido.short_description = "Itens do Pedido"

    def endereco_usuario(self):
        return f"{self.usuario.endereco.logradouro} {self.usuario.endereco} cep: {self.usuario.endereco.cep} bairro:"

    endereco_usuario.short_description = "Endereço do Usuário"

    def __str__(self):
        return f"Pedido {self.numero_pedido} de {self.usuario}"


