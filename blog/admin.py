from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Post, Comment, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'post_count', 'color_display', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Category Info', {
            'fields': ('name', 'slug', 'description', 'color')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def post_count(self, obj):
        return obj.get_post_count()
    post_count.short_description = 'Published Posts'
    
    def color_display(self, obj):
        return format_html(
            '<span style="color: {}; font-weight: bold;">● {}</span>',
            obj.color,
            obj.color
        )
    color_display.short_description = 'Color'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'post_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Tag Info', {
            'fields': ('name', 'slug')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def post_count(self, obj):
        return obj.get_post_count()
    post_count.short_description = 'Published Posts'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author', 'slug_display', 'status', 'featured', 'views_count', 
        'likes_count', 'comments_count', 'created_at', 'published_at'
    ]
    list_filter = [
        'status', 'featured', 'created_at', 'published_at', 
        'categories', 'tags', 'author'
    ]
    search_fields = ['title', 'content', 'author__username', 'author__email']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = [
        'uuid', 'views_count', 'likes_count', 'comments_count', 
        'created_at', 'updated_at', 'reading_time', 'slug_display'
    ]
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'slug_display', 'author', 'co_authors', 'content', 'excerpt')
        }),
        ('Media', {
            'fields': ('featured_image', 'featured_image_alt'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('status', 'featured', 'published_at'),
        }),
        ('Organization', {
            'fields': ('categories', 'tags'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': (
                'uuid', 'views_count', 'likes_count', 'comments_count', 
                'reading_time', 'created_at', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ['categories', 'tags', 'liked_by', 'bookmarked_by']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author').prefetch_related('categories', 'tags')
    
    def slug_display(self, obj):
        """Display the actual slug used in URLs"""
        return format_html('<code>{}</code>', obj.slug)
    slug_display.short_description = 'URL Slug'
    slug_display.admin_order_field = 'slug'
    
    actions = ['make_published', 'make_draft', 'make_featured']
    
    def make_published(self, request, queryset):
        queryset.update(status='published')
        self.message_user(request, f'{queryset.count()} posts marked as published.')
    make_published.short_description = 'Mark selected posts as published'
    
    def make_draft(self, request, queryset):
        queryset.update(status='draft')
        self.message_user(request, f'{queryset.count()} posts marked as draft.')
    make_draft.short_description = 'Mark selected posts as draft'
    
    def make_featured(self, request, queryset):
        queryset.update(featured=True)
        self.message_user(request, f'{queryset.count()} posts marked as featured.')
    make_featured.short_description = 'Mark selected posts as featured'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'post_title', 'author', 'content_preview', 'active', 
        'flagged', 'likes_count', 'created_at'
    ]
    list_filter = ['active', 'flagged', 'created_at', 'post']
    search_fields = ['content', 'author__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at', 'likes_count']
    
    fieldsets = (
        ('Comment', {
            'fields': ('post', 'author', 'content', 'parent')
        }),
        ('Moderation', {
            'fields': ('active', 'flagged')
        }),
        ('Statistics', {
            'fields': ('likes_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ['liked_by']
    
    def post_title(self, obj):
        return obj.post.title
    post_title.short_description = 'Post'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    actions = ['approve_comments', 'flag_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(active=True, flagged=False)
        self.message_user(request, f'{queryset.count()} comments approved.')
    approve_comments.short_description = 'Approve selected comments'
    
    def flag_comments(self, request, queryset):
        queryset.update(flagged=True)
        self.message_user(request, f'{queryset.count()} comments flagged.')
    flag_comments.short_description = 'Flag selected comments'
