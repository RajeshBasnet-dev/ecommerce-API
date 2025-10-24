import requests
import json

# Base URL for the API
BASE_URL = 'http://127.0.0.1:8000'

def test_jwt_authentication():
    print("Testing JWT Authentication...")
    
    # Test 1: Try to access a protected endpoint without authentication
    print("\n1. Testing access to protected endpoint without authentication:")
    response = requests.get(f'{BASE_URL}/api/products/')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 2: Register a new user
    print("\n2. Registering a new user:")
    register_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'StrongPass123!',
        'role': 'buyer'
    }
    response = requests.post(f'{BASE_URL}/api/auth/register/', 
                           json=register_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 3: Obtain JWT token
    print("\n3. Obtaining JWT token:")
    token_data = {
        'username': 'testuser',
        'password': 'StrongPass123!'
    }
    response = requests.post(f'{BASE_URL}/api/token/', 
                           json=token_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access']
        refresh_token = tokens['refresh']
        print(f"Access Token: {access_token[:50]}...")
        print(f"Refresh Token: {refresh_token[:50]}...")
    else:
        print(f"Response: {response.json()}")
        return
    
    # Test 4: Access protected endpoint with valid token
    print("\n4. Accessing protected endpoint with valid token:")
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'{BASE_URL}/api/products/', headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 5: Refresh token
    print("\n5. Refreshing token:")
    refresh_data = {'refresh': refresh_token}
    response = requests.post(f'{BASE_URL}/api/token/refresh/', 
                           json=refresh_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        new_tokens = response.json()
        new_access_token = new_tokens['access']
        print(f"New Access Token: {new_access_token[:50]}...")
    else:
        print(f"Response: {response.json()}")

if __name__ == '__main__':
    test_jwt_authentication()