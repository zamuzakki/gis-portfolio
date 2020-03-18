from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import HomePageView, ProfileView, ProfileEditView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('profile', login_required(ProfileView.as_view()), name='profile'),
    path('profile/edit', login_required(ProfileEditView.as_view()), name='profile_edit'),
]