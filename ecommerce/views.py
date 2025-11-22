from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *
from cart_manage.models import CartItem, Cart
from blog.models import Post

def product_list(request):
    # Récupérez les paramètres
    #  exclue keyword, min_price et max_price si elles sont vides
    category_ids = request.GET.getlist('category[]')
    brand_ids = request.GET.getlist('brand[]')
    keyword = request.GET.get('keyword', '').strip() if request.GET.get('keyword', '').strip() else None
    min_price = request.GET.get('min_price') if request.GET.get('min_price') else None
    max_price = request.GET.get('max_price') if request.GET.get('max_price') else None
    page_number = request.GET.get('page', 1)

    # Filtre initial (en stock)
    products = Product.objects.filter(in_stock=True)

    # Application des filtres
    if category_ids:
        products = products.filter(category__id__in=category_ids)
    if brand_ids:
        products = products.filter(brand__id__in=brand_ids)
    if min_price and min_price.isdigit():
        products = products.filter(Q(price__gte=min_price) | Q(promo_price__gte=min_price))
    if max_price and max_price.isdigit():
        products = products.filter(Q(price__lte=max_price) | Q(promo_price__lte=max_price))
    if keyword:
        products = products.filter(Q(name__icontains=keyword) | Q(keyword_set__keyword__icontains=keyword))

    products = products.distinct().order_by('-created_at')

    # Pagination
    paginator = Paginator(products, per_page=12)
    try:
        products = paginator.page(page_number)
    except:
        products = paginator.page(paginator.num_pages)

    # Récupération des catégories, marques et mots-clés
    categories = Category.objects.all()
    brands = Brand.objects.all()
    keywords = KeyWord.objects.values_list('keyword', flat=True).distinct()

    return render(request, 'ecommerce/product_list.html', {
        'products': products,
        'categories': categories,
        'brands': brands,
        'selected_categories': [int(id) for id in category_ids],
        'selected_brands': [int(id) for id in brand_ids],
        'selected_min_price': min_price,
        'selected_max_price': max_price,
        'selected_keyword': keyword,
        'keywords': keywords,
        'query_string': request.GET.urlencode(),
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

    rating = product.average_rating()
    full_stars = int(rating)
    half_stars = 1 if (rating - full_stars) >= 0.5 else 0  
    empty_stars = 5 - (full_stars + half_stars)

    if user.is_authenticated:
        cart = Cart.objects.get(user=user)
        product_in_cart = CartItem.objects.filter(cart=cart, product=product).exists()
    else:
        product_in_cart = False

    return render(request, 'ecommerce/product_detail.html', {
        'product': product,
        'similar_products': similar_products,
        'product_in_cart': product_in_cart,
        'rating': {
            'full_stars': range(full_stars),
            'half_stars': range(half_stars),
            'empty_stars': range(empty_stars),
            'rate': rating,
        }

    })


def home(request):
    products = Product.objects.filter(in_stock=True)
    vedettes_products = Product.objects.filter(in_stock=True).filter(is_vedette=True).order_by('-created_at')[:5]
    new_products = Product.objects.filter(in_stock=True).filter(is_new=True).order_by('-created_at')
    promo_products = Product.objects.filter(in_stock=True).filter(in_promo=True).order_by('-created_at')
    latest_posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')[:4]


    return render(request, 'ecommerce/index.html', {
        'products': products,
        'vedettes_products': vedettes_products,
        'new_products': new_products,
        'promo_products': promo_products,
        'latest_posts': latest_posts,
    })

def about(request):
    return render(request, 'ecommerce/about.html')

def contact(request):
    return render(request, 'ecommerce/contact.html')
