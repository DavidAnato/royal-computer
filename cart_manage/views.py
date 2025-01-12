# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from ecommerce.models import Product
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect

@login_required
def add_to_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)  # Crée un panier si l'utilisateur n'en a pas déjà un
    product = Product.objects.get(id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    try:
        item = CartItem.objects.get(cart=cart, product=product)
        item.quantity += quantity
        item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(cart=cart, product=product, quantity=quantity)
    messages.success(request, f'Le produit {product.name} a été ajouté à votre panier.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # Recharge la même page


@login_required
def remove_from_cart(request, item_id):
    item = CartItem.objects.get(id=item_id)
    if request.user == item.cart.user:
        item.delete()
    return redirect('cart')

@login_required
def clear_cart(request):
    cart = Cart.objects.get(user=request.user)  # Assurez-vous que l'utilisateur est connecté
    cart.items.all().delete()
    return redirect('cart')

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    new_products = Product.objects.filter(in_stock=True).filter(is_new=True).order_by('-created_at')

    if request.method == 'POST':
        formset = []
        promo_code = request.POST.get('promo_code')
        if promo_code.strip() == '':
            cart.promo_code = None  # Supprime le code promo si le champ est vide
            cart.save()
        else:
            # Vérifiez si le code promo existe et est valide, puis l'appliquez au panier
            try:
                promo = PromoCode.objects.get(code=promo_code)
                if promo.is_valid:
                    cart.promo_code = promo
                    cart.save()
                    messages.success(request, f"Code promo validé. Réduction de {promo.discount}% appliquée.")
                else:
                    cart.promo_code = None
                    messages.error(request, "Code promo invalide.")
            except PromoCode.DoesNotExist:
                cart.promo_code = None
                messages.error(request, "Code promo invalide.")

        for item in items:
            form = CartItemForm(request.POST, prefix=str(item.id), instance=item)
            if form.is_valid():
                item.quantity = form.cleaned_data['quantity']
                item.save()
            formset.append(form)
    else:
        formset = [CartForm(prefix=str(item.id), initial={'quantity': item.quantity}) for item in items]

    number_of_items_in_cart = cart.items.count()  # Supposons que vous avez un champ 'items' pour stocker les produits dans le panier

    context = {
        'cart': cart,
        'formset': formset,
        'new_products': new_products,
        'number_of_items_in_cart': number_of_items_in_cart,


    }
    return render(request, 'cart_manage/cart_view.html', context)

# Commande

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()
    user_addresses = Address.objects.filter(user=request.user)

    if request.method == 'POST':
        shipping_form = ShippingAddressForm(request.user, request.POST)
        if shipping_form.is_valid():
            selected_address = shipping_form.cleaned_data.get('shipping_address', None)  # Adresse peut être None

            # Créez une commande même si l'adresse est optionnelle
            order = Order.objects.create(user=request.user, address=selected_address)
            for item in items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.price)
            cart.items.all().delete()  # Supprimez les éléments du panier une fois la commande passée
            if cart.promo_code:
                cart.promo_code = None
                cart.save()

            return redirect('order_success')  # Redirigez l'utilisateur vers une page de confirmation de commande

    else:
        shipping_form = ShippingAddressForm(request.user)

    context = {
        'cart': cart,
        'items': items,
        'user_addresses': user_addresses,
        'shipping_form': shipping_form,
    }
    return render(request, 'cart_manage/checkout.html', context)


def order_success(request):
    order = Order.objects.filter(user=request.user).last()
    context = {
        'order': order,
    }

    return render(request, 'cart_manage/order_success.html', context)



from urllib.parse import quote
@login_required
def generate_whatsapp_url(request):
    # Récupérez le panier de l'utilisateur
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    # Générez le contenu du message WhatsApp sous forme de tableau lisible
    message = f"*Panier d'achats de {quote(cart.user.first_name)} {quote(cart.user.last_name)} :*%0A%0A"
    message += "*Produit\t\t\t\tQuantité\t\t\tPrix total*%0A"
    
    for item in cart.items.all():
        product_name = quote(item.product.name)
        quantity = item.quantity
        total_price = item.total_price()  # Appelez la méthode total_price()
        message += f"```{product_name}\t\t{quantity}\t\t\t{total_price}F```%0A"
    
    # Appelez les méthodes pour obtenir les valeurs du coût total, de la remise et du coût final
    total = cart.total()
    discount = cart.discount()
    final_total = cart.final_total()
    
    message += f"\n*Coût Total*: {total}F%0A"
    message += f"*Remise*: {discount}F%0A"
    message += f"*Coût Final*: {final_total}F%0A"
    
    # Générez l'URL WhatsApp complet
    whatsapp_url = f"https://wa.me/22956543880?text={message}"
    
    return redirect(whatsapp_url)
