# BazaarMate API Examples

This document provides examples for using the BazaarMate e-commerce API.

## Authentication

### User Registration

```bash
POST /api/auth/register/

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "buyer"
}
```

Response:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "buyer",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": null,
    "date_of_birth": null
  },
  "error": null
}
```

### User Login

```bash
POST /api/auth/login/

{
  "username": "john_doe",
  "password": "securepassword123"
}
```

Response:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Get User Profile

```bash
GET /api/auth/profile/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

Response:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "buyer",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": null,
    "date_of_birth": null
  },
  "error": null
}
```

## Products

### List Products

```bash
GET /api/products/?page=1&page_size=10&ordering=-created_at
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

Response:
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": 1,
        "title": "Smartphone XYZ",
        "description": "Latest model smartphone with advanced features",
        "price": "699.99",
        "stock": 50,
        "category": 1,
        "seller": 2,
        "image_url": "https://example.com/smartphone.jpg",
        "is_active": true,
        "created_at": "2023-01-15T10:30:00Z",
        "updated_at": "2023-01-15T10:30:00Z",
        "category_name": "Electronics",
        "seller_name": "TechStore"
      }
    ],
    "pagination": {
      "count": 1,
      "num_pages": 1,
      "current_page": 1,
      "next": null,
      "previous": null
    }
  },
  "error": null
}
```

### Create Product (Seller/Admin only)

```bash
POST /api/products/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "title": "Laptop ABC",
  "description": "High-performance laptop for professionals",
  "price": "1299.99",
  "stock": 25,
  "category": 1,
  "image_url": "https://example.com/laptop.jpg",
  "is_active": true
}
```

Response:
```json
{
  "success": true,
  "data": {
    "id": 2,
    "title": "Laptop ABC",
    "description": "High-performance laptop for professionals",
    "price": "1299.99",
    "stock": 25,
    "category": 1,
    "seller": 2,
    "image_url": "https://example.com/laptop.jpg",
    "is_active": true,
    "created_at": "2023-01-15T11:00:00Z",
    "updated_at": "2023-01-15T11:00:00Z",
    "category_name": "Electronics",
    "seller_name": "TechStore"
  },
  "error": null
}
```

### Filter Products

```bash
GET /api/products/?min_price=500&max_price=1500&category=electronics&in_stock=true
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## Categories

### List Categories

```bash
GET /api/products/categories/?ordering=name
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

Response:
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": 1,
        "name": "Electronics",
        "description": "Electronic devices and gadgets",
        "created_at": "2023-01-10T09:00:00Z",
        "updated_at": "2023-01-10T09:00:00Z",
        "products_count": 15
      }
    ],
    "pagination": {
      "count": 1,
      "num_pages": 1,
      "current_page": 1,
      "next": null,
      "previous": null
    }
  },
  "error": null
}
```

## Cart

### View Cart

```bash
GET /api/cart/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

Response:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user": 1,
    "created_at": "2023-01-15T10:00:00Z",
    "updated_at": "2023-01-15T10:30:00Z",
    "items": [
      {
        "id": 1,
        "cart": 1,
        "product": {
          "id": 1,
          "title": "Smartphone XYZ",
          "description": "Latest model smartphone with advanced features",
          "price": "699.99",
          "stock": 50,
          "category": 1,
          "seller": 2,
          "image_url": "https://example.com/smartphone.jpg",
          "is_active": true,
          "created_at": "2023-01-15T10:30:00Z",
          "updated_at": "2023-01-15T10:30:00Z",
          "category_name": "Electronics",
          "seller_name": "TechStore"
        },
        "quantity": 1,
        "added_at": "2023-01-15T10:30:00Z",
        "total_price": "699.99"
      }
    ],
    "total_items": 1,
    "total_price": "699.99"
  },
  "error": null
}
```

### Add Item to Cart

```bash
POST /api/cart/add/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2
}
```

## Orders

### List Orders

```bash
GET /api/orders/?ordering=-created_at
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

Response:
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": 1,
        "user": 1,
        "total_price": "699.99",
        "status": "delivered",
        "created_at": "2023-01-15T11:00:00Z",
        "updated_at": "2023-01-16T14:00:00Z",
        "shipped_at": "2023-01-15T15:00:00Z",
        "delivered_at": "2023-01-16T14:00:00Z",
        "user_email": "john@example.com",
        "items": [
          {
            "id": 1,
            "order": 1,
            "product": {
              "id": 1,
              "title": "Smartphone XYZ",
              "description": "Latest model smartphone with advanced features",
              "price": "699.99",
              "stock": 50,
              "category": 1,
              "seller": 2,
              "image_url": "https://example.com/smartphone.jpg",
              "is_active": true,
              "created_at": "2023-01-15T10:30:00Z",
              "updated_at": "2023-01-15T10:30:00Z",
              "category_name": "Electronics",
              "seller_name": "TechStore"
            },
            "quantity": 1,
            "price": "699.99"
          }
        ]
      }
    ],
    "pagination": {
      "count": 1,
      "num_pages": 1,
      "current_page": 1,
      "next": null,
      "previous": null
    }
  },
  "error": null
}
```

## Reviews

### List Product Reviews

```bash
GET /api/reviews/products/1/?ordering=-created_at
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

Response:
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": 1,
        "user": 1,
        "product": 1,
        "rating": 5,
        "comment": "Excellent product! Highly recommended.",
        "created_at": "2023-01-16T10:00:00Z",
        "updated_at": "2023-01-16T10:00:00Z",
        "user_name": "john_doe",
        "product_title": "Smartphone XYZ"
      }
    ],
    "pagination": {
      "count": 1,
      "num_pages": 1,
      "current_page": 1,
      "next": null,
      "previous": null
    }
  },
  "error": null
}
```

## Messaging

### List Order Messages

```bash
GET /api/messages/orders/1/?ordering=created_at
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

Response:
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": 1,
        "sender": 1,
        "receiver": 2,
        "order": 1,
        "content": "When will my order be shipped?",
        "is_read": false,
        "created_at": "2023-01-15T12:00:00Z",
        "updated_at": "2023-01-15T12:00:00Z",
        "sender_name": "john_doe",
        "receiver_name": "techstore"
      }
    ],
    "pagination": {
      "count": 1,
      "num_pages": 1,
      "current_page": 1,
      "next": null,
      "previous": null
    }
  },
  "error": null
}
```

## Search

### Global Search

```bash
GET /api/search/?q=smartphone
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

Response:
```json
{
  "success": true,
  "data": {
    "products": [
      {
        "id": 1,
        "title": "Smartphone XYZ",
        "description": "Latest model smartphone with advanced features",
        "price": "699.99",
        "stock": 50,
        "category": 1,
        "seller": 2,
        "image_url": "https://example.com/smartphone.jpg",
        "is_active": true,
        "created_at": "2023-01-15T10:30:00Z",
        "updated_at": "2023-01-15T10:30:00Z",
        "category_name": "Electronics",
        "seller_name": "TechStore"
      }
    ],
    "categories": [],
    "total_products": 1,
    "total_categories": 0
  },
  "error": null
}
```