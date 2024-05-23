from rest_framework.test import APITestCase
from django.urls import reverse

from account.models import User


class TestSetUp(APITestCase):

    def setUp(self):

        self.register_url = reverse("register")
        self.login_url = reverse("login")

        self.user_data = {
            "email": "email@gmail.com",
            "username": "email",
            "password": "email@gmail.com",  # can keep anything
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
