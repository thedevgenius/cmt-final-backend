from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Category

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