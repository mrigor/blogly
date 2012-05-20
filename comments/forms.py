from django import forms
from django.forms import Textarea
from comments.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('thing_id', 'author', 'parent_id', 'type', 'num_edits',
            'is_active', 'upds', 'downs', 'thread_id', 'reverse_thread_id',)
        widgets = {
            'content': Textarea(attrs={'cols': 70, 'rows': 3}),
        }
