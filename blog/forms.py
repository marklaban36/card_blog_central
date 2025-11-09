from .models import Comment
from .models import Post
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'slug',
            'featured_image',
            'content',
            'excerpt',
            'status',
        ]
        widgets = {
            'status': forms.RadioSelect(
                choices=Post._meta.get_field('status').choices
            ),
        }
