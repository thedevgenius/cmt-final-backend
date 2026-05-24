from django.urls import path
from .views import BusinessListAPIView

app_name = 'businesses' 

urlpatterns = [
    path('businesses/', BusinessListAPIView.as_view(), name='business_list'),
]