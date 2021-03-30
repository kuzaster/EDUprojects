from django.contrib.auth import views as auth_view
from django.urls import path

from .views import MyLoginView, ProfilePageView, UserEditView, UserRegisterView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", MyLoginView.as_view(), name="login"),
    path("<int:pk>/edit_profile/", UserEditView.as_view(), name="edit-profile"),
    path(
        "password/",
        auth_view.PasswordChangeView.as_view(
            template_name="registration/change_password.html"
        ),
    ),
    path("<int:pk>/profile/", ProfilePageView.as_view(), name="profile-page"),
]
