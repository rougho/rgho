from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EmailSubscriptionForm
from projects.models import Project

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = EmailSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for subscribing! We will notify you soon.')
            return redirect('homepage')
        else:
            if 'email' in form.errors:
                email_errors = form.errors['email']
                if any('already subscribed' in str(error) for error in email_errors):
                    messages.error(request, 'This email is already subscribed to our newsletter.')
                else:
                    messages.error(request, 'Please enter a valid email address.')
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        form = EmailSubscriptionForm()
    
    projects = Project.objects.all().order_by('-created_at')[:3]
    
    return render(request, 'core/index.html', {'form': form, 'projects': projects})