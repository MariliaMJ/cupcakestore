from django.contrib import admin
from .models import Cupcake,Pedido,ItemPedido 

admin.site.register(Cupcake)

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0 

class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ("cupcake", "quantidade", "pedido")

admin.site.register(ItemPedido, ItemPedidoAdmin)

class PedidoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "endereco_usuario", "itens_pedido", "numero_pedido") 
    inlines = [ItemPedidoInline]

admin.site.register(Pedido, PedidoAdmin)
