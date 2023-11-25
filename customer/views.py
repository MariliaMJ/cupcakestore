from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from carts.views import cart_counter
from checkout.models import Order
from store.models import Product

from .forms import (
    AddressForm,
    CustomerForm,
    CustomUserUpdateForm,
    LoginForm,
    UserCreationForm,
)
from .models import Customer


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

            if (
                user_form.is_valid()
                and address_form.is_valid()
                and customer_form.is_valid()
            ):
                user_form.save()
                customer_form.save()
                address_form.save()
                messages.success(request, "Dados atualizados com sucesso!")
                return redirect("user-account")

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
                messages.success(request, "Cadastro realizado com sucesso!")
                return redirect("user-account")

    return render(
        request,
        "user_account.html",
        {
            "user_data": user_data,
            "customer_form": customer_form,
            "customer_user_form": user_form,
            "address_form": address_form,
        },
    )


@login_required
def order_history(request):
    try:
        user = request.user

        customer = Customer.objects.get(user=user)
        orders = Order.objects.filter(customer=customer).order_by("-created_at")
        context = {"orders": orders}

        return render(request, "order_history.html", context)
    except Customer.DoesNotExist:
        return render(request, "order_history.html", {"orders": []})


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
