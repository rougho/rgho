from django.contrib import admin
from .models import Contact, EmailSubscription


class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','full_name', 'subject', 'date_time']
    readonly_fields = [field.name for field in Contact._meta.fields]
    search_fields = [field.name for field in Contact._meta.fields]

    def has_add_permission(self, request):
        return False


class EmailSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'agreement', 'createdAt']
    readonly_fields = ['uuid', 'createdAt']
    search_fields = ['email']


admin.site.register(Contact, ContactAdmin)
admin.site.register(EmailSubscription, EmailSubscriptionAdmin)


