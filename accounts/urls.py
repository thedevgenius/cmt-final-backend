from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserProfileUpdateView, UserProfileView

app_name = 'users' 

urlpatterns = [
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile_update'),
    path('users/me/', UserProfileView.as_view(), name='profile_view'),
]