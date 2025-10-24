# JWT Authentication Implementation for Django E-commerce API

This document provides a comprehensive overview of the JWT authentication implementation for the Django E-commerce API, including setup instructions, testing procedures, and security best practices.

## Overview

The Django E-commerce API implements JWT (JSON Web Token) authentication using the `djangorestframework-simplejwt` package. This provides secure, stateless authentication for all protected endpoints.

## Key Features

1. **JWT Token Endpoints**:
   - `/api/token/` - Obtain access and refresh tokens
   - `/api/token/refresh/` - Refresh expired access tokens

2. **Role-Based Access Control**:
   - Buyers: Can view products, manage cart, place orders, write reviews
   - Sellers: Can manage their own products, view their orders
   - Admins: Full access to all endpoints

3. **Security Features**:
   - Short-lived access tokens (15 minutes)
   - Long-lived refresh tokens (1 day)
   - Token blacklisting on logout
   - Rate limiting for authentication attempts

## Implementation Details

### 1. Settings Configuration

The JWT authentication is configured in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'accounts.authentication.CustomJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # ... other settings
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'SIGNING_KEY': env('JWT_SIGNING_KEY', default=SECRET_KEY),
}
```

### 2. Custom Authentication

A custom authentication class checks for blacklisted tokens:

```python
class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Check for blacklisted tokens
        # Return user and token if valid
        # Return None if invalid or blacklisted
```

### 3. Token Management

- Access tokens expire after 15 minutes
- Refresh tokens expire after 1 day
- Tokens are blacklisted on logout
- Refresh tokens are rotated after use

## Testing JWT Authentication

### 1. Obtain JWT Tokens

#### Using cURL:
```bash
# Register a new user (optional)
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "StrongPass123!",
    "role": "buyer"
  }'

# Obtain access and refresh tokens
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "StrongPass123!"
  }'
```

Response:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Using Postman:
1. Set method to POST
2. URL: `http://localhost:8000/api/token/`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "username": "testuser",
  "password": "StrongPass123!"
}
```

### 2. Use JWT Tokens

#### Using cURL:
```bash
# Access a protected endpoint
curl -X GET http://localhost:8000/api/products/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# Create a new product (requires seller or admin role)
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Product",
    "description": "Product description",
    "price": "29.99",
    "stock": 100,
    "category": 1
  }'
```

#### Using Postman:
1. Set method and URL for the endpoint
2. In "Headers" tab, add:
   - Key: `Authorization`
   - Value: `Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...`

### 3. Refresh Expired Tokens

#### Using cURL:
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

#### Using Postman:
1. Method: POST
2. URL: `http://localhost:8000/api/token/refresh/`
3. Body (raw JSON):
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Role-Based Access Control

The API implements role-based permissions:

- **Buyers**: Can view products, manage cart, place orders, write reviews
- **Sellers**: Can manage their own products, view their orders
- **Admins**: Full access to all endpoints

Endpoints return appropriate HTTP status codes:
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions

## Security Best Practices

### 1. Token Storage
- Never store tokens in localStorage for web applications
- Use secure, httpOnly cookies when possible
- For mobile apps, use secure storage mechanisms

### 2. Token Transmission
- Always use HTTPS in production
- Include tokens in the Authorization header
- Never send tokens in URL parameters

### 3. Token Expiration
- Use short-lived access tokens (15 minutes)
- Implement refresh token rotation
- Blacklist tokens on logout

### 4. Error Handling
- Don't expose sensitive information in error messages
- Use generic error messages for authentication failures
- Log security events for monitoring

## Environment Configuration

Sensitive configuration values should be stored in environment variables:

```env
# .env file
SECRET_KEY=your-secret-key
JWT_SIGNING_KEY=your-jwt-signing-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
```

## Common Issues and Solutions

### 1. "Token is invalid or expired"
- Obtain a new token using the refresh endpoint
- If refresh token is also expired, re-authenticate

### 2. "You do not have permission to perform this action"
- Check that you have the correct role for the endpoint
- Verify your user account has the required permissions

### 3. "Authentication credentials were not provided"
- Ensure the Authorization header is correctly formatted
- Check that the token is included in the header

## Testing with Different Tools

### cURL Examples

```bash
# Get products (public endpoint)
curl -X GET http://localhost:8000/api/products/

# Get products (authenticated)
curl -X GET http://localhost:8000/api/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Create a product (seller/admin only)
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Product", "price": "19.99", "stock": 10}'
```

### Python Requests Examples

```python
import requests

# Get products
response = requests.get('http://localhost:8000/api/products/')
print(response.json())

# Get products with authentication
headers = {'Authorization': 'Bearer YOUR_ACCESS_TOKEN'}
response = requests.get('http://localhost:8000/api/products/', headers=headers)
print(response.json())

# Create a product
data = {'title': 'Test Product', 'price': '19.99', 'stock': 10}
response = requests.post('http://localhost:8000/api/products/', 
                        headers=headers, json=data)
print(response.json())
```

## Conclusion

The JWT authentication implementation provides a secure, scalable solution for protecting the Django E-commerce API. By following the guidelines in this document, developers can easily test and integrate with the API using JWT tokens.

For production deployments, ensure that:
1. HTTPS is enforced
2. Tokens are properly secured
3. Rate limiting is configured
4. Logging is implemented for security monitoring
5. Regular security audits are performed