from django.db import models
from uuid import uuid4
from phonenumber_field.modelfields import PhoneNumberField

from django.core.exceptions import ValidationError

class EmailSubscription(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True, null=False)
    email = models.EmailField(blank=False, null=False)
    agreement = models.BooleanField(blank=False,null=False)
    createdAt = models.DateTimeField(auto_now_add=True, null=False)

    def clean(self):
        if EmailSubscription.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({'email': 'This email already exists.'})
        return super().clean()


class Contact(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False) 
    last_name = models.CharField(max_length=100, blank=False, null=False)
    phone_number = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(blank=False, null=False)
    company = models.CharField(max_length=100, blank=True, null=True)
    date_time = models.DateTimeField(editable=False, auto_now_add=True)
    subject = models.CharField(max_length=200, blank=False, null=False)
    message = models.TextField(blank=False, null=False)
    
    class Meta:
        ordering = ['-date_time']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.name} {self.last_name} - {self.email}"
    
    @property
    def full_name(self):
        return f"{self.name} {self.last_name}"