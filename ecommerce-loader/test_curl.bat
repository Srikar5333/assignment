@echo off
echo 🚀 Testing Ecommerce REST API
echo ================================================

echo.
echo 1. Testing GET /api/products
echo ------------------------------------------------
curl -X GET http://localhost:5000/api/products

echo.
echo.
echo 2. Testing GET /api/products/1
echo ------------------------------------------------
curl -X GET http://localhost:5000/api/products/1

echo.
echo.
echo 3. Testing Error Handling - Invalid ID
echo ------------------------------------------------
curl -X GET http://localhost:5000/api/products/999999

echo.
echo.
echo 4. Testing Pagination
echo ------------------------------------------------
curl -X GET "http://localhost:5000/api/products?page=1&per_page=5"

echo.
echo.
echo ✅ Demo Complete!
pause 