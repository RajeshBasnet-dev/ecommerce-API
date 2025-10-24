# BazaarMate E-commerce API

A fully functional REST API for an e-commerce platform built with Django REST Framework. This API supports buyer, seller, and admin roles with comprehensive e-commerce functionality.

## Features

- **Authentication & Authorization**
  - JWT-based authentication for all endpoints
  - Registration, login, profile management
  - Role-based access control (Buyer, Seller, Admin)
  - Multi-factor authentication support

- **Product Management**
  - Product catalog with categories
  - Advanced search, filtering, and sorting
  - Stock management

- **Shopping Cart**
  - Add/remove items
  - Update quantities
  - Calculate totals

- **Order Management**
  - Order creation and tracking
  - Status updates (pending, processing, shipped, delivered, cancelled)

- **Review System**
  - Product ratings and reviews
  - User feedback management

- **Messaging**
  - Communication between buyers and sellers
  - Order-related messaging

- **Advanced Features**
  - Pagination for all list endpoints
  - Input validation and error handling
  - Comprehensive API documentation
  - Global search functionality
  - **Enhanced Security Features** (See [Security Enhancements](SECURITY_ENHANCEMENTS.md))

## Technology Stack

- **Backend**: Django 5.2, Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: JWT via djangorestframework-simplejwt
- **API Documentation**: Swagger/OpenAPI via drf-yasg
- **Filtering**: django-filter
- **Security**: django-csp, django-environ, cryptography

## Project Structure

```
bazaar_mate/
├── apps/
│   ├── users/          # User authentication and profiles
│   ├── products/       # Product catalog and categories
│   ├── cart/           # Shopping cart functionality
│   ├── orders/         # Order management
│   ├── reviews/        # Product reviews and ratings
│   └── messaging/      # Messaging system
├── api/                # Global API components
├── bazaar_mate/        # Project settings and configuration
├── static/             # Static files
├── media/              # Media files
├── tests/              # Unit and integration tests
├── requirements.txt    # Project dependencies
└── manage.py           # Django management script
```

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout (revoke token)
- `POST /api/auth/refresh/` - Refresh access token
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile

### Products
- `GET /api/products/` - List products (with filtering and pagination)
- `POST /api/products/` - Create product (seller/admin only)
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product (seller/admin only)
- `DELETE /api/products/{id}/` - Delete product (seller/admin only)

### Categories
- `GET /api/products/categories/` - List categories
- `POST /api/products/categories/` - Create category (admin only)
- `GET /api/products/categories/{id}/` - Get category details
- `PUT /api/products/categories/{id}/` - Update category (admin only)
- `DELETE /api/products/categories/{id}/` - Delete category (admin only)

### Cart
- `GET /api/cart/` - View cart
- `POST /api/cart/add/` - Add item to cart
- `PUT /api/cart/update/{id}/` - Update cart item
- `DELETE /api/cart/remove/{id}/` - Remove item from cart

### Orders
- `GET /api/orders/` - List orders
- `POST /api/orders/` - Create order
- `GET /api/orders/{id}/` - Get order details
- `PUT /api/orders/{id}/` - Update order status

### Reviews
- `GET /api/reviews/products/{product_id}/` - List product reviews
- `POST /api/reviews/products/{product_id}/` - Create review
- `GET /api/reviews/{id}/` - Get review details
- `PUT /api/reviews/{id}/` - Update review
- `DELETE /api/reviews/{id}/` - Delete review

### Messaging
- `GET /api/messages/orders/{order_id}/` - List order messages
- `POST /api/messages/orders/{order_id}/` - Send message
- `GET /api/messages/{id}/` - Get message details
- `PUT /api/messages/{id}/` - Update message
- `DELETE /api/messages/{id}/` - Delete message

### Search
- `GET /api/search/?q={query}` - Global search across products and categories

## Security Enhancements

This API includes comprehensive security enhancements to protect sensitive data and prevent common vulnerabilities:

### Authentication Security
- Strong JWT implementation with short-lived access tokens (15 minutes)
- Rotating refresh tokens with blacklist support
- Token revocation on logout or password change
- Rate limiting for authentication endpoints (5 attempts/minute)

### Password Security
- Minimum 12-character password requirements
- Mandatory uppercase, lowercase, digit, and special character
- Prevention of common password patterns
- PBKDF2 secure password hashing

### Data Security
- Field-level encryption for sensitive data (phone numbers, messages)
- Environment-based secret management
- HTTPS enforcement in production

### API Security
- Content Security Policy (CSP) implementation
- HTTP Strict Transport Security (HSTS)
- XSS and content type sniffing protection
- Proper CORS configuration

### Safe Git Practices
- Comprehensive .gitignore to prevent sensitive file commits
- Environment variable management with .env.example template

For detailed information about all security enhancements, see [SECURITY_ENHANCEMENTS.md](SECURITY_ENHANCEMENTS.md).

## Testing the API with JWT Authentication

### 1. Obtain JWT Tokens

To access protected endpoints, you first need to obtain a JWT token:

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

This will return:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Using Postman:
1. Set the request method to POST
2. Set the URL to `http://localhost:8000/api/token/`
3. In the "Body" tab, select "raw" and "JSON"
4. Enter the credentials:
```json
{
  "username": "testuser",
  "password": "StrongPass123!"
}
```
5. Click "Send"

### 2. Use JWT Tokens to Access Protected Endpoints

Once you have the access token, include it in the Authorization header for all protected requests:

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
1. Set the request method and URL for the endpoint you want to test
2. In the "Headers" tab, add a new header:
   - Key: `Authorization`
   - Value: `Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...` (your access token)
3. Click "Send"

### 3. Refresh Expired Tokens

Access tokens expire after 15 minutes. To get a new access token:

#### Using cURL:
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

#### Using Postman:
1. Set the request method to POST
2. Set the URL to `http://localhost:8000/api/token/refresh/`
3. In the "Body" tab, select "raw" and "JSON"
4. Enter the refresh token:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
5. Click "Send"

### 4. Role-Based Access Control

The API implements role-based access control:
- **Buyers**: Can view products, manage cart, place orders, write reviews
- **Sellers**: Can manage their own products, view their orders
- **Admins**: Full access to all endpoints

Some endpoints will return 403 Forbidden if you don't have the required role.

### 5. Error Handling

The API returns appropriate HTTP status codes:
- `200 OK`: Successful GET, PUT requests
- `201 Created`: Successful POST requests
- `204 No Content`: Successful DELETE requests
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/RajeshBasnet-dev/ecommerce-API.git
   cd ecommerce-API
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a .env file**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the API documentation**:
   - Swagger UI: http://localhost:8000/swagger/
   - ReDoc: http://localhost:8000/redoc/

## Filtering and Sorting

The API supports advanced filtering and sorting for list endpoints:

### Product Filtering
- `?min_price=10` - Products with price >= 10
- `?max_price=100` - Products with price <= 100
- `?category=electronics` - Products in electronics category
- `?seller=john` - Products from seller john
- `?in_stock=true` - Products that are in stock
- `?title=phone` - Products with "phone" in title
- `?description=smart` - Products with "smart" in description
- `?is_active=true` - Active products only

### Sorting
- `?ordering=price` - Sort by price (ascending)
- `?ordering=-price` - Sort by price (descending)
- `?ordering=title` - Sort by title (ascending)
- `?ordering=-created_at` - Sort by creation date (descending)

### Pagination
- `?page=2` - Get page 2
- `?page_size=50` - Get 50 items per page (max 100)

## Search Functionality

Use the global search endpoint to search across products and categories:
```
GET /api/search/?q=search_term
```

## Authentication

Most endpoints require authentication. To authenticate:

1. Register a new user or use existing credentials
2. Obtain a JWT token:
   ```bash
   POST /api/token/
   {
     "username": "your_username",
     "password": "your_password"
   }
   ```
3. Include the token in the Authorization header:
   ```
   Authorization: Bearer your_access_token_here
   ```

## Role-Based Access Control

- **Buyers**: Can view products, manage cart, place orders, write reviews
- **Sellers**: Can manage their own products, view their orders
- **Admins**: Full access to all endpoints

## Testing

Run the test suite:
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.