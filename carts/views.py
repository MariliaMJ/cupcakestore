from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from store.models import Product
from carts.models import Cart, CartItem
import uuid

# Create your views here.

def cart(request):
    cart_id = _cart_id(request)
    try:
        cart = Cart.objects.get(cart_id=cart_id)
    except Cart.DoesNotExist:
        breakpoint()
        cart = Cart.objects.create(
            cart_id = cart_id
        )
        cart.save()
    
    cart_items = CartItem.objects.filter(cart=cart).all()
    cart_items_render = []
    total = 0

    for item in cart_items:
        cart_items_render.append(
            {
                "cupcake": item.product,
                "quantity": item.quantity,
                "total_per_product": item.quantity * item.product.price,
            }
        )

        total += item.product.price * item.quantity

    return render(request, "carrinho.html", {"cart_items": cart_items_render, "total": total})

def _cart_id(request):
    cart_id = request.session.get("cart_id", None)
    if not cart_id:
        breakpoint()
        cart_id = str(uuid.uuid4())
        request.session["cart_id"] = cart_id
    return cart_id

def add_to_cart(request, cupcake_id):
    if request.method == "GET":
        cupcake_id = str(cupcake_id)
        product = Product.objects.get(id=cupcake_id)

        cart_id = _cart_id(request)
        try:
            cart = Cart.objects.get(cart_id=cart_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = cart_id
            )
            cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=1,
            )
            cart_item.save()

        return HttpResponseRedirect(reverse("get-cupcakes"))
    else:
        return HttpResponseRedirect(reverse("get-cupcakes"))

def remove_from_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect("cart")