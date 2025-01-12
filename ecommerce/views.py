from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *
from cart_manage.models import CartItem, Cart
from blog.models import Post

def product_list(request):
    # Récupérez les paramètres de filtre, de tri et de recherche depuis la requête
    category_ids = request.GET.getlist('category[]')
    brand_ids = request.GET.getlist('brand[]')
    keyword = request.GET.get('keyword')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by', 'name')  # Par défaut, triez par nom

    # Filtrez les produits en fonction des paramètres
    products = Product.objects.filter(in_stock=True)

    if category_ids:
        products = products.filter(category__in=category_ids)

    if brand_ids:
        products = products.filter(brand__in=brand_ids)

    if min_price:
        products = products.filter(Q(price__gte=min_price) | Q(promo_price__gte=min_price))

    if max_price:
        products = products.filter(Q(price__lte=max_price) | Q(promo_price__lte=max_price))

    if keyword:
        # Recherchez par nom de produit ou mots-clés associés
        products = products.filter(Q(name__icontains=keyword) | Q(keyword_set__keyword__icontains=keyword))

    # Éliminez les doublons en utilisant .distinct()
    products = products.distinct()

    # Triez les produits
    products = products.order_by(sort_by)

    # Paginez les produits
    paginator = Paginator(products, per_page=12)  # Nombre de produits par page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    # Obtenez toutes les catégories et marques pour les filtres
    categories = Category.objects.all()
    brands = Brand.objects.all()

    # Obtenez tous les mots-clés pour la recherche avancée
    keywords = KeyWord.objects.values_list('keyword', flat=True).distinct()

    # Obtenez l'utilisateur actuel
    user = request.user

    # Vérifiez si l'utilisateur est authentifié
    if user.is_authenticated:
        # L'utilisateur est connecté, récupérez le panier de l'utilisateur
        cart = Cart.objects.filter(user=user).first()
        
        if cart is not None:
            # Récupérez la liste des produits déjà présents dans le panier
            products_in_cart = CartItem.objects.filter(cart=cart).values_list('product__id', flat=True)

            number_of_items_in_cart = cart.items.count()  # Supposons que vous avez un champ 'items' pour stocker les produits dans le panier
        else:
            # Le panier de l'utilisateur est vide
            products_in_cart = []
            number_of_items_in_cart = 0
    else:
        # L'utilisateur n'est pas connecté, initialisez les valeurs à zéro ou à une valeur par défaut
        cart = None
        products_in_cart = []
        number_of_items_in_cart = 0

    return render(request, 'ecommerce/product_list.html', {
        'products': products,
        'categories': categories,
        'brands': brands,
        'selected_categories': category_ids,
        'selected_brands': brand_ids,
        'selected_min_price': min_price,
        'selected_max_price': max_price,
        'selected_keyword': keyword,
        'selected_sort_by': sort_by,
        'keywords': keywords,
        'products_in_cart': products_in_cart,  
        'number_of_items_in_cart': number_of_items_in_cart,
    })

from django.http import JsonResponse

def autocomplete_suggestions(request):
    term = request.GET.get('term')
    # Recherchez les mots-clés qui contiennent le terme recherché
    suggestions = KeyWord.objects.filter(keyword__icontains=term)
    suggestion_list = [keyword.keyword for keyword in suggestions]
    return JsonResponse(suggestion_list, safe=False)

def product_detail(request, product_id):
    # Obtenez l'utilisateur actuel
    user = request.user

    product = Product.objects.get(id=product_id)
    similar_products = Product.objects.filter(in_stock=True).filter(category=product.category).exclude(id=product.id).order_by('-created_at')[:5]

    # Vérifiez si l'utilisateur est authentifié
    if user.is_authenticated:
        # L'utilisateur est connecté, récupérez le panier de l'utilisateur
        cart = Cart.objects.filter(user=user).first()
        
        # Vérifiez si le produit est dans le panier de l'utilisateur actuel
        product_in_cart = CartItem.objects.filter(cart__user=user, product=product).exists()
        number_of_items_in_cart = cart.items.count()  # Supposons que vous avez un champ 'items' pour stocker les produits dans le panier
    else:
        # L'utilisateur n'est pas connecté, initialisez les valeurs à zéro ou à une valeur par défaut
        cart = None
        product_in_cart = False
        number_of_items_in_cart = 0

    return render(request, 'ecommerce/product_detail.html', {
        'product': product,
        'similar_products': similar_products,
        'product_in_cart': product_in_cart,
        'number_of_items_in_cart': number_of_items_in_cart,
    })


def home(request):
    products = Product.objects.filter(in_stock=True)
    vedettes_products = Product.objects.filter(in_stock=True).filter(is_vedette=True).order_by('-created_at')[:5]
    new_products = Product.objects.filter(in_stock=True).filter(is_new=True).order_by('-created_at')
    promo_products = Product.objects.filter(in_stock=True).filter(in_promo=True).order_by('-created_at')
    latest_posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')[:4]


    # Obtenez l'utilisateur actuel
    user = request.user

    # Vérifiez si l'utilisateur est authentifié
    if user.is_authenticated:
        # L'utilisateur est connecté, récupérez le panier de l'utilisateur
        cart = Cart.objects.filter(user=user).first()
        
        if cart is not None:
            # Récupérez la liste des produits déjà présents dans le panier
            products_in_cart = CartItem.objects.filter(cart=cart).values_list('product__id', flat=True)
            number_of_items_in_cart = cart.items.count()  # Supposons que vous avez un champ 'items' pour stocker les produits dans le panier
        else:
            # Le panier de l'utilisateur est vide
            products_in_cart = []
            number_of_items_in_cart = 0
    else:
        # L'utilisateur n'est pas connecté, initialisez les valeurs à zéro ou à une valeur par défaut
        cart = None
        products_in_cart = []
        number_of_items_in_cart = 0

    return render(request, 'ecommerce/index.html', {
        'products': products,
        'vedettes_products': vedettes_products,
        'new_products': new_products,
        'promo_products': promo_products,
        'products_in_cart': products_in_cart,  
        'latest_posts': latest_posts,
        'number_of_items_in_cart': number_of_items_in_cart,
    })

def about(request):
    if request.user.is_authenticated:
        # L'utilisateur est connecté, récupérez le panier de l'utilisateur
        cart = Cart.objects.filter(user=request.user).first()
        
        if cart is not None:
            number_of_items_in_cart = cart.items.count()
        else:
            number_of_items_in_cart = 0
    else:
        # L'utilisateur n'est pas connecté, initialisez le nombre d'articles dans le panier à zéro
        number_of_items_in_cart = 0

    context = {
        'number_of_items_in_cart': number_of_items_in_cart,
    }

    return render(request, 'ecommerce/about.html', context)

def contact(request):
    if request.user.is_authenticated:
        # L'utilisateur est connecté, récupérez le panier de l'utilisateur
        cart = Cart.objects.filter(user=request.user).first()
        
        if cart is not None:
            number_of_items_in_cart = cart.items.count()
        else:
            number_of_items_in_cart = 0
    else:
        # L'utilisateur n'est pas connecté, initialisez le nombre d'articles dans le panier à zéro
        number_of_items_in_cart = 0

    context = {
        'number_of_items_in_cart': number_of_items_in_cart,
    }

    return render(request, 'ecommerce/contact.html', context)
