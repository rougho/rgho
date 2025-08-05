from django.shortcuts import render
from projects.models import Project
import markdown
from django.shortcuts import get_object_or_404

# Create your views here.

def projects_view(request):
    return render(request, 'projects/projects.html', {})


def single_project_view(request, slug):
    project = get_object_or_404(Project, slug=slug)
    
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
    }
    return render(request, 'projects/single_project.html', context=context)