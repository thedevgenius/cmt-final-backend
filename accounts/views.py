# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import UserProfileUpdateSerializer, UserProfileSerializer

class UserProfileUpdateView(APIView):
    """
    Endpoint for the authenticated user to update their own profile details.
    """
    # Enforce that a valid JWT token must be provided
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """
        Handles partial updates (PATCH). 
        Users can pass only the fields they want to change.
        """
        # Pass the authenticated user instance and incoming data to the serializer
        serializer = UserProfileUpdateSerializer(
            instance=request.user, 
            data=request.data, 
            partial=True,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Profile updated successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """
        Handles full updates (PUT). 
        Requires all fields to be passed in the payload.
        """
        serializer = UserProfileUpdateSerializer(
            instance=request.user, 
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Profile updated successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileView(APIView):
    """
    Endpoint to retrieve the profile details of the currently authenticated user.
    """
    # Enforce that a valid JWT token must be provided
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # request.user automatically holds the user instance attached to the provided JWT token
        serializer = UserProfileSerializer(request.user)
        
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)