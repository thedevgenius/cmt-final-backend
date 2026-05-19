from rest_framework import serializers

class RequestOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, min_length=12)

class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, min_length=10)
    otp = serializers.CharField(min_length=4, max_length=6)