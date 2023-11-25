from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from carts.views import cart_counter

from store.models import Product

"""Renders a list of cupcakes/products available for purchase
Parameters
----------
request : HttpRequest
access https://docs.djangoproject.com/en/4.2/ref/request-response/ for more info
"""
def get_cupcakes(request: HttpRequest) -> HttpResponse:
    cupcakes = Product.objects.filter(is_available=True).all()
    cart_count = cart_counter(request)

    return render(
        request, "list.html", {"cupcakes": cupcakes, "cart_count": cart_count}
    )
