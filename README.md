# BazaarMate E-commerce API

A fully functional REST API for an e-commerce platform built with Django REST Framework and FastAPI.

## Features

- **Authentication & Authorization**
  - JWT-based authentication for all endpoints
  - Registration, login, logout, password reset, email verification
  - Role-based access control (Buyer, Seller, Admin)

- **Database Models**
  - User: roles (buyer, seller, admin), email, password, profile info
  - Category: name, description
  - Product: title, description, price, stock, category (FK), seller (FK), image URL
  - Cart: user (FK), items (M2M with Product), quantity
  - Order: user (FK), products, quantities, total price, status (pending, shipped, delivered, canceled), timestamps
  - Review: user (FK), product (FK), rating, comment, timestamp
  - Wishlist: user (FK), products (M2M)
  - SellerProfile: user (FK), store name, description, earnings
  - Message: sender (FK), receiver (FK), order (FK), content, timestamp

- **Endpoints**
  - Auth: `/api/auth/register/`, `/api/auth/login/`, `/api/auth/logout/`, `/api/auth/password-reset/`, `/api/auth/verify-email/`
  - Products: `/api/products/` (GET, POST, PUT, DELETE), `/api/products/<id>/` (GET, PUT, DELETE)
  - Categories: `/api/products/categories/` (GET, POST, PUT, DELETE)
  - Cart: `/api/cart/`, `/api/cart/add/`, `/api/cart/update/`, `/api/cart/remove/`
  - Orders: `/api/orders/`, `/api/orders/<id>/`
  - Reviews: `/api/reviews/products/<id>/`
  - Wishlist: `/api/wishlist/`, `/api/wishlist/add/`, `/api/wishlist/remove/`
  - Seller: `/api/seller/products/`, `/api/seller/orders/`, `/api/seller/analytics/`
  - Admin: `/api/admin/users/`, `/api/admin/sellers/`, `/api/admin/products/`, `/api/admin/orders/`
  - Messaging: `/api/messages/orders/<order_id>/`

- **Features**
  - Pagination, filtering, and sorting for list endpoints
  - Stock validation, role permissions, and input validation
  - API responses structured as `{ success: bool, data: {...}, error: str|null }`
  - Error handling and HTTP status codes implemented consistently

## Technology Stack

- **Backend**: Django 5.2, Django REST Framework, FastAPI
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: JWT via djangorestframework-simplejwt
- **Documentation**: Swagger/OpenAPI

## Setup Instructions

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Load demo data**:
   ```bash
   python manage.py loaddemo
   ```

5. **Run the Django development server**:
   ```bash
   python manage.py runserver
   ```

6. **Run the FastAPI server**:
   ```bash
   python fastapi_main.py
   ```

## API Documentation

- **Django REST Framework**: Available at `http://localhost:8000/api/docs/`
- **FastAPI**: Available at `http://localhost:8001/docs`

## Testing

Run the test suite:
```bash
python manage.py test
```

## Mock Data

The `loaddemo` command generates:
- 50 Buyers
- 10 Sellers
- 200 Products
- 10 Categories
- 20 Orders
- 50 Reviews

Images are represented as demo URLs (Unsplash/Pexels placeholders).

## Postman Collection

A Postman collection is available in the `docs` directory with Buyer, Seller, and Admin flows.