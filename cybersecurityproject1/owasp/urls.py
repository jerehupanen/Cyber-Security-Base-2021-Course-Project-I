from django.urls import path

from . import views

app_name = 'owasp'
urlpatterns = [
    # ex: /owasp/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /owasp/viewvideo/123/
    path('viewvideo/<int:video_id>/', views.view_video, name='view_video'),
    # ex: /owasp/addvideo/
    path('addvideo/', views.add_video, name='add_video'),
    # ex: /owasp/editvideo/123/
    path('editvideo/<int:video_id>/', views.edit_video, name='edit_video'),
    # ex: /owasp/signup
    path('signup/', views.signup_view, name='signup'),
    # ex: /owasp/login
    path('login/', views.login_view, name='login'),
     # ex: /owasp/logout
    path('logout/', views.logout_view, name='logout'),
    # ex: /owasp/profile/username
    path('profile/<str:username>/', views.profile_view, name='profile')
]