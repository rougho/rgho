from django.forms import ModelForm
from django import forms
from .models import EmailSubscription

class EmailSubscriptionForm(ModelForm):
    class Meta:
        model = EmailSubscription
        fields = ['email', 'agreement']
        error_messages = {
            'email': {
                'required': 'Please enter an email address.',
                'invalid': 'Please enter a valid email address.',
            }
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if EmailSubscription.objects.filter(email=email).exists():
                raise forms.ValidationError('This email is already subscribed to our newsletter.')
        return email