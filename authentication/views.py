from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as django_login, logout as django_logout, get_user_model
from django.contrib.auth.decorators import login_required
import requests

from authentication.utils import send_password_reset_email
from .forms import *
from .models import Address
from cart_manage.models import Order
from ecom import settings as django_settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
import random

User = get_user_model()

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Authenticate user
            user = User.objects.get(email=form.cleaned_data['email'])
            if user is not None:
                django_login(request, user)
                return redirect('home')
            else:
                return render(request, 'authentication/signup.html', status=400)


    return render(request, 'authentication/signup.html', context={'form': form})

def login(request):
    if request.method == 'POST':
        # Récupérer `next` depuis POST
        next_url = request.POST.get('next', None)
        print("##################")
        print(next_url)
        print("##################")

        username = request.POST.get('username')
        password = request.POST.get('password')

        # Recherche de l'utilisateur par différents identifiants
        user = None
        for field in ['username', 'email', 'phone_number']:
            try:
                user = User.objects.get(**{field: username})
                break
            except User.DoesNotExist:
                continue

        if user is not None and user.check_password(password):
            django_login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            error_message = 'Nom d\'utilisateur, email ou numéro de téléphone incorrect.'
            return render(
                request,
                'authentication/login.html',
                {
                    'error': error_message,
                }
            )

    return render(
        request,
        'authentication/login.html'
    )

def google_login(request):
    code = request.GET.get('code')
    # Exchange the authorization code for an access token
    token_response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": django_settings.GOOGLE_CLIENT_ID,
            "client_secret": django_settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": django_settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        },
    )
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return render(request, 'authentication/google_login.html', {'error': 'Failed to obtain access token.'})

    # Use the access token to obtain user info
    user_info_response = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        params={"access_token": access_token},
    )
    user_info = user_info_response.json()

    email = user_info.get("email")
    first_name = user_info.get("given_name")
    last_name = user_info.get("family_name")
    google_id = user_info.get("id")
    picture_url = user_info.get("picture")
    verified_email = user_info.get("verified_email", False)

    if not email:
        return render(request, 'authentication/google_login.html', {'error': 'Failed to obtain user email.'})

    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "first_name": first_name,
            "last_name": last_name,
            "google_id": google_id,
            "picture_url": picture_url,
            "verified_email": verified_email,
            "is_active": True,
        },
    )

    if not created:
        user.first_name = first_name
        user.last_name = last_name
        user.google_id = google_id
        user.picture_url = picture_url
        user.verified_email = verified_email
        user.save()

        django_login(request, user)
        return redirect('home')



    return render(request, 'authentication/google_login.html')

def logout(request):
    django_logout(request)
    return redirect('home')

@login_required
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=request.user).all()
    return render(request, 'authentication/profile.html', {'user': user, 'orders':orders})

@login_required
def settings(request):
    user = request.user

    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = SettingsForm(instance=user)

    return render(request, 'authentication/settings.html', {'form': form})

@login_required
def manage_address(request, address_id=None):
    user = request.user
    instance = None
    next = request.GET.get('next', None)
    if address_id:
        instance = get_object_or_404(Address, id=address_id)

    if request.method == 'POST':
        if 'delete' in request.POST:
            # Gérer la suppression d'une adresse
            if instance:
                instance.delete()
                return redirect('settings')
        else:
            form = AddressForm(request.POST, instance=instance)
            if form.is_valid():
                address = form.save(commit=False)
                address.user = user
                address.save()
                if next:
                    return redirect(next)
                return redirect('settings')
    else:
        form = AddressForm(instance=instance)

    template = 'authentication/manage_address.html'

    context = {
        'form': form,
        'address_id': address_id,
        'next': next
    }

    return render(request, template, context)
@login_required
def delete_account(request):

    if request.method == 'POST':
        # Si l'utilisateur confirme la suppression du compte
        if request.POST.get('confirm_delete'):
            user = request.user
            # Supprimez le compte de l'utilisateur
            user.delete()
            return redirect('home')  # Redirige vers la page d'accueil après la suppression du compte
        else:
            return redirect('setiings')  # Redirige vers la page de setiings si la suppression est annulée
    else:
        return render(request, 'authentication/delete_account.html')

def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Générer un OTP à 5 chiffres
            otp = ''.join([str(random.randint(0, 9)) for _ in range(5)])
            # Sauvegarder l'OTP temporairement
            user.otp = otp
            user.save()
            
            # Envoyer l'email avec l'OTP
            send_password_reset_email(email, otp)
            return redirect(f'/user/password_reset_confirm/?email={email}')
        except User.DoesNotExist:
            return render(request, 'authentication/password_reset.html', 
                        {'error': 'Email non trouvé'})

    return render(request, 'authentication/password_reset.html')

def password_reset_confirm(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        try:
            user = User.objects.get(email=email, otp=otp)
            # OTP valide, connecter l'utilisateur
            django_login(request, user)
            # Effacer l'OTP
            user.otp = None 
            user.save()
            return redirect('password_change')
        except User.DoesNotExist:
            return render(request, 'authentication/password_reset_confirm.html',
                        {'error': 'Code OTP invalide'})

    return render(request, 'authentication/password_reset_confirm.html')