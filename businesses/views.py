from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from .models import Business
from .serializers import BusinessListSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50

class BusinessListAPIView(APIView):
    """
    Core listing endpoint for Businesses.
    Accepts custom query parameters and manually handles pagination.
    """
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        # 1. Extract Query Parameters
        category_slug = request.query_params.get('category')
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius_km = float(request.query_params.get('radius', 10.0)) # Default 10km radius

        # 2. Base Queryset (Only active and verified businesses)
        queryset = Business.objects.select_related('city').filter(is_active=True)

        # 3. Filter by Category (Checks both primary and ManyToMany categories)
        if category_slug:
            queryset = queryset.filter(
                Q(primary_category__slug=category_slug) | 
                Q(categories__slug=category_slug)
            ).distinct() # Distinct is crucial when filtering on ManyToMany fields to avoid duplicate rows

        # 4. Filter by Location (Bounding Box Approach)
        # 1 degree of latitude is ~111 km. This creates a quick square boundary.
        # It is highly efficient because it utilizes the database indexes directly.
        if lat and lng:
            try:
                lat = float(lat)
                lng = float(lng)
                
                lat_delta = radius_km / 111.0
                # Longitude distance changes based on latitude, so we adjust it using the Cosine of the latitude
                import math
                lng_delta = radius_km / (111.0 * math.cos(math.radians(lat)))

                lat_min, lat_max = lat - lat_delta, lat + lat_delta
                lng_min, lng_max = lng - lng_delta, lng + lng_delta

                # Filter businesses within this geographic square
                queryset = queryset.filter(
                    latitude__range=(lat_min, lat_max),
                    longitude__range=(lng_min, lng_max)
                )
                
                # TODO (Future Customization): Add Haversine formula annotation here 
                # to calculate exact distance and order by proximity.
                
            except ValueError:
                return Response(
                    {"error": "Invalid latitude or longitude provided."}, 
                    status=400
                )

        # 5. Default Ordering
        # Ensure consistent ordering for pagination, otherwise items might duplicate across pages
        queryset = queryset.order_by('-created_at')

        # 6. Manual Pagination Execution
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request, view=self)
        
        # 7. Serialization
        serializer = BusinessListSerializer(paginated_queryset, many=True)
        
        # 8. Return standard paginated response
        return paginator.get_paginated_response(serializer.data)