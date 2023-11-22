from django.urls import path
from . import views

urlpatterns = [
    path("add-to-cart/<uuid:cupcake_id>/", views.add_to_cart, name="add-to-cart"),
    path("", views.cart, name="cart"),
]