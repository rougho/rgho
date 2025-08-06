from django.shortcuts import render
from projects.models import Project
from resume.models import Resume
import markdown
from django.shortcuts import get_object_or_404

# Create your views here.

def projects_view(request):
    projects = Project.objects.all()
    resume = Resume.objects.first()
    
    # Add split technologies to each project
    for project in projects:
        project.techs = [tech.strip() for tech in project.technologies.split(',') if tech.strip()]
    
    context = {
        'projects' : projects,
        'resume': resume,
    }
    return render(request, 'projects/projects.html', context=context)


def single_project_view(request, slug):
    project = get_object_or_404(Project, slug=slug)
    resume = Resume.objects.first()
    
    # Get non-featured images for sidebar
    sidebar_images = project.images.filter(featured=False).order_by('order', 'uploaded_at')
    
    # Enable tables explicitly with extra extensions
    md = markdown.Markdown(extensions=[
        'extra',    # This should include tables
        'tables',   # Explicitly enable tables
    ])
    
    # Debug: let's see what gets converted
    converted = md.convert(project.description)
    
    project.description = converted
    
    context = {
        'project': project,
        'sidebar_images': sidebar_images,
        'resume': resume,
    }
    return render(request, 'projects/single_project.html', context=context)