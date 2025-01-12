from django import forms
from .models import CartItem
from authentication.models import Address

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']

    promo_code = forms.CharField(max_length=20, label="Code promo", required=False)

from django import forms

class CartForm(forms.Form):
    # Champs pour mettre à jour les quantités des articles dans le panier
    quantities = forms.IntegerField(
        label="Quantité",
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )
    # Champ pour ajouter un code promo
    promo_code = forms.CharField(max_length=20, label="Code promo", required=False)

class ShippingAddressForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(ShippingAddressForm, self).__init__(*args, **kwargs)
        self.fields['shipping_address'] = forms.ModelChoiceField(
            queryset=Address.objects.filter(user=user),  # Filtrer les adresses par utilisateur connecté
            widget=forms.RadioSelect,  # Utilisez des boutons radio pour la sélection
            to_field_name='id',  # Spécifiez le champ à utiliser comme valeur
            required=False  # Rendre le champ optionnel
        )
