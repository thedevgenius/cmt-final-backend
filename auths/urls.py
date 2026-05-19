from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RequestOTPView, VerifyOTPView

app_name = 'auths' 

urlpatterns = [
    path('otp/request/', RequestOTPView.as_view(), name='request_otp'),
    path('otp/verify/', VerifyOTPView.as_view(), name='verify_otp'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]