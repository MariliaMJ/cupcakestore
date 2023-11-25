from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart, name="cart"),
    path("add_to_cart/<uuid:product_id>/", views.add_to_cart, name="add_cart"),
    path(
        "remove_from_cart/<uuid:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path(
        "remove_cart_item/<uuid:product_id>/",
        views.remove_cart_item,
        name="remove_cart_item",
    ),
]
