from .models import User
from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

# Adding the below to reset the password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


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

    # SerializerMethodField allows us to pass a method instead of the typical Charfield
    # You can then define a function called get_tokens in the serializer. Also empty bracket of SerializerMethodField
    # assumes that you are passing the get_tokens function.
    # Now the output will be a dictionary instead of text "'refresh': '3213ddada213', 'access': 'adsad' "
    # very difficult on the frontend to extract the refresh and access from above.
    # It can be a nested dict but it should be of the format "refresh": "3213ddada213", "access": "adsad"
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj["email"])
        return {
            "refresh": user.tokens()["refresh"],
            "access": user.tokens()["access"],
        }

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


class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ["email"]


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)

            user.set_password(password)
            user.save()

            return user

        except Exception as e:
            raise AuthenticationFailed("The reset link is invalid", 401)
        return super().validate(attrs)
