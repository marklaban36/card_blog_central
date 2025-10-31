from django.shortcuts import render
from django.views import generic
from django.views.generic import DetailView
from .models import Post

# Create your views here.


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1)
    template_name = "blog/public_post.html"
    paginate_by = 20
