from django.urls import path
from . import views
from .views import delete_featured_image

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    path(
        'post/<slug:slug>/delete-image/',
        delete_featured_image,
        name='delete_featured_image',
    ),
    path(
        'post/<slug:slug>/comment/<int:comment_id>/edit/',
        views.comment_edit,
        name='comment_edit',
    ),
    path(
        'post/<slug:slug>/comment/<int:comment_id>/delete/',
        views.comment_delete,
        name='comment_delete',
    ),
]
