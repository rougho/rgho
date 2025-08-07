from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

def email_new_subscribers(request, subscriber):
    try:
        template = render_to_string(
                'emails/subscriptions.html',
                { 
                    'receiver' : subscriber.split('@')[0]
                }
            )
        
        email = EmailMessage(
            subject="🚀 You're In! Welcome aboard!",
            body=template,
            to=[subscriber]
        )

        email.content_subtype = 'html'
        email.send()
        logger.info(f"Subscription email sent successfully to {subscriber}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send subscription email to {subscriber}: {str(e)}")
        # Don't raise the exception to avoid breaking the user flow
        pass


def email_contact_confirmation(request, id,email, full_name):
    try:
        template = render_to_string(
                'emails/contact_confirmation.html',
                { 
                    'full_name' : full_name,
                    'id' : id,
                }
            )
        
        email = EmailMessage(
            subject='📧 Message Received. Thanks for reaching out!',
            body=template,
            to=[email]
        )

        email.content_subtype = 'html'
        email.send()
        logger.info(f"Contact form response email sent successfully to {email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send Contact form response email to {email}: {str(e)}")
        # Don't raise the exception to avoid breaking the user flow
        pass
