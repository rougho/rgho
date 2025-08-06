from django.contrib import admin
from .models import Resume, Experience, Project, Education, Skill, Other


# Inline admin classes for nested models
class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1  # Number of empty forms to display
    fields = ('job_title', 'company', 'job_description', 'location', 'from_date', 'to_date')


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1
    fields = ('title', 'technologies', 'description', 'from_date', 'to_date', 'url')


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1
    fields = ('degree', 'institution', 'description', 'location', 'from_date', 'to_date')


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    fields = ('category', 'name', 'level')


class OtherInline(admin.TabularInline):
    model = Other
    extra = 1
    fields = ('title',)


# Main Resume admin with all nested models as inlines
@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'createdAt')
    list_filter = ('createdAt',)
    search_fields = ('full_name', 'email')
    readonly_fields = ('createdAt',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('image', 'full_name', 'birthday', 'email', 'phone')
        }),
        ('Social Links', {
            'fields': ('github', 'linkedin')
        }),
        ('Metadata', {
            'fields': ('createdAt',),
            'classes': ('collapse',)
        })
    )
    
    inlines = [
        ExperienceInline,
        ProjectInline, 
        EducationInline,
        SkillInline,
        OtherInline,
    ]
