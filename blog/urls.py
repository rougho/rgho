from django.urls import path
from .views import (
    blog_home,
    blog_post,
)

urlpatterns = [
    path('', blog_home, name='blog_home_page'),
    path('<slug:slug>/', blog_post, name='blog_post'),
]