from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    widgets = {
        'text': forms.Textarea(attrs={'class': 'form-control rounded-5', 'rows': 3, 'placeholder': 'Join the discussion and leave a comment!'}),
    }
