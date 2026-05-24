from rest_framework import serializers
from .models import Business
# Import your City model (adjust path as needed)
from addresses.models import City 

# 1. Create a lightweight serializer for the City
class CityBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name', 'slug']

class BusinessListSerializer(serializers.ModelSerializer):
    distance = serializers.FloatField(read_only=True, required=False)
    
    # 2. Override the default 'city' field to use our custom serializer
    city = CityBasicSerializer(read_only=True)

    class Meta:
        model = Business
        fields = [
            'id', 'name', 'slug', 'handle', 'address', 'locality', 
            'city', # This will now output {"name": "...", "slug": "..."}
            'latitude', 'longitude', 'distance'
        ]