from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import BlacklistedToken

User = get_user_model()

class SimpleTestCase(TestCase):
    def test_user_creation(self):
        """Test that we can create a user"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!',
            role='buyer'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, 'buyer')
        self.assertTrue(user.check_password('TestPass123!'))

    def test_blacklisted_token_model(self):
        """Test that we can create a BlacklistedToken"""
        user = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='TestPass123!',
            role='buyer'
        )
        
        # This should not raise an exception
        token = BlacklistedToken(
            jti='test-jti',
            user=user,
            expires_at='2025-01-01T00:00:00Z'
        )
        token.save()
        
        # Verify it was saved
        self.assertEqual(BlacklistedToken.objects.count(), 1)
        self.assertEqual(BlacklistedToken.objects.first().jti, 'test-jti')