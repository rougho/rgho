from django.shortcuts import render
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