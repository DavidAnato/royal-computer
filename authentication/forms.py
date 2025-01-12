from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from .models import Address

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')
        

class LoginForm(forms.Form):
    username_or_email_or_phone = forms.CharField(label="Username, Email, or Phone Number")
    password = forms.CharField(widget=forms.PasswordInput)


User = get_user_model()

from django import forms
from .models import CustomUser

class SettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_photo',
                  'receive_confirmation_emails', 'receive_order_updates', 'receive_promotions',
                  'language', 'currency',
                  'payment_method', 'mobile_money_number', 'paypal_email',
                  'profile_visibility', 'data_sharing']
        
    profile_photo = forms.FileField(required=False)


    receive_confirmation_emails = forms.BooleanField(required=False)
    receive_order_updates = forms.BooleanField(required=False)
    receive_promotions = forms.BooleanField(required=False)
    profile_visibility = forms.BooleanField(required=False)
    data_sharing = forms.BooleanField(required=False)

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'city', 'postal_code']  # Liste des champs à inclure dans le formulaire
