from .models import User
from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
        )

    # validation checks provided in the serializer. Basically does the checking like django forms.
    # this validation is done before the create function being called.
    def validate(self, attrs):
        email = attrs.get("email", "")
        username = attrs.get("username", "")

        if not username.isalnum():
            raise serializers.ValidationError(
                "Username should only contain alphanumeric characters"
            )

        return attrs

    # this will take the data (including validated username) and create the model instance.
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=20, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)

    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "username",
            "tokens",
        )

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        print(email)
        print(password)

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")
        if user.is_active == False:
            raise AuthenticationFailed("Account inactive. Contact admin")

        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        return {"email": user.email, "username": user.username, "tokens": user.tokens}

        return super().validate(attrs)
