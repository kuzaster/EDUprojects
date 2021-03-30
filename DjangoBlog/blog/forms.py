from django import forms

from .models import Comment, Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "author", "shot_body", "body")

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "author": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "value": "",
                    "id": "elder",
                    "type": "hidden",
                }
            ),
            "shot_body": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control"}),
        }


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "shot_body", "body")

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "shot_body": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control"}),
        }


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "body")

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control"}),
        }
