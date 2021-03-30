from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from blog.models import MyUser


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    mobile = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    skype = forms.CharField(
        max_length=250, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = MyUser
        fields = ["avatar", "first_name", "last_name", "email", "mobile", "skype"]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"


class EditProfileForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = "__all__"
