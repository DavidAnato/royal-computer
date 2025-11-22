from cart_manage.models import Cart, CartItem
from ecom import settings

def global_variables(request):
    user = request.user
    number_of_items_in_cart = 0
    products_in_cart = []
    if user.is_authenticated:
        cart = Cart.objects.filter(user=user).first()
        number_of_items_in_cart = cart.items.count() if cart else 0
        products_in_cart = CartItem.objects.filter(cart=cart).values_list('product__id', flat=True)

    return {
        'GOOGLE_CLIENT_ID': settings.GOOGLE_CLIENT_ID,
        'GOOGLE_REDIRECT_URI': settings.GOOGLE_REDIRECT_URI,
        'number_of_items_in_cart': number_of_items_in_cart,
        'products_in_cart': products_in_cart,
    }
