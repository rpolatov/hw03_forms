from .models import Post
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("text", "group",)
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 9}),
            "group": forms.Select(attrs={"class": "form-control"}),
        }  # С виджетами красивее!
