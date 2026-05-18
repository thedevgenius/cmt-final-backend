# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Specify the fields the user is allowed to update
        fields = ['full_name', 'email'] 
        extra_kwargs = {
            'full_name': {'required': False},
            'email': {'required': False},
        }

    def validate_email(self, value):
        """Ensure the email is unique if it's being updated."""
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use by another account.")
        return value