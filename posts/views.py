from typing import Any, Dict
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from .models import Post, Status
from django.urls import reverse_lazy

class PostListView(ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published_status = Status.objects.get(name="published")
        context["post_list"] = Post.objects.filter(
            status=published_status
            ).order_by("created_on").reverse()
        return context

class DraftPostListView(LoginRequiredMixin, ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        draft_status = Status.objects.get(name="draft")
        context["post_list"] = Post.objects.filter(
            author = self.request.user
        ).filter(
            status=draft_status
            ).order_by("created_on").reverse()
        return context


class PostDetailView(DetailView):
    template_name = "posts/detail.html"
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = "posts/new.html"
    model = Post
    fields = ['title', 'subtitle', 'body', 'status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "posts/edit.html"
    model = Post
    fields = ['title','subtitle', 'body', 'status']

    def test_func(self):
        post_obj = self.get_object()
        return post_obj.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "posts/delete.html"
    model = Post
    success_url = reverse_lazy('list')

    def test_func(self):
        post_obj = self.get_object()
        return post_obj.author == self.request.user
