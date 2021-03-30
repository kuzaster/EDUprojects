from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views import generic

from blog.models import MyUser

from .forms import SignUpForm


class ProfilePageView(generic.DetailView):
    model = MyUser
    template_name = "registration/user_profile.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProfilePageView, self).get_context_data(*args, **kwargs)

        user_page = get_object_or_404(MyUser, id=self.kwargs["pk"])

        context["user_page"] = user_page
        return context


class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class MyLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "registration/login.html"

    def get_success_url(self):
        return reverse("profile-page", args=[self.request.user.id])


class UserEditView(LoginRequiredMixin, generic.UpdateView):
    login_url = "login"
    model = MyUser
    template_name = "registration/edit_profile.html"
    fields = ["first_name", "last_name", "avatar", "mobile", "skype"]

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse("profile-page", args=[self.request.user.id])
