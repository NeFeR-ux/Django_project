from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'post_type', 'categories']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 10}),
        }