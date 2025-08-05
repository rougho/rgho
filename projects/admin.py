from django.contrib import admin
from .models import Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
    """Inline admin for managing project images"""
    model = ProjectImage
    extra = 3  # Show 3 empty image upload fields by default
    fields = ['image', 'caption','featured', 'order']
    readonly_fields = ['uploaded_at']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at', 'image_count']
    list_filter = ['created_at', 'created_by']
    search_fields = ['title', 'description', 'technologies']
    readonly_fields = ['slug', 'created_by', 'created_at', 'updated_at']
    
    def get_inlines(self, request, obj):
        """Only show ProjectImageInline when editing existing projects"""
        if obj:  # obj exists = editing existing project
            return [ProjectImageInline]
        else:  # obj is None = creating new project
            return []
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = 'Images'
