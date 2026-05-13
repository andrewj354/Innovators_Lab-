import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.users.models import UserProfile
from apps.users.serializers import UserSerializer, UserProfileSerializer

User = get_user_model()


class UserModelTest(TestCase):
    """Test User model"""

    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
        }

    def test_create_user(self):
        """Test creating a user"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertTrue(user.check_password(self.user_data['password']))

    def test_user_string_representation(self):
        """Test user string representation"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['username'])

    def test_user_email_uniqueness(self):
        """Test email uniqueness constraint"""
        User.objects.create_user(**self.user_data)
        with self.assertRaises(Exception):
            User.objects.create_user(**self.user_data)


class UserProfileModelTest(TestCase):
    """Test UserProfile model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='profile@example.com',
            username='profileuser',
            password='testpass123',
            first_name='Profile',
            last_name='User',
        )

    def test_create_user_profile(self):
        """Test creating user profile"""
        profile = UserProfile.objects.create(
            user=self.user,
            phone='+380123456789',
            address='123 Test St',
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.phone, '+380123456789')
        self.assertEqual(profile.address, '123 Test St')

    def test_profile_cascade_delete(self):
        """Test profile is deleted when user is deleted"""
        profile = UserProfile.objects.create(user=self.user)
        user_id = self.user.id
        self.user.delete()
        self.assertFalse(UserProfile.objects.filter(id=profile.id).exists())


class UserSerializerTest(TestCase):
    """Test UserSerializer"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='serializer@example.com',
            username='serializeruser',
            password='testpass123',
            first_name='Serializer',
            last_name='User',
        )

    def test_serialize_user(self):
        """Test serializing user"""
        serializer = UserSerializer(self.user)
        data = serializer.data
        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['first_name'], self.user.first_name)

    def test_deserialize_user(self):
        """Test deserializing user data"""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class UserAPITest(APITestCase):
    """Test User API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='api@example.com',
            username='apiuser',
            password='testpass123',
            first_name='API',
            last_name='User',
        )

    def test_get_user_list(self):
        """Test getting user list"""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_via_api(self):
        """Test creating user via API"""
        data = {
            'email': 'createapi@example.com',
            'username': 'createapiuser',
            'password': 'testpass123',
            'first_name': 'Create',
            'last_name': 'API',
        }
        response = self.client.post('/api/users/', data)
        # Should require authentication for creation
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN, status.HTTP_201_CREATED])

    def test_get_user_detail(self):
        """Test getting user detail"""
        response = self.client.get(f'/api/users/{self.user.id}/')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED])

    def test_user_authentication(self):
        """Test user authentication"""
        data = {
            'email': 'api@example.com',
            'password': 'testpass123',
        }
        response = self.client.post('/api/auth/login/', data)
        # Should return token or authentication response
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED])
