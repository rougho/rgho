from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Contact, EmailSubscription


class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','full_name', 'subject', 'date_time']
    readonly_fields = [field.name for field in Contact._meta.fields]
    search_fields = [field.name for field in Contact._meta.fields]

    def has_add_permission(self, request):
        return False


class EmailSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'agreement', 'createdAt', 'unsubscribe_link']
    readonly_fields = ['uuid', 'createdAt', 'unsubscribe_link']
    search_fields = ['email']
    
    def unsubscribe_link(self, obj):
        """Generate unsubscribe link for admin interface"""
        if obj.uuid:
            url = reverse('unsubscribe', args=[obj.uuid])
            return format_html('<a href="{}" target="_blank">Unsubscribe Link</a>', url)
        return "No UUID"
    unsubscribe_link.short_description = "Unsubscribe Link"


admin.site.register(Contact, ContactAdmin)
admin.site.register(EmailSubscription, EmailSubscriptionAdmin)


