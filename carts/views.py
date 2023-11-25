from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from store.models import Product
from carts.models import Cart, CartItem
from store.models import Product
import uuid

# Create your views here.


def cart(request):
    cart_id = _cart_id(request)
    try:
        cart = Cart.objects.get(cart_id=cart_id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=cart_id)
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

    return render(
        request, "carrinho.html", {"cart_items": cart_items_render, "total": total}
    )


def _cart_id(request):
    cart_id = request.session.get("cart_id", None)
    if not cart_id:
        cart_id = str(uuid.uuid4())
        request.session["cart_id"] = cart_id
    return cart_id


def add_to_cart(request, product_id):
    if request.method == "GET":
        product_id = str(product_id)
        product = Product.objects.get(id=product_id)

        cart_id = _cart_id(request)
        try:
            cart = Cart.objects.get(cart_id=cart_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=cart_id)
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

        return HttpResponseRedirect(reverse("cart"))
    else:
        return HttpResponseRedirect(reverse("cart"))


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = request.session.get("cart_id", None)
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(cart_id=cart_id)
            cart_item = CartItem.objects.get(product=product, cart=cart)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except Exception as e:
        pass
    return HttpResponseRedirect(reverse("cart"))


def cart_counter(request):
    cart_count = 0

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(cart=cart).all()
        else:
            cart_items = CartItem.objects.filter(cart=cart).all()
        for cart_item in cart_items:
            cart_count += cart_item.quantity
    except Cart.DoesNotExist:
        return cart_count

    return cart_count


def remove_cart_item(request, product_id):  # remove o item do carrinho
    product = get_object_or_404(Product, id=product_id)
    cart_id = request.session.get("cart_id", None)
    if request.user.is_authenticated:
        cart = Cart.objects.get(cart_id=cart_id)
        cart_item = CartItem.objects.get(product=product, cart=cart)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return HttpResponseRedirect(reverse("cart"))
