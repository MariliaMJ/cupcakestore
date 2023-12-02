from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.forms import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from checkout.models import Order

from .forms import (
    AddressForm,
    CustomerForm,
    CustomUserUpdateForm,
    LoginForm,
    SignupForm,
)
from .models import Customer

"""Signs a user up, collecting a username and a password
Parameters
----------
request : HttpRequest
access https://docs.djangoproject.com/en/4.2/ref/request-response/ for more info
"""
def user_signup(request: HttpRequest) -> HttpResponse | SignupForm:
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/accounts/login")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})


"""Logs a user in. 
Parameters
----------
request : HttpRequest
access https://docs.djangoproject.com/en/4.2/ref/request-response/ for more info
"""
def login(request: HttpRequest) -> HttpResponse:
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


def logout(request):
    return render("logged_out.html")


"""Shows a form of a user saved data, allowing them to edit it or completed
unfilled information. It's only possible to check this being logged in.
Parameters
----------
request : HttpRequest
access https://docs.djangoproject.com/en/4.2/ref/request-response/ for more info
"""
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
            address_form = AddressForm(request.POST, instance=customer.address)

            if user_form.is_valid() and address_form.is_valid():
                user_form.save()
                address_form.save()
                messages.success(request, "Dados atualizados com sucesso!")
                return redirect("user-account")

        else:
            user_form = CustomUserUpdateForm(instance=request.user)
            address_form = AddressForm(instance=customer.address)
    except Customer.DoesNotExist:
        user_data = {
            "name": request.user.first_name,
            "email": request.user.email,
            "phone_number": "",
            "address": {
                "street": "",
                "neighborhood": "",
                "city": "",
                "state": "",
                "zip_code": "",
            },
        }
        user_form = CustomUserUpdateForm(instance=request.user)
        address_form = AddressForm()

        if request.method == "POST":
            user_form = CustomUserUpdateForm(request.POST)
            address_form = AddressForm(request.POST)

            if user_form.is_valid() and address_form.is_valid():
                user = user_form.save(commit=False)
                customer = Customer.objects.create(user=user)
                address = address_form.save()
                customer.address = address
                customer.save()
                messages.success(request, "Cadastro realizado com sucesso!")
                return redirect("user-account")

    return render(
        request,
        "user_account.html",
        {"user_data": user_data, "user_form": user_form, "address_form": address_form},
    )


"""Renders a list of requested orders realted to a user. Must be logged in to see
this page.

Parameters
----------
request : HttpRequest
access https://docs.djangoproject.com/en/4.2/ref/request-response/ for more info
"""


@login_required
def order_history(request: HttpRequest) -> HttpResponse:
    try:
        user = request.user

        customer = Customer.objects.get(user=user)
        orders = Order.objects.filter(customer=customer).order_by("-created_at")
        context = {"orders": orders}

        return render(request, "order_history.html", context)
    except Customer.DoesNotExist:
        return render(request, "order_history.html", {"orders": []})


"""Renders a form to collect a customer's data in case this data was not yet
collected

Parameters
----------
request : HttpRequest
access https://docs.djangoproject.com/en/4.2/ref/request-response/ for more info
"""


def get_customers_data(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            request.session["cliente_id"] = cliente.id
            return redirect("checkout")
    else:
        form = CustomerForm()

    return render(request, "coleta_dados_cliente.html", {"form": form})


"""Resets the password of a user account

Parameters
----------
request : HttpRequest
access https://docs.djangoproject.com/en/4.2/ref/request-response/ for more info
"""


def password_reset(request: HttpRequest) -> HttpResponse | SetPasswordForm:
    breakpoint()
    if request.method == "POST":
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            request.user.password = make_password(password)
            request.user.save()

            return redirect("login")
    else:
        form = SetPasswordForm()

    return render(request, "password_reset.html", {"form": form})
