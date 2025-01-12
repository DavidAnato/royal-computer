# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('generate_whatsapp_url/', views.generate_whatsapp_url, name='generate_whatsapp_url'),
    path('', views.cart, name='cart'),

    path('checkout/', views.checkout, name='checkout'),
    path('order_success/', views.order_success, name='order_success'),  # Créez cette vue pour afficher une confirmation de commande

]
