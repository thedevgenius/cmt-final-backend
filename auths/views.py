from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from accounts.models import User
from .services import send_and_store_otp, verify_otp_service
from .serializers import RequestOTPSerializer, VerifyOTPSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RequestOTPView(APIView):
    """
    API View to request an OTP for a given phone number.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RequestOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data['phone']

        if not phone:
            return Response(
                {"error": "Phone number is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Call our service function
        result = send_and_store_otp(phone)
        
        if result['success']:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyOTPView(APIView):
    """
    API View to verify an OTP and return JWT tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data['phone']
        otp = serializer.validated_data['otp']
        result = verify_otp_service(phone, otp)

        if not result["success"]:
            return Response({"detail": result["error"]}, status=result["status"])
        
        user, created = User.objects.get_or_create(
            phone=phone,
            defaults={"is_active": True}
        )

        if not user.is_active:
            user.is_active = True
            user.save()

        tokens = get_tokens_for_user(user)
        
        # 6. Return Success Response
        return Response({
            "success": True, 
            "detail": "Login successful.",
            "user_created": created,
            "tokens": tokens 
        }, status=status.HTTP_200_OK)
    
