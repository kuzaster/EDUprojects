from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import AddCommentForm, CreatePostForm, EditPostForm
from .models import Comment, Post

# Create your views here.


class HomeView(ListView):
    model = Post
    template_name = "home.html"

    def get_ordering(self):
        ordering = self.request.GET.get("ordering", "-published")
        return ordering


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"

    def get_ordering(self):
        ordering = self.request.GET.get("ordering", "-published")
        return ordering


class AddPostView(CreateView):
    model = Post
    template_name = "add_post.html"
    form_class = CreatePostForm


class AddCommentView(CreateView):
    model = Comment
    template_name = "add_comment.html"
    form_class = AddCommentForm

    def get_success_url(self):
        return reverse("detail-post", args=[self.kwargs["pk"]])

    def form_valid(self, form):
        form.instance.post_id = self.kwargs["pk"]
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(AddCommentView, self).get_context_data(*args, **kwargs)

        current_post = get_object_or_404(Post, id=self.kwargs["pk"])

        context["current_post"] = current_post
        return context


class EditPostView(LoginRequiredMixin, UpdateView):
    login_url = "login"
    model = Post
    template_name = "edit_post.html"
    form_class = EditPostForm


class DeletePostView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    model = Post
    template_name = "delete_post.html"
    success_url = reverse_lazy("home")
