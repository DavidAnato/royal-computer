from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="nom")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "catégorie"
        verbose_name_plural = "catégories"

class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="nom")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "marque"
        verbose_name_plural = "marques"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="catégorie")
    name = models.CharField(max_length=150, verbose_name="nom")
    image = models.ImageField(upload_to='product_images/', verbose_name="image")
    image_secondary = models.ImageField(upload_to='product_images/', verbose_name="image secondaire")
    description = models.TextField(verbose_name="description")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, verbose_name="marque")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="prix")
    promo_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="prix promo")
    in_promo = models.BooleanField(default=False, verbose_name="en promo")
    is_vedette = models.BooleanField(default=False, verbose_name="Vedette")
    in_stock = models.BooleanField(default=True, verbose_name="en stock")
    is_new = models.BooleanField(default=True, verbose_name="Nouveau")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="date de création")
    specification = models.TextField(verbose_name="Specification", null=True, blank=True)
    warranty_info = models.TextField(verbose_name="Info Garantie", null=True, blank=True)
    display = models.CharField(max_length=150, verbose_name="Ecran", null=True, blank=True)
    processor_capacity = models.CharField(max_length=150, verbose_name="Processeur", null=True, blank=True)
    camera_quality = models.CharField(max_length=150, verbose_name="Camera", null=True, blank=True)
    memory = models.CharField(max_length=150, verbose_name="Memoire RAM", null=True, blank=True)
    harddisk_capacity = models.CharField(max_length=150, verbose_name="Capacite memoire", null=True, blank=True)
    graphics = models.CharField(max_length=150, verbose_name="Graphisme", null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.promo_price is None or self.promo_price >= self.price:
            self.in_promo = False
            self.promo_price = None
        else:
            self.in_promo = True

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "produit"
        verbose_name_plural = "produits"

    def average_rating(self):
        ratings = Rating.objects.filter(product=self)
        if ratings.exists():
            total_ratings = ratings.count()
            sum_ratings = ratings.aggregate(models.Sum('rating'))['rating__sum']
            average = sum_ratings / total_ratings
            return average
        return 0.0


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="utilisateur")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="produit")
    rating = models.IntegerField(choices=[(1, '1 étoile'), (2, '2 étoiles'), (3, '3 étoiles'), (4, '4 étoiles'), (5, '5 étoiles')], verbose_name="notation")

    def __str__(self):
        return f"Notation de {self.product.name} par {self.user.username}"

    class Meta:
        verbose_name = "notation"
        verbose_name_plural = "notations"

class AdditionalImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_image_set', verbose_name="produit")
    image = models.ImageField(upload_to='additional_images/', verbose_name="image supplémentaire")

    def __str__(self):
        return f"Image supplémentaire pour {self.product.name}"

    class Meta:
        verbose_name = "image supplémentaire"
        verbose_name_plural = "images supplémentaires"

class KeyWord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='keyword_set', verbose_name="produit")
    keyword = models.CharField(max_length=100, verbose_name="Mot clé", null=True)

    def __str__(self):
        return f"Mots clés pour {self.product.name}"

    class Meta:
        verbose_name = "Mot clé"
        verbose_name_plural = "Mots clés"


# ############
