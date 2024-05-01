from django.contrib import admin
from .models import Video


@admin.register(Video)
class videoAdmin(admin.ModelAdmin):
    list_display=['id','name','video_file']

