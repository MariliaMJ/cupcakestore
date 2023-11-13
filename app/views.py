from uuid import UUID

from django.contrib.auth import login
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import AddressForm, CustomerForm, UserCreationForm, LoginForm
from .models import Cupcake, Address, Order, Customer, ItemOrder
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/accounts/login")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect("cupcakes")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


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

        return HttpResponseRedirect(reverse("get-cupcakes"))
    else:
        return HttpResponseRedirect(reverse("get-cupcakes"))


def view_cart(request):
    cart = request.session.get("cart", {})

    cart_items = []
    total = 0

    for cupcake_id, quantity in cart.items():
        cupcake = get_object_or_404(Cupcake, id=cupcake_id)
        total = 0
        cart_items.append(
            {
                "cupcake": cupcake,
                "quantity": quantity,
                "total_per_product": quantity * cupcake.price,
            }
        )

        total += cupcake.price * quantity

    return render(request, "carrinho.html", {"cart_items": cart_items, "total": total})


def get_customers_data(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            request.session["cliente_id"] = cliente.id
            return redirect("checkout")
    else:
        form = CustomerForm()

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
                value = cupcake.price
                value_total = cupcake.price * quantity
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

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            messages.success(request, 'Um e-mail com instruções para redefinir sua senha foi enviado para o seu endereço de e-mail.')

            email_subject = 'Instruções para redefinir a senha'
            email_message = 'Siga as instruções no email para redefinir sua senha.'
            from_email = 'mmjanizelli@gmail.com'
            recipient_list = [form.cleaned_data['email']]
            send_mail(email_subject, email_message, from_email, recipient_list, fail_silently=False)

            return redirect("login") 
    else:
        form = PasswordResetForm()
    
    return render(request, "password_reset_done.html", {'form': form})


def _get_customer(customerForm: Customer) -> Customer:
    try:
        customer = Customer.objects.get(email=customerForm.email)

        if not customer:
            return customerForm
        return customer
    except:
        return customerForm
