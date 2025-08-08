from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from .forms import EmailSubscriptionForm, ContactForm
from .models import EmailSubscription
from projects.models import Project
from resume.models import Resume
from lib.emails_hanlder import email_new_subscribers, email_contact_confirmation

# Create your views here.
def base(request):
    pass

def index(request):
    if request.method == 'POST':
        form = EmailSubscriptionForm(request.POST)
        if form.is_valid():
            subscription_instance = form.save()
            email_new_subscribers(request, subscription_instance)
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
    resume = Resume.objects.first()
    
    return render(request, 'core/index.html', {'form': form, 'projects': projects, 'resume' : resume})



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