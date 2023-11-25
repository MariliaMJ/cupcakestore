from django.shortcuts import render
from carts.views import cart_counter

from store.models import Product

# Create your views here.
def get_cupcakes(request):
    cupcakes = Product.objects.filter(is_available=True).all()
    cart_count = cart_counter(request)

    return render(
        request, "list.html", {"cupcakes": cupcakes, "cart_count": cart_count}
    )
