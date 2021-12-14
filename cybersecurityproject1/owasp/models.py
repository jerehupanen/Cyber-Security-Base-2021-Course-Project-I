from django.db import models
from django.contrib.auth.models import User

# A video can only be linked to one user
class VideoItem(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    videoTitle = models.CharField('Video title', max_length=200)
    videoLink = models.CharField('Video link', max_length=500)
    date = models.DateTimeField('Date published')

# A feedback can only be linked to one video and one user
class VideoFeedback(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    videoItem = models.ForeignKey(VideoItem, on_delete=models.CASCADE)
    comment = models.TextField('Comment')

class ProfileInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField('Username', max_length=50)
    email = models.CharField('E-mail', max_length=200)
    phone = models.CharField('Phone number', max_length=50)