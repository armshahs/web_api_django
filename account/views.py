from django.shortcuts import render
from django.conf import settings

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.db import transaction

from .serializers import RegisterSerializer, LoginSerializer
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

import jwt


# Create your views here.
class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    @transaction.atomic()
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        # Creating tokens for the user who just got registered
        user_email = user_data["email"]
        user = User.objects.get(email=user_email)
        token = RefreshToken.for_user(user).access_token

        # Sending email
        current_site = get_current_site(request).domain
        relativeLink = reverse("email-verify")
        absurl = "http://" + current_site + relativeLink + "?token=" + str(token)
        email_body = (
            "Hi " + user.username + ", use link below to verify your email \n" + absurl
        )
        data = {
            "email_body": email_body,
            "to_email": user_email,
            "email_subject": "Verify your email",
        }
        Util.send_email(data)

        # return response
        return Response(
            {"data": user_data, "token": str(token)}, status=status.HTTP_201_CREATED
        )


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get("token")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response(
                {"email": "Successfully verified"}, status=status.HTTP_200_OK
            )

        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {"error": "Verification Link Expired"}, status=status.HTTP_200_OK
            )

        except jwt.exceptions.DecodeError as identifier:
            return Response(
                {"error": "Invalid token. Request new token."},
                status=status.HTTP_200_OK,
            )


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
