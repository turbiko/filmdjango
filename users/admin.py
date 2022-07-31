from django.contrib import admin

# Register your models here.

from .models import Profile, Activity, Message

admin.site.register(Profile)
admin.site.register(Activity)
admin.site.register(Message)
