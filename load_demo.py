import os
import sys
import random
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bazaarmate.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import User
from sellers.models import SellerProfile
from products.models import Category, Product
from orders.models import Order, OrderItem
from reviews.models import Review
from cart.models import Cart, CartItem
from wishlist.models import Wishlist

def load_demo_data():
    print("Loading demo data for BazaarMate...")
    
    # Clear existing data
    print("Clearing existing data...")
    Review.objects.all().delete()
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    CartItem.objects.all().delete()
    Cart.objects.all().delete()
    Wishlist.objects.all().delete()
    Product.objects.all().delete()
    Category.objects.all().delete()
    SellerProfile.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()

    # Create admin user
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@bazaarmate.com',
        password='admin123',
        role='admin'
    )
    print(f'Created admin user: {admin_user.email}')

    # Create buyer users
    buyers = []
    for i in range(50):
        buyer = User.objects.create_user(
            username=f'buyer{i+1}',
            email=f'buyer{i+1}@example.com',
            password='password123',
            role='buyer',
            first_name=f'Buyer{i+1}',
            last_name='Test'
        )
        buyers.append(buyer)
        
        # Create cart for each buyer
        Cart.objects.create(user=buyer)
        
        # Create wishlist for each buyer
        Wishlist.objects.create(user=buyer)
        
    print(f'Created {len(buyers)} buyers')

    # Create seller users and profiles
    sellers = []
    for i in range(10):
        seller_user = User.objects.create_user(
            username=f'seller{i+1}',
            email=f'seller{i+1}@example.com',
            password='password123',
            role='seller',
            first_name=f'Seller{i+1}',
            last_name='Test'
        )
        
        seller_profile = SellerProfile.objects.create(
            user=seller_user,
            store_name=f'Store {i+1}',
            description=f'This is the amazing store {i+1}',
            is_verified=True
        )
        sellers.append(seller_profile)
    print(f'Created {len(sellers)} sellers')

    # Create categories
    categories_data = [
        'Electronics', 'Clothing', 'Home & Garden', 'Books', 'Sports',
        'Beauty', 'Toys', 'Automotive', 'Health', 'Food & Beverage'
    ]
    
    categories = []
    for cat_name in categories_data:
        category = Category.objects.create(
            name=cat_name,
            description=f'Products in the {cat_name} category'
        )
        categories.append(category)
    print(f'Created {len(categories)} categories')

    # Create products
    products = []
    adjectives = ['Premium', 'Deluxe', 'Standard', 'Basic', 'Professional', 'Ultimate']
    nouns = ['Widget', 'Gadget', 'Tool', 'Device', 'Accessory', 'Kit']
    
    for i in range(200):
        product = Product.objects.create(
            title=f'{random.choice(adjectives)} {random.choice(nouns)} {i+1}',
            description=f'This is a fantastic product #{i+1} that will change your life. High quality and durable.',
            price=random.uniform(10.00, 500.00),
            stock=random.randint(0, 100),
            category=random.choice(categories),
            seller=random.choice(sellers),
            image_url=f'https://picsum.photos/300/300?random={i+1}',
            is_active=True
        )
        products.append(product)
    print(f'Created {len(products)} products')

    # Create orders
    orders = []
    for i in range(20):
        buyer = random.choice(buyers)
        order = Order.objects.create(
            user=buyer,
            total_price=0,
            status=random.choice(['pending', 'processing', 'shipped', 'delivered', 'cancelled'])
        )
        
        # Add random products to order
        num_products = random.randint(1, 5)
        selected_products = random.sample(products, min(num_products, len(products)))
        total_price = 0
        
        for product in selected_products:
            quantity = random.randint(1, 3)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
            total_price += product.price * quantity
        
        order.total_price = total_price
        order.save()
        orders.append(order)
    print(f'Created {len(orders)} orders')

    # Create reviews
    reviews = []
    for i in range(50):
        buyer = random.choice(buyers)
        product = random.choice(products)
        
        # Check if user already reviewed this product
        if not Review.objects.filter(user=buyer, product=product).exists():
            review = Review.objects.create(
                user=buyer,
                product=product,
                rating=random.randint(1, 5),
                comment=f'This is review #{i+1}. The product is {"amazing" if random.randint(1, 5) > 3 else "okay"}.'
            )
            reviews.append(review)
    print(f'Created {len(reviews)} reviews')

    print("Successfully loaded demo data!")

if __name__ == "__main__":
    load_demo_data()