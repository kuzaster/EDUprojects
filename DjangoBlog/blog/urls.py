from django.urls import path

from .views import (
    AddCommentView,
    AddPostView,
    DeletePostView,
    EditPostView,
    HomeView,
    PostDetailView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("post/<int:pk>", PostDetailView.as_view(), name="detail-post"),
    path("add_post", AddPostView.as_view(), name="add-post"),
    path("post/edit/<int:pk>", EditPostView.as_view(), name="edit-post"),
    path("post/<int:pk>/delete", DeletePostView.as_view(), name="delete-post"),
    path("post/<int:pk>/comment", AddCommentView.as_view(), name="add-comment"),
]
