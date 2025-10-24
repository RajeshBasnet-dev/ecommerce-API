from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class JWTAuthenticationTestCase(APITestCase):
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

    def test_obtain_jwt_token(self):
        """Test obtaining JWT token"""
        data = {
            'username': 'buyer',
            'password': 'TestPass123!'
        }
        response = self.client.post('/api/token/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_access_protected_endpoint_with_valid_token(self):
        """Test accessing protected endpoint with valid token"""
        # Get token
        data = {
            'username': 'buyer',
            'password': 'TestPass123!'
        }
        token_response = self.client.post('/api/token/', data, format='json')
        access_token = token_response.data['access']
        
        # Access protected endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/api/products/')
        # Should be able to access (even if no products exist)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_protected_endpoint_without_token(self):
        """Test accessing protected endpoint without token"""
        response = self.client.get('/api/products/')
        # Should return 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_endpoint_with_invalid_token(self):
        """Test accessing protected endpoint with invalid token"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid.token.here')
        response = self.client.get('/api/products/')
        # Should return 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_jwt_token(self):
        """Test refreshing JWT token"""
        # Get initial token
        data = {
            'username': 'buyer',
            'password': 'TestPass123!'
        }
        token_response = self.client.post('/api/token/', data, format='json')
        refresh_token = token_response.data['refresh']
        
        # Refresh token
        refresh_data = {
            'refresh': refresh_token
        }
        response = self.client.post('/api/token/refresh/', refresh_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)