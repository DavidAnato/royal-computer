from django.urls import path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('shop/', product_list, name='shop'),
    path('autocomplete_suggestions/', autocomplete_suggestions, name='autocomplete_suggestions'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

    

]
