from django.contrib.auth import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . import forms
from owasp.models import VideoItem, VideoFeedback, ProfileInformation

class IndexView(generic.ListView):
    template_name = 'owasp/index.html'
    context_object_name = 'latest_videos'

    def get_queryset(self):
        """Return the last five published videos."""
        return VideoItem.objects.order_by('date')[:5]

def view_video(request, video_id):
    video = get_object_or_404(VideoItem, pk=video_id)
    comments = VideoFeedback.objects.filter(videoItem_id = video.id)

    if request.method == 'POST':
        form = forms.AddFeedback(request.POST)
        if form.is_valid():
            currentForm = form.save(commit=False)
            currentForm.poster = request.user
            currentForm.videoItem = video
            currentForm.save()
        return redirect('owasp:view_video', video_id)
    else:
        form = forms.AddFeedback()

    return render(request, 'owasp/view_video.html', {'video': video, 'comments': comments, 'form': form})

@login_required(login_url="/owasp/login/") #requires user to be logged in to use form
def add_video(request):
    if request.method == 'POST':
        form = forms.AddVideo(request.POST)
        if form.is_valid():
            currentForm = form.save(commit=False)
            currentForm.poster = request.user
            currentForm.save()
            return redirect('owasp:index')
    else:
        form = forms.AddVideo()
    return render(request, 'owasp/add_video.html', {'form':form})

def edit_video(request, video_id):
    return HttpResponse("You're editing video %s." % video_id)

def signup_view(request):
    if request.method == 'POST':
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid(): # returns true if form is valid, maybe paaswords dont match?
            user = form.save()
            login(request, user)
            return redirect('owasp:index')
    else:
        form = forms.UserRegistrationForm()
    return render(request, 'owasp/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('owasp:index')
    else:
        form = AuthenticationForm()
    return render(request, 'owasp/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('owasp:index')

def profile_view(request, username):
    try:
        profileInfo = ProfileInformation.objects.get(username = username)
    except ProfileInformation.DoesNotExist:
        profileInfo = None

    if request.method == 'POST':
        form = forms.AddProfileInformation(request.POST)
        if form.is_valid():
            if profileInfo is None:
                currentForm = form.save(commit=False)
                currentForm.user = request.user
                currentForm.username = request.user.username
                currentForm.save()
            else:
                profileInfo.email = request.POST.get('email')
                profileInfo.phone = request.POST.get('phone')
                profileInfo.save()

        return redirect('owasp:profile', username)
    else:
        if profileInfo is None:
            form = forms.AddProfileInformation()
        else:
            form = forms.AddProfileInformation(initial={"email": profileInfo.email, "phone": profileInfo.phone})
        return render(request, 'owasp/profile.html', {'username': request.user.username, 'profileInfo': profileInfo, 'form': form})