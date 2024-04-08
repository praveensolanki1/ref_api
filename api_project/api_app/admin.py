from django.contrib import admin
from .models import User,Referral

# This code snippet is registering the `User` model with the Django admin interface.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'referral_code', 'timestamp_of_registration','points')
    search_fields = ('name', 'email')
    list_filter = ('timestamp_of_registration',)




admin.site.register(Referral)    