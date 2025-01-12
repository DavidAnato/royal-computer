from django.urls import path
from .views import *


urlpatterns = [
    path('', post_list, name='post_list'),
    
    # URL pour afficher un article de blog
    path('post/<slug:slug>/', post_detail, name='post_detail'),

    # URL pour éditer un commentaire
    path('comment/edit/<int:comment_id>/', edit_comment, name='edit_comment'),

    # URL pour supprimer un commentaire
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
]
