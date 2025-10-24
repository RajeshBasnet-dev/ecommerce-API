from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import Django models and settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bazaarmate.settings')

import django
django.setup()

from accounts.models import User
from products.models import Category, Product
from orders.models import Order
from reviews.models import Review

app = FastAPI(
    title="BazaarMate FastAPI",
    description="FastAPI endpoints for BazaarMate e-commerce platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic models
class UserBase(BaseModel):
    username: str
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

class ProductBase(BaseModel):
    title: str
    description: str
    price: float
    stock: int
    category_id: int
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    category_name: str
    seller_name: str

# Authentication dependency
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # In a real implementation, you would verify the token
    # For now, we'll just return a mock user
    return UserResponse(id=1, username="testuser", email="test@example.com", role="buyer")

# Auth endpoints
@app.post("/auth/register/", response_model=UserResponse)
async def register_user(user: UserCreate):
    # In a real implementation, you would create the user in the database
    return UserResponse(id=1, username=user.username, email=user.email, role="buyer")

@app.post("/auth/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # In a real implementation, you would verify credentials and return a token
    return {"access_token": "mock_token", "token_type": "bearer"}

# Category endpoints
@app.get("/categories/", response_model=List[CategoryResponse])
async def list_categories(skip: int = 0, limit: int = 100):
    # In a real implementation, you would query the database
    categories = [
        CategoryResponse(id=1, name="Electronics", description="Electronic devices"),
        CategoryResponse(id=2, name="Clothing", description="Apparel and accessories"),
    ]
    return categories

@app.post("/categories/", response_model=CategoryResponse)
async def create_category(category: CategoryCreate, current_user: UserResponse = Depends(get_current_user)):
    # In a real implementation, you would save to the database
    return CategoryResponse(id=3, name=category.name, description=category.description)

# Product endpoints
@app.get("/products/", response_model=List[ProductResponse])
async def list_products(skip: int = 0, limit: int = 100, category_id: Optional[int] = None):
    # In a real implementation, you would query the database
    products = [
        ProductResponse(
            id=1,
            title="Smartphone",
            description="Latest model smartphone",
            price=699.99,
            stock=50,
            category_id=1,
            category_name="Electronics",
            seller_name="Tech Store",
            image_url="https://example.com/smartphone.jpg"
        ),
    ]
    return products

@app.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate, current_user: UserResponse = Depends(get_current_user)):
    # In a real implementation, you would save to the database
    category = CategoryResponse(id=product.category_id, name="Electronics", description="Electronic devices")
    return ProductResponse(
        id=2,
        title=product.title,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category_id=product.category_id,
        category_name=category.name,
        seller_name="Tech Store",
        image_url=product.image_url
    )

# Run the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)