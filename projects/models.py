from django.db import models
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
import os
import shutil
from django.conf import settings


def project_image_upload_path(instance, filename):
    """Generate upload path: projects/{project_id}/{filename}"""
    if hasattr(instance, 'project'):
        # For ProjectImage model - project should already exist
        return f'projects/{instance.project.id}/{filename}'
    else:
        # For Project model - this shouldn't be used anymore
        return f'projects/{instance.id}/{filename}'

# Create your models here.
class Project(models.Model):
    slug = models.UUIDField(default=uuid4, editable=False, null=False, unique=True)
    title = models.CharField(max_length=200, null=False)
    description = models.TextField(null=False)
    technologies = models.CharField(max_length=500, help_text="e.g., React, Django, PostgreSQL")
    github_url = models.URLField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    @property
    def featured_image(self):
        """Get the featured image for this project"""
        featured = self.images.filter(featured=True).first()
        return featured.image if featured else None


class ProjectImage(models.Model):
    """Model for storing multiple images per project"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=project_image_upload_path)
    caption = models.CharField(max_length=255, blank=True, help_text="Optional image caption")
    featured = models.BooleanField(default=False, help_text="Mark as featured image for this project")
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'uploaded_at']
    
    def __str__(self):
        return f"{self.project.title} - Image {self.id}"


@receiver(post_delete, sender=Project)
def delete_project_files(sender, instance, **kwargs):
    """Delete all project files when project is deleted"""
    # Delete the entire project folder
    project_folder = os.path.join(settings.MEDIA_ROOT, 'projects', str(instance.id))
    if os.path.exists(project_folder):
        shutil.rmtree(project_folder)


@receiver(post_delete, sender=ProjectImage)
def delete_project_image_file(sender, instance, **kwargs):
    """Delete image file when ProjectImage is deleted"""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)