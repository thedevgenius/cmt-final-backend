# serializers.py
from rest_framework import serializers
from .models import Category

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # Return the fields you want to show in the list view
        fields = ['id', 'name', 'slug', 'parent', 'icon_class', 'category_type', 'is_active', 'order']


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # Include all the fields you want to show on the detail page, including SEO metadata
        fields = [
            'id', 'name', 'slug', 'parent', 'icon_class', 'color', 
            'order', 'category_type', 'is_active', 'is_featured', 
            'meta_title', 'meta_description', 'meta_keywords'
        ]