from carts.models import Cart, CartItem, CartView


def get_cart(cart_id):
    try:
        cart = Cart.objects.get(cart_id=cart_id)
    except Cart.DoesNotExist as e:
        raise e
    
    cart_items = CartItem.objects.filter(cart=cart).all()
    cart_items_render = []
    total = 0

    for item in cart_items:
        cart_items_render.append(
            {
                "cupcake": item.product,
                "quantity": item.quantity,
                "total_per_product": item.quantity * item.product.price,
            }
        )

        total += item.product.price * item.quantity
    return CartView(cart_items=cart_items_render, total=total)