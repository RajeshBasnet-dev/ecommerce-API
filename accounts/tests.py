from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import BlacklistedToken

User = get_user_model()

class AuthenticationTestCase(APITestCase):
    def setUp(self):
        # Create test users
        self.buyer_user = User.objects.create_user(
            username='buyer',
            email='buyer@test.com',
            password='TestPass123!',
            role='buyer'
        )
        self.seller_user = User.objects.create_user(
            username='seller',
            email='seller@test.com',
            password='TestPass123!',
            role='seller'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='TestPass123!',
            role='admin'
        )

    def test_user_registration(self):
        """Test user registration endpoint"""
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'StrongPass123!',
            'role': 'buyer'
        }
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('data' in response.data)
        self.assertEqual(response.data['data']['username'], 'newuser')
        self.assertEqual(response.data['data']['role'], 'buyer')

    def test_user_registration_with_weak_password(self):
        """Test user registration with weak password fails"""
        data = {
            'username': 'newuser2',
            'email': 'newuser2@test.com',
            'password': 'weak',
            'role': 'buyer'
        }
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        """Test user login endpoint"""
        data = {
            'email': 'buyer@test.com',
            'password': 'TestPass123!'
        }
        response = self.client.post('/api/auth/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_user_login_with_invalid_credentials(self):
        """Test user login with invalid credentials fails"""
        data = {
            'email': 'buyer@test.com',
            'password': 'WrongPassword'
        }
        response = self.client.post('/api/auth/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_logout(self):
        """Test user logout endpoint"""
        # First login to get tokens
        login_data = {
            'email': 'buyer@test.com',
            'password': 'TestPass123!'
        }
        login_response = self.client.post('/api/auth/login/', login_data, format='json')
        refresh_token = login_response.data['refresh']
        
        # Now logout
        logout_data = {
            'refresh': refresh_token
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {login_response.data["access"]}')
        response = self.client.post('/api/auth/logout/', logout_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Successfully logged out')
        
        # Verify token is blacklisted
        token = RefreshToken(refresh_token)
        self.assertTrue(BlacklistedToken.objects.filter(jti=token['jti']).exists())

    def test_access_profile_authenticated(self):
        """Test accessing profile with valid authentication"""
        # Login first
        login_data = {
            'email': 'buyer@test.com',
            'password': 'TestPass123!'
        }
        login_response = self.client.post('/api/auth/login/', login_data, format='json')
        
        # Access profile
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {login_response.data["access"]}')
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['username'], 'buyer')

    def test_access_profile_unauthenticated(self):
        """Test accessing profile without authentication fails"""
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile(self):
        """Test updating user profile"""
        # Login first
        login_data = {
            'email': 'buyer@test.com',
            'password': 'TestPass123!'
        }
        login_response = self.client.post('/api/auth/login/', login_data, format='json')
        
        # Update profile
        update_data = {
            'first_name': 'John',
            'last_name': 'Doe'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {login_response.data["access"]}')
        response = self.client.patch('/api/auth/profile/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['first_name'], 'John')
        self.assertEqual(response.data['data']['last_name'], 'Doe')

class PasswordValidationTestCase(TestCase):
    def test_strong_password_validation(self):
        """Test that strong passwords pass validation"""
        from django.contrib.auth.password_validation import validate_password
        from django.core.exceptions import ValidationError
        
        strong_password = 'Str0ngP@ssw0rd!'  # Better strong password
        try:
            validate_password(strong_password)
            self.assertTrue(True)  # Password is valid
        except ValidationError:
            self.fail("Strong password validation failed")

    def test_weak_password_validation(self):
        """Test that weak passwords fail validation"""
        from django.contrib.auth.password_validation import validate_password
        from django.core.exceptions import ValidationError
        
        weak_password = '123'
        with self.assertRaises(ValidationError):
            validate_password(weak_password)

class RoleBasedPermissionTestCase(APITestCase):
    def setUp(self):
        # Create test users
        self.buyer_user = User.objects.create_user(
            username='buyer',
            email='buyer@test.com',
            password='TestPass123!',
            role='buyer'
        )
        self.seller_user = User.objects.create_user(
            username='seller',
            email='seller@test.com',
            password='TestPass123!',
            role='seller'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='TestPass123!',
            role='admin'
        )

    def test_buyer_role(self):
        """Test that user has buyer role"""
        self.assertEqual(self.buyer_user.role, 'buyer')

    def test_seller_role(self):
        """Test that user has seller role"""
        self.assertEqual(self.seller_user.role, 'seller')

    def test_admin_role(self):
        """Test that user has admin role"""
        self.assertEqual(self.admin_user.role, 'admin')