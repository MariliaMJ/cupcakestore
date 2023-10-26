from uuid import UUID
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import Cupcake
from .models import Pedido
from .models import Usuario

import pdb

def get_cupcakes(request):
    cupcakes = Cupcake.objects.all()
    return render(request, "list.html", {"cupcakes": cupcakes})

def add_to_cart(request, cupcake_id):
  
    # pdb.set_trace()
    if request.method == 'GET':
        # pdb.set_trace()
        cupcake_id = str(cupcake_id)
        if "cart" not in request.session:
            request.session["cart"] = {}
        
        cart = request.session["cart"]
        if cupcake_id in cart:
            cart[cupcake_id] += 1
        else:
            cart[cupcake_id] = 1
        
        request.session["cart"] = cart
        
        return HttpResponseRedirect(reverse("get-cupcakes"))
    else:
        return HttpResponseRedirect(reverse("get-cupcakes"))

def view_cart(request):
    cart = request.session.get("cart", {})

    cart_items = []  # Lista para armazenar objetos de produto no carrinho
    total = 0
    
    for cupcake_id, quantity in cart.items():
        cupcake = get_object_or_404(Cupcake, id=cupcake_id)
        total_per_product = 0
        cart_items.append({"cupcake": cupcake, "quantity": quantity, "total_per_product": quantity * cupcake.preco})

        total += cupcake.preco * quantity

    return render(request, "carrinho.html", {"cart_items": cart_items, "total": total})

def checkout(request):
    cart = request.session.get("cart", {})
    
    # Crie um novo objeto de Pedido com base nos itens do carrinho e salve no banco de dados
    if cart:
        pedido = Pedido.objects.create()
        for cupcake_id, quantity in cart.items():
            cupcake = Cupcake.objects.get(pk=cupcake_id)
            pedido.itempedido_set.create(cupcake=cupcake, quantidade=quantity)
        
        # Limpe a sessão do carrinho após a finalização da compra
        request.session["cart"] = {}
        
        return render(request, "checkout.html", {"pedido": pedido})
    
    # Caso não haja itens no carrinho, redirecione para a página da lista de cupcakes ou adicione um tratamento adequado
    return redirect("get-cupcakes")