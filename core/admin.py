from django.contrib import admin
from .models import Contact


class ContactForm(admin.ModelAdmin):
    list_display = ['id','full_name', 'subject', 'date_time']
    readonly_fields = [field.name for field in Contact._meta.fields]
    search_fields = [field.name for field in Contact._meta.fields]

    def has_add_permission(self, request):
        return False


admin.site.register(Contact, ContactForm)


