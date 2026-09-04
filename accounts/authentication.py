from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        email = attrs.get("email").strip().lower()
        password = attrs.get("password")

        # Find user using email
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "detail": "Invalid Email or Password"
            })

        # Check password
        if not user.check_password(password):
            raise serializers.ValidationError({
                "detail": "Invalid Email or Password"
            })

        # Check account status
        if not user.is_active:
            raise serializers.ValidationError({
                "detail": "This account is inactive."
            })

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),

            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
            }
        }