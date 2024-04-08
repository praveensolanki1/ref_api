from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Referral
from .serializers import ReferralSerializer
from .models import *
from . views import *



class UserRegistrationAPITestCase(APITestCase):
    def test_user_registration(self):
        # Data for user registration
        data = {
            'name': 'nikhil',
            'email': 'nikhil@example.com',
            'password': 'Nikhil123'
        }

        # Make POST request to user registration endpoint
        url = reverse('register')
        response = self.client.post(url, data)

        # Check if the response status code is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the user was created in the database
        self.assertTrue(User.objects.filter(email='nikku@example.com').exists())

        # Check if the response contains the serialized user data
        user = User.objects.get(email='nikku@example.com')
        serializer = UserRegistrationSerializer(user)
        self.assertEqual(response.data, serializer.data)

    def test_user_registration_missing_fields(self):
        # Data for user registration with missing fields
        data = {
            'name': 'nikhil',
            # Missing 'email' and 'password' fields
        }

        # Make POST request to user registration endpoint
        url = reverse('register')
        response = self.client.post(url, data)

        # Check if the response status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if the user was not created in the database
        self.assertFalse(User.objects.filter(name='nikhil').exists())

class UserTestCase(TestCase):
    def test_referral_code_generation(self):
        user = User.objects.create(name="Test User", email="test@example.com", password="Nikhil123")
        self.assertIsNotNone(user.referral_code)
        self.assertEqual(len(user.referral_code), 10)  # Ensure the referral code has the correct length





class ReferralsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.referral1 = Referral.objects.create(referrer=self.user, referee=self.user)
        self.referral2 = Referral.objects.create(referrer=self.user, referee=self.user)
        self.referral3 = Referral.objects.create(referrer=self.user, referee=self.user)

    def test_referrals_list(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Make GET request to the referrals endpoint
        url = reverse('referrals')
        response = self.client.get(url)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response contains the serialized referrals
        serializer = ReferralSerializer([self.referral1, self.referral2, self.referral3], many=True)
        self.assertEqual(response.data, serializer.data)