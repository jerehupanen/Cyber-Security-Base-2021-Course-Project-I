from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm, UserModel
from django.contrib.auth import password_validation

class AddVideo(forms.ModelForm):
    class Meta:
        model = models.VideoItem
        fields = ['poster', 'videoTitle', 'videoLink', 'date']

class AddFeedback(forms.ModelForm):
    class Meta:
        model = models.VideoFeedback
        fields = ['poster', 'videoItem', 'comment']
        exclude = ('poster', 'videoItem')

class AddProfileInformation(forms.ModelForm):
    class Meta:
        model = models.ProfileInformation
        fields = ['user', 'username', 'email', 'phone']
        exclude = ('user', 'username')

class UserRegistrationForm(UserCreationForm):
    email = None
    password2 = None

    class Meta:
        model = UserModel
        fields = ('username', 'password1')