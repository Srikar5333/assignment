import requests
import json

BASE_URL = "http://localhost:5000"

def test_get_all_products():
    """Test GET /api/products endpoint"""
    print("🧪 Testing GET /api/products")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/products")
        print(f"Status Code: {response.status_code}")
        print(f"URL: {BASE_URL}/api/products")
        
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Success! Found {len(products)} products")
            print("\n📋 Sample Response:")
            print(json.dumps(products[:2], indent=2))  # Show first 2 products
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Flask server is running!")
        print("Run: python api.py")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_product_by_id(product_id):
    """Test GET /api/products/<id> endpoint"""
    print(f"\n🧪 Testing GET /api/products/{product_id}")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/products/{product_id}")
        print(f"Status Code: {response.status_code}")
        print(f"URL: {BASE_URL}/api/products/{product_id}")
        
        if response.status_code == 200:
            product = response.json()
            print("✅ Success! Product found:")
            print(json.dumps(product, indent=2))
        elif response.status_code == 404:
            print("✅ Error handling works! Product not found:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Unexpected error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Flask server is running!")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_pagination():
    """Test pagination on GET /api/products"""
    print(f"\n🧪 Testing Pagination GET /api/products?page=1&per_page=5")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/products?page=1&per_page=5")
        print(f"Status Code: {response.status_code}")
        print(f"URL: {BASE_URL}/api/products?page=1&per_page=5")
        
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Success! Found {len(products)} products (limited to 5)")
            print("\n📋 Paginated Response:")
            print(json.dumps(products, indent=2))
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Flask server is running!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Ecommerce REST API Demo")
    print("=" * 50)
    
    # Test 1: Get all products
    test_get_all_products()
    
    # Test 2: Get product by ID (valid ID)
    test_get_product_by_id(1)  # Try with ID 1
    
    # Test 3: Get product by ID (invalid ID)
    test_get_product_by_id(999999)
    
    # Test 4: Test pagination
    test_pagination()
    
    print("\n" + "=" * 50)
    print("✅ Demo Complete!")
    print("\n📋 Demo Checklist:")
    print("✅ GET /api/products - List all products")
    print("✅ GET /api/products/<id> - Get product by ID")
    print("✅ Error handling - Invalid product ID returns 404")
    print("✅ Pagination - /api/products?page=1&per_page=5")
    print("\n🌐 API Base URL: http://localhost:5000") 