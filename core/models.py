from django.db import models
from uuid import uuid4
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


