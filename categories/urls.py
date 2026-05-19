from django.urls import path
from .views import CategoryTreeView, CategoryListView
app_name = 'categories' 

urlpatterns = [
    path('categories/tree/', CategoryTreeView.as_view(), name='category_tree'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
]