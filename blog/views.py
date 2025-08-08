from django.shortcuts import render
from django.shortcuts import get_object_or_404
import markdown

from .models import Post, Category
from lib.subscribe_newsletter import subscribe_newsletter



# Create your views here.
def blog_home(request):
    # Get all published posts
    posts = Post.objects.filter(status='published').select_related('author').prefetch_related(
        'categories', 
        'tags', 
        'liked_by', 
        'bookmarked_by',
        'comments'
    ).order_by('-created_at')

    # Get 6 random categories
    all_categories = Category.objects.order_by('?')[:6]
   
    form = subscribe_newsletter(request)
    context = {
        'posts' : posts,
        'form' : form,
        'all_categories' : all_categories,
    }
    return render(request, 'blog/blog_home.html', context=context)


def blog_post(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')    
    
    # Convert markdown content
    md = markdown.Markdown(extensions=[
        'extra',
        'tables',
    ])
    converted = md.convert(post.content)
    post.content = converted

    # Increment view count
    post.views_count += 1
    post.save(update_fields=['views_count'])

    context = {
        'post': post,
        'reading_time': post.reading_time,
        'views_count': post.views_count,
        'likes_count': post.get_like_count(),
        'comments_count': post.get_comment_count(),
    }
    return render(request, 'blog/blog_post.html', context=context)


