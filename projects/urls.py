from django.urls import path
from .views import (
    projects_view,
    single_project_view
)

urlpatterns = [
    path('', projects_view, name='projects'),
    path('<str:slug>/', single_project_view, name='single_project')
]