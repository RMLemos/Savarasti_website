from django.contrib import admin
from accounts.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = 'country', 'interests', 'bio',
    list_per_page = 10