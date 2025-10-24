# BazaarMate E-commerce API

A fully functional REST API for an e-commerce platform built with Django REST Framework. This API supports buyer, seller, and admin roles with comprehensive e-commerce functionality.

## Features

- **Authentication & Authorization**
  - JWT-based authentication for all endpoints
  - Registration, login, profile management
  - Role-based access control (Buyer, Seller, Admin)

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

## Technology Stack

- **Backend**: Django 5.2, Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: JWT via djangorestframework-simplejwt
- **API Documentation**: Swagger/OpenAPI via drf-yasg
- **Filtering**: django-filter

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
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
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

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the API documentation**:
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
   POST /api/auth/login/
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