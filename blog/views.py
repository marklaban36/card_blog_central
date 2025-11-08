from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from cloudinary.uploader import destroy

from .models import Post, Comment
from .forms import CommentForm, PostForm

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1)
    template_name = "blog/public_post.html"
    paginate_by = 6

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=1)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Comment submitted')

    comment_form = CommentForm()

    return render(request, "blog/post_detail.html", {
        "post": post,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
    })

@login_required
def create_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Post created successfully!")
        return HttpResponseRedirect(reverse('post_detail', args=[post.slug]))
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, "Post updated successfully!")
        return HttpResponseRedirect(reverse('post_detail', args=[post.slug]))
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return HttpResponseRedirect(reverse('home'))
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required
def delete_featured_image(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if post.featured_image and post.featured_image.public_id != 'placeholder':
        destroy(post.featured_image.public_id)
        post.featured_image = 'placeholder'
        post.save()
        messages.success(request, "Image deleted successfully.")
    else:
        messages.warning(request, "No image to delete.")
    return HttpResponseRedirect(reverse('edit_post', args=[slug]))

@login_required
def comment_edit(request, slug, comment_id):
    post = get_object_or_404(Post, slug=slug, status=1)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)

    if comment.author != request.user:
        messages.error(request, "You can only edit your own comments.")
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST, instance=comment)
        if comment_form.is_valid():
            comment_form.save()  # No change to approval status
            messages.success(request, 'Comment updated successfully!')
            return HttpResponseRedirect(reverse('post_detail', args=[slug]))
        else:
            messages.error(request, 'Error updating comment!')
    else:
        comment_form = CommentForm(instance=comment)

    return render(request, 'blog/edit_comment.html', {
        'form': comment_form,
        'comment': comment,
        'post': post,
    })


@login_required
def comment_delete(request, slug, comment_id):
    post = get_object_or_404(Post, slug=slug, status=1)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)

    if comment.author != request.user:
        messages.error(request, 'You can only delete your own comments!')
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))

    comment.delete()
    messages.success(request, 'Comment deleted!')
    return HttpResponseRedirect(reverse('post_detail', args=[slug]))
