from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'mobile_number', 'gender', 'created_at', 'notifi_count')
    search_fields = ('first_name', 'last_name', 'email','notifi_count')
