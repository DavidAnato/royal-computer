from math import ceil
from urllib.parse import urlencode
from django.shortcuts import render, redirect, get_object_or_404
from cart_manage.models import Cart
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *
from .forms import *

# Constantes
PER_PAGE = 8

def post_list(request):
    # Récupération des articles publiés, triés par date de publication
    all_posts = Post.objects.filter(published_date__isnull=False).order_by('-updated_date')
    latest_post = all_posts.first()

    # Si aucun post n'existe, retourner une page vide
    if not latest_post:
        return render(request, 'blog/post_list.html', {
            'posts': [],
            'other_posts': [],
            'categories': [],
            'categories_left': [],
            'categories_right': [],
            'selected_categories': [],
            'search_term': '',
            'latest_post': None,
            'query_string': '',
        })

    # Récupération des paramètres de recherche, de filtre et de tri depuis la requête
    search_term = request.GET.get('search', '')
    category_ids = request.GET.getlist('category')

    # Filtrage des articles
    posts = all_posts

    if search_term:
        posts = posts.filter(Q(title__icontains=search_term) | Q(content__icontains=search_term))

    if category_ids:
        posts = posts.filter(categories__in=category_ids)

    # Élimination des doublons
    posts = posts.distinct()

    # Pagination sur les posts filtrés
    paginator = Paginator(posts, per_page=PER_PAGE)
    page_number = request.GET.get('page', 1)
    try:
        page_number = max(int(page_number), 1)
    except ValueError:
        page_number = 1
    posts = paginator.get_page(page_number)

    # Préserver les paramètres de recherche, de filtre et de tri dans les liens de pagination
    query_params = {
        'search': search_term,
    }
    if category_ids:
        query_params['category'] = category_ids
    query_string = urlencode(query_params, doseq=True)  # `doseq=True` permet de gérer les listes (e.g., catégories)

    # Mise à jour des autres articles en fonction des filtres
    if search_term or category_ids:
        other_posts = posts  # Pagination sur les résultats filtrés
    else:
        other_posts = all_posts.exclude(pk=latest_post.pk)  # Pagination sur tous les posts sans filtre

    # Pagination sur other_posts
    paginator_other = Paginator(other_posts, per_page=PER_PAGE)
    other_posts_page_number = request.GET.get('page', 1)
    try:
        other_posts_page_number = max(int(other_posts_page_number), 1)
    except ValueError:
        other_posts_page_number = 1
    other_posts = paginator_other.get_page(other_posts_page_number)

    # Récupération des catégories pour les filtres
    categories = Category.objects.all()
    mid_index = ceil(len(categories) / 2)
    categories_left = categories[:mid_index]
    categories_right = categories[mid_index:]
    selected_categories = [int(category_id) for category_id in category_ids]

    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'other_posts': other_posts,  # Pagination des autres posts
        'categories': categories,
        'categories_left': categories_left,
        'categories_right': categories_right,
        'selected_categories': selected_categories,
        'search_term': search_term,
        'latest_post': latest_post,
        'query_string': query_string,  # Ajout de la chaîne de requête pour la pagination
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


    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'latest_posts': latest_posts,  # Ajout des 4 derniers articles
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
