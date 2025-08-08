from django.urls import path
from .views import (
    index,
    contact,
    unsubscribe,
)

urlpatterns = [
    path('', index, name='homepage'),
    path('contact/', contact, name='contact'),
    path('unsubscribe/<uuid:uuid>/', unsubscribe, name='unsubscribe'),
]