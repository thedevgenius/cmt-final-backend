from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from core.pagination import StandardResultsSetPagination
from .models import Category
from .serializers import CategoryListSerializer


class CategoryTreeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # 1. Fetch all active categories in ONE query, pulling only needed fields
        categories = Category.objects.filter(is_active=True).values(
            'id', 'name', 'slug', 'parent_id',
        )
        
        # 2. Create a dictionary to easily look up categories by their ID
        category_dict = {}
        for cat in categories:
            cat['children'] = [] # Initialize an empty children list for every category
            category_dict[cat['id']] = cat
            
        # 3. Build the tree
        tree = []
        for cat in category_dict.values():
            parent_id = cat['parent_id']
            
            if parent_id is None:
                # If it has no parent, it's a Root category
                tree.append(cat)
            else:
                # If it has a parent, append it to the parent's 'children' list
                parent = category_dict.get(parent_id)
                if parent:
                    parent['children'].append(cat)
                    
        return Response({
            "success": True,
            "data": tree
        })
    

class CategoryListView(ListAPIView):
    """
    API View to list all categories with filtering, searching, and pagination.
    """
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    pagination_class = StandardResultsSetPagination
    
    # 1. Register the filter backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # 2. Exact Match Filters (e.g., ?parent=2 or ?is_active=true)
    filterset_fields = ['parent', 'category_type', 'is_active', 'is_featured']
    
    # 3. Search Filters (e.g., ?search=dental)
    # The '^' prefix means "starts with". Remove it for partial "contains" matches.
    search_fields = ['name', 'slug', 'meta_title']
    
    # 4. Ordering Filters (e.g., ?ordering=-order or ?ordering=name)
    ordering_fields = ['order', 'name', 'id']
    ordering = ['order'] # Default ordering if none is provided