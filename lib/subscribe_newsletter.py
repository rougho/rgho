from django.shortcuts import redirect
from django.contrib import messages
from core.forms import EmailSubscriptionForm
from lib.emails_hanlder import email_new_subscribers

def subscribe_newsletter(request):
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
        return EmailSubscriptionForm()