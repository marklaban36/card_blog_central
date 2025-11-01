from django.db import models
from django.contrib.auth.models import User

DRAFT = 0
PUBLISHED = 1
STATUS = (
    (DRAFT, "Draft"),
    (PUBLISHED, "Published"),
)


class Post(models.Model):
    # Basic identity
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    # Relations
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_posts",
    )

    # Content
    content = models.TextField()
    excerpt = models.TextField(blank=True)

    # Timestamps and status
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=DRAFT)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return "{} | written by {}".format(self.title, self.author)

    @property
    def is_published(self):
        return self.status == PUBLISHED

    def get_excerpt(self, max_len=200):
        if self.excerpt:
            return self.excerpt
        if len(self.content) > max_len:
            return self.content[: max_len - 3] + "..."
        return self.content


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="commenter",
    )
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return "Comment {!r} by {}".format(self.body, self.author)

    def approve(self):
        self.approved = True
        self.save()
