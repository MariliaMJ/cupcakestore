from enum import Enum
from django.db import models
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
    rua = models.TextField()
    bairro = models.TextField()
    cidade = models.TextField()
    estado = models.TextField()
    cep = models.TextField()
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
    endereco = models.DecimalField(max_digits=5, decimal_places=2)
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

class Item(models.Model):
    produto = models.ForeignKey(Cupcake, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    # Outros campos relevantes para os itens
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    numero_pedido = models.CharField(max_length=10)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data = models.DateTimeField()
    itens = models.ManyToManyField(Item, related_name='pedidos')
    status = models.CharField(
        max_length=20,
        choices=[(status.name, status.value) for status in StatusPedido],
        default=StatusPedido.PENDENTE.value
    )

    def __str__(self):
        return self.numero_pedido
    