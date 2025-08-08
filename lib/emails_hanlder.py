from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

def email_new_subscribers(request, subscription_instance):
    try:
        # Build the correct unsubscribe URL
        unsubscribe_path = reverse('unsubscribe', kwargs={'uuid': subscription_instance.uuid})
        unsubscribe_url = request.build_absolute_uri(unsubscribe_path)
        
        template = render_to_string(
                'emails/subscriptions.html',
                { 
                    'receiver': subscription_instance.email.split('@')[0],
                    'uuid': subscription_instance.uuid,
                    'unsubscribe_url': unsubscribe_url,
                    'request': request
                }
            )
        
        email = EmailMessage(
            subject="🚀 You're In! Welcome aboard!",
            body=template,
            to=[subscription_instance.email]
        )

        email.content_subtype = 'html'
        email.send()
        logger.info(f"Subscription email sent successfully to {subscription_instance.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send subscription email to {subscription_instance.email}: {str(e)}")
        return False


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
        return False
