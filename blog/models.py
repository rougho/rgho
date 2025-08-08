from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from uuid import uuid4
import os

def post_media_upload_path(instance, filename):
    """Generate upload path for post media files"""
    # Ensure UUID exists (for new instances)
    if not instance.uuid:
        instance.uuid = uuid4()
    
    # Clean the title for use in path (remove special characters)
    clean_title = slugify(instance.title) if instance.title else 'untitled'
    
    # Use only first 50 chars of title to avoid path length issues
    clean_title = clean_title[:50] if len(clean_title) > 50 else clean_title
    
    # Create directory path: media/blog/{title-uuid}/
    # UUID ensures uniqueness even with identical titles
    return os.path.join('blog', f'{clean_title}-{str(instance.uuid)[:8]}', filename)



# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    # Core fields
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    co_authors = models.CharField(max_length=255, blank=True, help_text="Comma-separated list of co-authors")
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True, help_text="Short description of the post")
    # Status and publishing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    featured = models.BooleanField(default=False, help_text="Feature this post on homepage")
    
    # SEO fields
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="SEO keywords (comma separated)")
    
    # Media
    featured_image = models.ImageField(upload_to=post_media_upload_path, blank=True, null=True)
    featured_image_alt = models.CharField(max_length=100, blank=True, help_text="Alt text for featured image")
    
    # Engagement tracking
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    
    # Many-to-many relationships for engagement
    liked_by = models.ManyToManyField(User, blank=True, related_name='liked_posts')
    bookmarked_by = models.ManyToManyField(User, blank=True, related_name='bookmarked_posts')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Reading time estimation (in minutes)
    reading_time = models.PositiveIntegerField(default=0, help_text="Estimated reading time in minutes")
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['slug']),
            models.Index(fields=['featured', '-created_at']),
        ]
    

    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):

        if not self.uuid:
            self.uuid = uuid4()        
        if not self.slug:
            base_slug = slugify(self.title) if self.title else 'untitled'            
            if not base_slug or base_slug == 'untitled':
                self.slug = f"post-{str(self.uuid)[:8]}"
            else:
                self.slug = base_slug                
                if Post.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                # Instead of incrementing numbers, append part of UUID for guaranteed uniqueness
                    self.slug = f"{base_slug}-{str(self.uuid)[:8]}"
                
        
        if not self.excerpt and self.content:
            self.excerpt = self.content[:300] + "..." if len(self.content) > 300 else self.content
        
        if self.content:
            word_count = len(self.content.split())
            self.reading_time = max(1, round(word_count / 200))
        
        super().save(*args, **kwargs)
    

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def is_published(self):
        return self.status == 'published'
    
    def get_like_count(self):
        return self.liked_by.count()
    
    def get_comment_count(self):
        return self.comments.filter(active=True).count()


class Comment(models.Model):
    # Core fields
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments')
    content = models.TextField(max_length=1000)
    
    # Nested comments (replies)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    # Moderation
    active = models.BooleanField(default=True)
    flagged = models.BooleanField(default=False)
    
    # Engagement
    likes_count = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(User, blank=True, related_name='liked_comments')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'active', 'created_at']),
            models.Index(fields=['parent']),
        ]
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    def is_reply(self):
        return self.parent is not None
    
    def get_replies(self):
        return self.replies.filter(active=True)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text="Hex color code for category")
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'slug': self.slug})
    
    def get_post_count(self):
        return self.posts.filter(status='published').count()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:tag_posts', kwargs={'slug': self.slug})
    
    def get_post_count(self):
        return self.posts.filter(status='published').count()


# Add the many-to-many relationships to Post
Post.add_to_class('categories', models.ManyToManyField(Category, blank=True, related_name='posts'))
Post.add_to_class('tags', models.ManyToManyField(Tag, blank=True, related_name='posts'))