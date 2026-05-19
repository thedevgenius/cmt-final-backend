# serializers.py
from rest_framework import serializers
from .models import Category

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # Return the fields you want to show in the list view
        fields = ['id', 'name', 'slug', 'parent', 'icon_class', 'category_type', 'is_active', 'order']