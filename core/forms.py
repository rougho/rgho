from django.forms import ModelForm
from django import forms
from .models import EmailSubscription, Contact
from lib.phone_number_prefix import CountryPhoneWidget

class EmailSubscriptionForm(ModelForm):
    class Meta:
        model = EmailSubscription
        fields = ['email', 'agreement']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control border-0',
                'placeholder': 'email@codescandy.com',
                'required': True
            }),
            'agreement': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'required': True
            })
        }
        error_messages = {
            'email': {
                'required': 'Please enter an email address.',
                'invalid': 'Please enter a valid email address.',
            },
            'agreement': {
                'required': 'You must agree to receive newsletter updates.',
            }
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if EmailSubscription.objects.filter(email=email).exists():
                raise forms.ValidationError('This email is already subscribed to our newsletter.')
        return email
    
class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'last_name', 'phone_number', 'email', 'company', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }),
            'phone_number': CountryPhoneWidget(),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company name'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your message subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your message',
                'rows': 8
            })
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            return name.strip().title()
        return name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            return last_name.strip().title()
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            return email.lower().strip()
        return email

    def clean_company(self):
        company = self.cleaned_data.get('company')
        if company:
            return company.strip().title()
        return company

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message:
            return message.strip()
        return message