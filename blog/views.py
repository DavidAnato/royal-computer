from math import ceil
from django.shortcuts import render, redirect, get_object_or_404
from cart_manage.models import Cart
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *
from .forms import *

# Constantes
PER_PAGE = 8

def post_list(request):
    user = request.user

    # Récupération des articles publiés, triés par date de publication
    all_posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')

    latest_post = all_posts.first()

    other_posts = all_posts.exclude(pk=latest_post.pk)

    # Récupération des paramètres de recherche, de filtre et de tri depuis la requête
    search_term = request.GET.get('search', '')
    category_ids = request.GET.getlist('category')
    sort_by = request.GET.get('sort_by', 'published_date')

    # Filtrage des articles de blog en fonction des paramètres
    posts = Post.objects.filter(published_date__isnull=False)

    if search_term:
        posts = posts.filter(Q(title__icontains=search_term) | Q(content__icontains=search_term))

    if category_ids:
        posts = posts.filter(categories__in=category_ids)

    # Tri des articles
    allowed_sorts = ['published_date', 'title', 'author']  # Liste des champs de tri autorisés
    if sort_by in allowed_sorts:
        posts = posts.order_by(sort_by)
    else:
        sort_by = 'published_date'  # Utilisation du tri par date par défaut

    # Pagination
    paginator = Paginator(posts, per_page=PER_PAGE)
    page_number = request.GET.get('page', 1)
    try:
        page_number = max(int(page_number), 1)
    except ValueError:
        page_number = 1
    posts = paginator.get_page(page_number)

    # Récupération des catégories pour les filtres
    categories = Category.objects.all()
    mid_index = ceil(len(categories) / 2)
    categories_left = categories[:mid_index]
    categories_right = categories[mid_index:]

    # Récupération du panier de l'utilisateur s'il est authentifié
    cart = None
    number_of_items_in_cart = 0
    if user.is_authenticated:
        cart = Cart.objects.filter(user=user).first()
        if cart:
            number_of_items_in_cart = cart.items.count()

    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'categories': categories,
        'categories_left': categories_left,
        'categories_right': categories_right,
        'selected_categories': category_ids,
        'search_term': search_term,
        'selected_sort_by': sort_by,
        'latest_post': latest_post,
        'other_posts': other_posts,
        'number_of_items_in_cart': number_of_items_in_cart,
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published_date__isnull=False)
    user = request.user

    if request.method == 'POST':
        # Création d'un nouveau commentaire
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  # Utilisateur actuel
            comment.save()
    else:
        form = CommentForm()

    # Exclure l'article courant de la liste des 4 derniers articles
    latest_posts = Post.objects.filter(published_date__isnull=False).exclude(pk=post.pk).order_by('-published_date')[:4]

    comments = post.comments.filter(approved_comment=True)

    number_of_items_in_cart = 0  # Initialisation par défaut
    if user.is_authenticated:
        cart = Cart.objects.filter(user=user).first()
        if cart:
            number_of_items_in_cart = cart.items.count()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'latest_posts': latest_posts,  # Ajout des 4 derniers articles
        'number_of_items_in_cart': number_of_items_in_cart
    })

def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', slug=comment.post.slug)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/edit_comment.html', {'form': form, 'comment': comment})

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_slug = comment.post.slug  # Conserver le slug de l'article pour redirection

    if request.user == comment.author:  # Vérifie que l'utilisateur est l'auteur du commentaire
        comment.delete()

    return redirect('post_detail', slug=post_slug)
