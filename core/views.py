from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from .forms import ContactForm
from .models import EmailSubscription
from projects.models import Project
from resume.models import Resume
from lib.emails_hanlder import email_contact_confirmation
from lib.subscribe_newsletter import subscribe_newsletter
import requests 
import os
import json
from datetime import datetime
    

# Create your views here.
def base(request):
    pass

def index(request):
    form = subscribe_newsletter(request)
    
    projects = Project.objects.all().order_by('-created_at')[:3]
    resume = Resume.objects.first()


    # GITHUB ACTIVITY
    GITHUB_BASE_URL = 'https://api.github.com'
    user_name = 'rougho'
    repository_url = f"{GITHUB_BASE_URL}/users/{user_name}/repos?sort=created&direction=desc"
    personal_access_token = os.getenv('GITHUB_TOKEN')
    headers = {
        'Authorization': f"Bearer {personal_access_token}" }
    repo_response = requests.get(repository_url, headers=headers)
    if repo_response.status_code == 200:
        data = []
        repositories = repo_response.json()[:3]
        for repo in repositories:
            repo_dict = {}
            name = repo.get('name')
            url = f'https://api.github.com/repos/rougho/{name}/commits'
            commits = requests.get(url, headers=headers).json()[:3]
            commit_list = []
            for commit in commits:
                commit_data = {
                    'author': commit.get('commit', {}).get('author', {}).get('name', ''),
                    'committer': commit.get('commit', {}).get('committer', {}).get('name', ''),
                    'message': commit.get('commit', {}).get('message', ''),
                    'time': datetime.strptime(
                        commit.get('commit', {}).get('committer', {}).get('date', ''),
                        "%Y-%m-%dT%H:%M:%SZ"
                    )
                }
                commit_list.append(commit_data)
            repo_dict[name] = commit_list
            data.append(repo_dict)



        
    ####################
    return render(request, 'core/index.html', {'form': form, 'projects': projects, 'resume': resume, 'github_activity': data if 'data' in locals() else []})



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form first to get the ID
            contact_instance = form.save()
            
            # Now get the data including the auto-generated ID
            email = form.cleaned_data['email']
            full_name = contact_instance.full_name  # Use the property from the model
            contact_id = contact_instance.id
            
            if email_contact_confirmation(request, id=contact_id, email=email, full_name=full_name):
                messages.success(request, 'Thank you for contacting me! I will get back to you soon.')
                return redirect('homepage')  # Redirect to avoid form resubmission
            else:
                messages.error(request, 'Something happened. Please contact via email address after 48 hours.')

        else:
            # Handle specific field errors
            for field, errors in form.errors.items():
                for error in errors:
                    if field == 'email':
                        messages.error(request, f'Email: {error}')
                    elif field == 'phone_number':
                        messages.error(request, f'Phone: {error}')
                    elif field == 'name':
                        messages.error(request, f'First name: {error}')
                    elif field == 'last_name':
                        messages.error(request, f'Last name: {error}')
                    elif field == 'message':
                        messages.error(request, f'Message: {error}')
                    else:
                        messages.error(request, f'{field.title()}: {error}')
            
            # If no specific errors were found, show general message
            if not form.errors:
                messages.error(request, 'Please correct the errors in the form.')
    else:
        form = ContactForm()
    
    resume = Resume.objects.first()
    return render(request, 'core/contact.html', {'form': form, 'resume': resume})


def unsubscribe(request, uuid):
    """
    Handle email subscription unsubscribe requests
    """
    try:
        subscription = get_object_or_404(EmailSubscription, uuid=uuid)
        
        if request.method == 'POST':
            # User confirmed unsubscribe
            email = subscription.email
            subscription.delete()
            messages.success(request, f'You have been successfully unsubscribed from my newsletter.')
            return render(request, 'emails/unsubscribe_success.html', {'email': email})
        
        # Show confirmation page
        return render(request, 'emails/unsubscribe_confirm.html', {'subscription': subscription})
        
    except EmailSubscription.DoesNotExist:
        raise Http404("Invalid unsubscribe link or subscription not found.")