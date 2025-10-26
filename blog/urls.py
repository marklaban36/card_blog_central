from . import views
from django.urls import path

urlpatterns = [
    path('', views.Publicpost.as_view(), name='home'),
]