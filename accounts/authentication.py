from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        email = attrs.get("email")

        password = attrs.get("password")

        user = authenticate(
            username=email,
            password=password
        )

        if not user:

            raise serializers.ValidationError(
                "Invalid Email or Password"
            )

        refresh = RefreshToken.for_user(user)

        return {

            "refresh": str(refresh),

            "access": str(refresh.access_token),

            "user": {

                "id": user.id,

                "username": user.username,

                "email": user.email,

                "phone": user.phone

            }

        }