from django.db import models
from django.contrib.auth import get_user_model
import markdown
from django.utils.safestring import mark_safe
import re
User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)  # Un slug est l'URL conviviale de l'article
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(help_text="Utilisez des balises personnalisées pour formater le texte.<br> <h5 style='font-weight: bold; margin-bottom: 0;'># Les sous titres #</h5> <br> ___ pour Séparation horizontale <br> <strong>*gras*</strong> <br> <em>-italique-</em> <br> _ <u>souligner</u> _")
    image = models.ImageField(upload_to='blog_images/')
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def formatted_content(self):

        content = self.content

        # Lien personnalisé
        link_pattern = r'\[(.*?)\]\((.*?)\)'
        content = re.sub(link_pattern, r'<a href="\2">\1</a>', content)

        # Ligne horizontale (hr)
        content = re.sub(r'___', r'<hr>', content)
        # Gras
        content = re.sub(r'\*(.*?)\*', r'<strong>\1</strong>', content)
        # Italique
        content = re.sub(r'-(.*?)-', r'<em>\1</em>', content)
        # Souligner
        content = re.sub(r'_(.*?)_', r'<u>\1</u>', content)
        # Titre h5 en gras avec margin-bottom: 0;
        content = re.sub(r'#(.*?)#', r'<h5 style="font-weight: bold; margin-bottom: 0;">\1</h5>', content)
        return mark_safe(content)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=True)
    
    def approve(self):
        self.approved_comment = True
        self.save()

    def formatted_content(self):
        text = self.text
        # Gras
        text = re.sub(r'\*(.*?)\*', r'<strong>\1</strong>', text)
        return mark_safe(text)
    
    def __str__(self):
        return self.text
