from django.urls import path
from .views import CategoryTreeView
app_name = 'categories' 

urlpatterns = [
    path('tree/', CategoryTreeView.as_view(), name='category_tree'),
]