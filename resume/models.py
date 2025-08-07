from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
import os


# Create your models here.
def image_upload_path(instance, filename):
    """Generate upload path: resumes/profile_photos/{filename}"""
    if hasattr(instance, 'resume') and instance.resume and instance.resume.full_name:
        # For nested models that have a resume relationship
        safe_name = instance.resume.full_name.replace(' ', '_').lower()
        return f'resumes/{safe_name}/profile_photos/{filename}'
    elif hasattr(instance, 'full_name') and instance.full_name:
        # For the Resume model itself
        safe_name = instance.full_name.replace(' ', '_').lower()
        return f'resumes/{safe_name}/profile_photos/{filename}'
    else:
        # Fallback when name is not available yet
        return f'resumes/profile_photos/{filename}'


class Resume(models.Model):
    image = models.ImageField(upload_to=image_upload_path)
    pdf_resume = models.FileField(upload_to=image_upload_path, blank=True, null=True, help_text="Upload your resume as PDF")
    full_name = models.CharField(default='Rouhollah Ghobadinezhad', null=False, max_length=30, blank=False)
    birthday = models.DateField(blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    phone = PhoneNumberField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=False)


    def __str__(self):
        return f'{self.full_name}'



class Experience(models.Model):
    connect_to = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experiences')
    job_title = models.CharField(max_length=100, null=False, blank=False)
    company = models.CharField(max_length=100, null=False, blank=False)
    from_date = models.DateField(null=False, blank=False)
    to_date = models.DateField(null=False, blank=False)
    location = models.CharField(max_length=50, null=False, blank=False)
    job_description = models.TextField(null=False, blank=False)



class Project(models.Model):
    connect_to = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    technologies = models.CharField(max_length=200, null=False, blank=False)
    url = models.URLField(blank=True, null=True)
    from_date = models.DateField(null=False, blank=False)
    to_date = models.DateField(blank=True, null=True)

class Education(models.Model):
    connect_to = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=100, null=False, blank=False)
    institution = models.CharField(max_length=100, null=False, blank=False)
    from_date = models.DateField(null=False, blank=False)
    to_date = models.DateField(null=False, blank=False)
    location = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=False)

class Skill(models.Model):
    connect_to = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    category = models.CharField(max_length=50, null=False, blank=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ], null=False, blank=False)

class Other(models.Model):
    connect_to = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='others')
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)


# Signal handlers to delete files when model instances are deleted
@receiver(post_delete, sender=Resume)
def delete_resume_files(sender, instance, **kwargs):
    """Delete image and PDF files when Resume instance is deleted"""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
    
    if instance.pdf_resume:
        if os.path.isfile(instance.pdf_resume.path):
            os.remove(instance.pdf_resume.path)


@receiver(pre_save, sender=Resume)
def delete_old_files_on_change(sender, instance, **kwargs):
    """Delete old files when new files are uploaded"""
    if not instance.pk:
        return False  # New instance, nothing to delete

    try:
        old_resume = Resume.objects.get(pk=instance.pk)
    except Resume.DoesNotExist:
        return False

    # Delete old image if a new one is uploaded
    if old_resume.image and old_resume.image != instance.image:
        if os.path.isfile(old_resume.image.path):
            os.remove(old_resume.image.path)
    
    # Delete old PDF if a new one is uploaded
    if old_resume.pdf_resume and old_resume.pdf_resume != instance.pdf_resume:
        if os.path.isfile(old_resume.pdf_resume.path):
            os.remove(old_resume.pdf_resume.path)

