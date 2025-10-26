from django.shortcuts import render
from django.views import generic
from .models import Post


# Create your views here.


class Publicpost(generic.ListView):
    model = Post
    template_name = 'blog/public_post.html'
