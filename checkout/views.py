from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from accounts.models import Account

from customer.forms import AddressForm, CustomUserCreationForm
from customer.models import Customer
from carts.models import Cart, CartItem
from checkout.controller import get_cart
from checkout.models import ItemOrder, Order


"""Does the whole process of checkout. Checks the cart and collects the user's 
information, save all of them and completes and order, cleaning the cart.
Parameters
----------
request : HttpRequest
access https://docs.djangoproject.com/en/4.2/ref/request-response/ for more info
"""
def checkout(request: HttpRequest) -> HttpResponse:
    cart_id = request.session.get("cart_id", {})
    user = request.user if request.user.is_authenticated else None

    if user:
        try:
            customer_form = CustomUserCreationForm(prefix="customer", instance=user)
            customer = Customer.objects.get(user=user)
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
            address_form = AddressForm(
                initial=initial_data, prefix="address", instance=customer.address
            )
        except Customer.DoesNotExist:
            address_form = AddressForm(prefix="address")

    else:
        address_form = AddressForm(prefix="address")
        customer_form = CustomUserCreationForm(prefix="customer")
    if request.method == "POST":
        address_form = AddressForm(request.POST, prefix="address")
        customer_form = CustomUserCreationForm(
            request.POST, prefix="customer", instance=user
        )

        with transaction.atomic():
            address_form.is_valid()
            customer_form.is_valid()
            address = address_form.save()
            user = _get_account(customer_form)
            
            customer = _get_customer(user)
            if customer is None:
                customer = user
            customer.address = address
            customer.save()
            order = Order()
            order.customer = customer
            order.save()

            cart = Cart.objects.get(cart_id=cart_id)
            cart_items = CartItem.objects.filter(cart=cart).all()

            for item in cart_items:
                value = item.product.price
                value_total = item.product.price * item.quantity
                item_order = ItemOrder(
                    product=item.product,
                    order=order,
                    quantity=item.quantity,
                    value=value,
                    value_total=value_total,
                )
                item_order.save()

            request.session["cart_id"] = {}
        transaction.commit()

        return render(request, "confirmation.html")
    else:
        cart_view = get_cart(cart_id)
        return render(
            request,
            "checkout.html",
            {
                "address_form": address_form,
                "customer_form": customer_form,
                "cart_view": cart_view,
            },
        )

"""Does the whole process of checkout. Checks the cart and collects the user's 
information, save all of them and completes and order, cleaning the cart.
Parameters
----------
user : Account. The entity of a person registration in the website, based on django 
preset account registration

"""
def _get_customer(user: Account) -> Customer:
    try:
        return Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        customer = Customer(user=user)
        customer.save()
        return customer

def _get_account(user: CustomUserCreationForm) -> Account:
    try:
        return Account.objects.get(email=user.data['customer-email'])
    except Account.DoesNotExist:
        return None