from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
# from phonenumber_field.modelfields import PhoneNumberField

class Language(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name='code')
    name = models.CharField(max_length=100, verbose_name='nom')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'langue'
        verbose_name_plural = 'langues'

class Currency(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name='code')
    name = models.CharField(max_length=100, verbose_name='nom')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'devise'
        verbose_name_plural = 'devises'

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100, verbose_name='nom')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'méthode de paiement'
        verbose_name_plural = 'méthodes de paiement'

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='e-mail')
    username = models.CharField(max_length=100, verbose_name='nom d\'utilisateur', unique=True)
    phone_number = models.CharField(max_length=100, verbose_name='numéro de téléphone', blank=True, null=True)
    phone_number_confirmed = models.BooleanField(default=False, verbose_name='Numéro de téléphone confirmé')
    profile_photo = models.ImageField(upload_to='profile_photos/', verbose_name='photo de profil', blank=True, null=True)
    
    # Préférences de notification
    receive_confirmation_emails = models.BooleanField(default=True, verbose_name='recevoir des e-mails de confirmation')
    receive_order_updates = models.BooleanField(default=True, verbose_name='recevoir des mises à jour de commande')
    receive_promotions = models.BooleanField(default=True, verbose_name='recevoir des promotions')
    
    # Préférences de langue et de devise
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, verbose_name='langue préférée')
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, verbose_name='devise')
      
    # Méthodes de paiement
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, verbose_name='méthode de paiement')
    mobile_money_number = models.CharField(max_length=20, verbose_name='numéro mobile money', blank=True)
    paypal_email = models.EmailField(verbose_name='adresse e-mail PayPal', blank=True)
    
    # Confidentialité et sécurité
    profile_visibility = models.BooleanField(default=True, verbose_name='visibilité du profil')
    data_sharing = models.BooleanField(default=True, verbose_name='autorisations de partage de données')
    
    # Google OAuth
    google_id = models.CharField(max_length=255, verbose_name='ID Google', blank=True)
    picture_url = models.URLField(verbose_name='URL de la photo de profil', blank=True)
    verified_email = models.BooleanField(default=False, verbose_name='e-mail vérifié')
    
    def is_phone_number_confirmed(self):
        if self.phone_number_confirmed:
            return self.phone_number_confirmed

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'utilisateur personnalisé'
        verbose_name_plural = 'utilisateurs personnalisés'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.username:
            self.username = self.email.split('@')[0]
            self.save()

        if self.profile_photo:
            img = Image.open(self.profile_photo.path)

            width, height = img.size
            if width != height:
                min_side = min(width, height)
                left = (width - min_side) / 2
                top = (height - min_side) / 2
                right = (width + min_side) / 2
                bottom = (height + min_side) / 2

                img = img.crop((left, top, right, bottom))
                img.save(self.profile_photo.path)


    

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    address = models.CharField(max_length=100, verbose_name='adresse')
    city = models.CharField(max_length=50, verbose_name='ville')
    postal_code = models.CharField(max_length=10, verbose_name='code postal')

    def __str__(self):
        return self.address
