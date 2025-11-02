from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post
from .forms import CommentForm


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1)
    template_name = "blog/public_post.html"
    paginate_by = 20


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=1)
    comments = post.comments.filter(approved=True)

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.approved = True  # auto-approve for now
                comment.save()
                return redirect("post_detail", slug=post.slug)
        else:
            return redirect("login")  # redirect if not logged in
    else:
        form = CommentForm()

    return render(request, "blog/post_detail.html", {
        "post": post,
        "comments": comments,
        "form": form,
    })
