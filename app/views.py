import logging
from uuid import UUID

from django.contrib.auth import login
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import AddressForm, CustomerForm
from .models import Cupcake, Address, Order, Customer, ItemOrder


def get_cupcakes(request):
    cupcakes = Cupcake.objects.all()
    return render(request, "list.html", {"cupcakes": cupcakes})


def add_to_cart(request, cupcake_id):
    if request.method == "GET":
        cupcake_id = str(cupcake_id)
        if "cart" not in request.session:
            request.session["cart"] = {}

        cart = request.session["cart"]

        if cupcake_id in cart:
            cart[cupcake_id] += 1
        else:
            cart[cupcake_id] = 1

        request.session["cart"] = cart
        logging.debug(f"cart from session {cart}")

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
        cart_items.append(
            {
                "cupcake": cupcake,
                "quantity": quantity,
                "total_per_product": quantity * cupcake.preco,
            }
        )

        total += cupcake.preco * quantity

    return render(request, "carrinho.html", {"cart_items": cart_items, "total": total})


def get_customers_data(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            request.session["cliente_id"] = cliente.id
            return redirect("checkout")
    else:
        form = ClienteForm()

    return render(request, "coleta_dados_cliente.html", {"form": form})


def checkout(request):
    cart = request.session.get("cart", {})

    if "cliente_id" not in request.session:
        address_form = AddressForm(request.POST, prefix="address")
        customer_form = CustomerForm(request.POST, prefix="customer")

    if (
        request.method == "POST"
        and address_form.is_valid()
        and customer_form.is_valid()
    ):
        with transaction.atomic():
            address = address_form.save()
            customer = customer_form.save(commit=False)
            cliente = _get_customer(customer)
            cliente.address = address
            cliente.save()

            order = Order()
            order.customer = cliente
            order.save()

            for cupcake_id, quantity in cart.items():
                cupcake = Cupcake.objects.get(pk=cupcake_id)
                value = cupcake.preco
                value_total = cupcake.preco * quantity
                item = ItemOrder(
                    cupcake=cupcake,
                    order=order,
                    quantity=quantity,
                    value=value,
                    value_total=value_total,
                )
                item.save()

            request.session["cart"] = {}
        transaction.commit()

        return render(request, "confirmation.html")
    else:
        return render(
            request,
            "checkout.html",
            {"address_form": address_form, "customer_form": customer_form},
        )


def order(request):
    return render(request, "order.html")


def _get_customer(customerForm: Customer) -> Customer:
    try:
        customer = Customer.objects.get(email=customerForm.email)

        if not customer:
            return customerForm
        return customer
    except:
        return customerForm
