from django.contrib import admin

# Register your models here.
from .models import Asset, Review, Tag

admin.site.register(Asset)
admin.site.register(Review)
admin.site.register(Tag)
