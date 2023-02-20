from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    model = Comment
    fields = ('content', )