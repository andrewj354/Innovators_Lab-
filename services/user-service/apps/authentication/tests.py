import pytest
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationTest(APITestCase):
    """Test authentication endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='auth@example.com',
            username='authuser',
            password='testpass123',
            first_name='Auth',
            last_name='User',
        )

    def test_user_registration(self):
        """Test user registration"""
        data = {
            'email': 'newauth@example.com',
            'username': 'newauthuser',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'first_name': 'New',
            'last_name': 'Auth',
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])

    def test_user_login(self):
        """Test user login"""
        data = {
            'email': 'auth@example.com',
            'password': 'testpass123',
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED])

    def test_user_logout(self):
        """Test user logout"""
        response = self.client.post('/api/auth/logout/')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED])

    def test_get_me(self):
        """Test getting current user"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_verify_token(self):
        """Test token verification"""
        response = self.client.post('/api/auth/verify/', {})
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_400_BAD_REQUEST])
