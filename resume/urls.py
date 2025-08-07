from django.urls import path
from .views import (
    resume_view,
    download_resume_pdf,
)


urlpatterns = [
    path('', resume_view, name='resume'),
    path('download/<int:resume_id>/', download_resume_pdf, name='download_resume_pdf'),
]