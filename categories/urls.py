from django.urls import path
from .views import CategoryTreeView, CategoryListView, CategoryDetailView
app_name = 'categories' 

urlpatterns = [
    path('categories/tree/', CategoryTreeView.as_view(), name='category_tree'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
]