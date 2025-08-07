from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.conf import settings
import os
from .models import Resume

# Create your views here.

def resume_view(request):
    # Get the first resume (or you can filter by specific criteria)
    try:
        resume = Resume.objects.first()  # Gets the first resume
        # Or use: resume = Resume.objects.get(id=1)  # Gets specific resume by ID
    except Resume.DoesNotExist:
        resume = None
    
    context = {
        'resume': resume,
    }
    return render(request, 'resume/resume.html', context=context)

def download_resume_pdf(request, resume_id):
    """Download the resume PDF file"""
    resume = get_object_or_404(Resume, id=resume_id)
    
    if not resume.pdf_resume:
        raise Http404("PDF file not found")
    
    file_path = resume.pdf_resume.path
    
    if not os.path.exists(file_path):
        raise Http404("PDF file not found")
    
    with open(file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        file_name = resume.full_name
        file_name = file_name.replace(' ','-')
        response['Content-Disposition'] = f'attachment; filename="{resume.full_name}_Resume.pdf"'
        return response