from django.contrib import admin
from .models import ProfileInformation, VideoItem, VideoFeedback

admin.site.register(VideoItem)
admin.site.register(VideoFeedback)
admin.site.register(ProfileInformation)