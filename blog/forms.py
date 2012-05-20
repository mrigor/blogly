from django import forms
from django.forms import Textarea
from blog.models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ('author', 'status', 'slug')
        widgets = {
            'body': Textarea(attrs={'cols': 15, 'rows': 5}),
        }
