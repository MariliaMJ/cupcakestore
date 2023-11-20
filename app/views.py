from uuid import UUID

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import AddressForm, CustomUserCreationForm, CustomerForm, LoginForm, UserCreationForm,CustomUserUpdateForm
from .models import Cupcake, Customer, ItemOrder, Order


def user_signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/accounts/login")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("cupcakes")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


@login_required
def user_account(request):
    try:
        customer = Customer.objects.get(user=request.user)
        user_data = {
            "name": request.user.first_name,
            "email": request.user.email,
            "phone_number": customer.phone_number,
            "address": {
                "street": customer.address.street,
                "neighborhood": customer.address.neighborhood,
                "city": customer.address.city,
                "state": customer.address.state,
                "zip_code": customer.address.zip_code,
            },
        }

        if request.method == "POST":
            user_form = CustomUserUpdateForm(request.POST, instance=request.user)
            customer_form = CustomerForm(request.POST, instance=customer)
            address_form = AddressForm(request.POST, instance=customer.address)

            if user_form.is_valid() and address_form.is_valid() and customer_form.is_valid():
                user_form.save()
                customer_form.save()
                address_form.save()
                messages.success(request, 'Dados atualizados com sucesso!')
                return redirect('user-account')

        else:
            user_form = CustomUserUpdateForm(instance=request.user)
            customer_form = CustomerForm(instance=customer)
            address_form = AddressForm(instance=customer.address)

    except Customer.DoesNotExist:
        user_data = None
        user_form = CustomUserUpdateForm()
        customer_form = CustomerForm()
        address_form = AddressForm()

        if request.method == "POST":
            user_form = CustomUserUpdateForm(request.POST)
            customer_form = CustomerForm(request.POST)
            address_form = AddressForm(request.POST)

            if customer_form.is_valid() and address_form.is_valid():
                user = user_form.save(commit=False)
                customer = customer_form                
                address = address_form.save()
                customer.address = address
                customer.user = user
                customer.save()
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('user-account')

    return render(request, "user_account.html", {"user_data": user_data, "customer_form": customer_form, "customer_user_form": user_form, "address_form": address_form})

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
    user = request.user if request.user.is_authenticated else None

    if user:
        customer = Customer.objects.get(user=user)

        # TODO corrigir dado inicial
        # se o usuário estiver logaod, o form deve vir preenchido com os dados 
        # cadastrados, caso contrário, 'epossível fazeer o checkout sem login ou 
        # oferecer a opção de logar 
        initial_data = {
            "address-street": customer.address.street,
            "address-neighborhood": customer.address.neighborhood,
            "address-city": customer.address.city,
            "address-state": customer.address.state,
            "address-zip_code": customer.address.zip_code,
            "customer-name": customer.user.first_name,
            "customer-email": customer.user.email,
            "customer-phone_number": customer.phone_number,
        }
        address_form = AddressForm(initial=initial_data, prefix="address")
        customer_form = CustomUserCreationForm(initial=initial_data, prefix="customer")
    else:
        address_form = AddressForm(request.POST, prefix="address")
        customer_form = CustomUserCreationForm(request.POST, prefix="customer")

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
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            messages.success(
                request,
                "Um e-mail com instruções para redefinir sua senha foi enviado para o seu endereço de e-mail.",
            )

            email_subject = "Instruções para redefinir a senha"
            email_message = "Siga as instruções no email para redefinir sua senha."
            from_email = "mmjanizelli@gmail.com"
            recipient_list = [form.cleaned_data["email"]]
            send_mail(
                email_subject,
                email_message,
                from_email,
                recipient_list,
                fail_silently=False,
            )

            return redirect("login")
    else:
        form = PasswordResetForm()

    return render(request, "password_reset_done.html", {"form": form})


def _get_customer(customerForm: Customer) -> Customer:
    try:
        customer = Customer.objects.get(user_email=customerForm.email)

        if not customer:
            return customerForm
        return customer
    except:
        return customerForm
