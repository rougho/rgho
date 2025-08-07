from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

def email_new_subscribers(request, subscriber):
    try:
        template = render_to_string(
                'emails/subscriptions.html',
                { 
                    'receiver' : subscriber.email
                }
            )
        
        email = EmailMessage(
            subject='Thank You for Subscribing!',
            body=template,
            to=[subscriber.email]
        )

        email.content_subtype = 'html'
        email.send()
        logger.info(f"Subscription email sent successfully to {subscriber.email}")
        
    except Exception as e:
        logger.error(f"Failed to send subscription email to {subscriber.email}: {str(e)}")
        # Don't raise the exception to avoid breaking the user flow
        pass
