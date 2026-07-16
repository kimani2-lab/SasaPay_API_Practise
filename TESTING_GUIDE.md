"""
SasaPay API - Authentication & Transaction Testing Guide

This module demonstrates how to use the API with authentication.
Run the development server: python manage.py runserver

Testing commands using curl or requests library.
"""

# ============================================================================
# AUTHENTICATION FLOW TEST
# ============================================================================

# 1. REGISTER NEW USER
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'

# Response: Returns token like "abc123xyz789"
# Save token for next requests


# 2. LOGIN WITH CREDENTIALS
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'


# ============================================================================
# PROTECTED ENDPOINTS (Require Token)
# ============================================================================

# Set token variable (Linux/Mac):
TOKEN="your_token_here"

# 3. GET CURRENT USER PROFILE
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Token $TOKEN"


# 4. UPDATE USER PROFILE
curl -X PATCH http://localhost:8000/api/users/update_profile/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "TestUpdated",
    "email": "newemail@example.com"
  }'


# 5. CREATE TRANSACTION
curl -X POST http://localhost:8000/api/transactions/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reference": "TXN20260716001",
    "amount": "5000.00",
    "status": "pending"
  }'


# 6. LIST ALL TRANSACTIONS (Paginated)
curl -X GET http://localhost:8000/api/transactions/ \
  -H "Authorization: Token $TOKEN"

# With filtering:
curl -X GET "http://localhost:8000/api/transactions/?status=pending" \
  -H "Authorization: Token $TOKEN"

# With pagination:
curl -X GET "http://localhost:8000/api/transactions/?page=1" \
  -H "Authorization: Token $TOKEN"


# 7. GET SINGLE TRANSACTION
curl -X GET http://localhost:8000/api/transactions/1/ \
  -H "Authorization: Token $TOKEN"


# 8. UPDATE TRANSACTION
curl -X PUT http://localhost:8000/api/transactions/1/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reference": "TXN20260716001",
    "amount": "5000.00",
    "status": "completed"
  }'


# 9. MARK TRANSACTION AS COMPLETED
curl -X POST http://localhost:8000/api/transactions/1/mark_completed/ \
  -H "Authorization: Token $TOKEN"


# 10. MARK TRANSACTION AS FAILED
curl -X POST http://localhost:8000/api/transactions/1/mark_failed/ \
  -H "Authorization: Token $TOKEN"


# 11. GET PENDING TRANSACTIONS
curl -X GET http://localhost:8000/api/transactions/pending/ \
  -H "Authorization: Token $TOKEN"


# 12. GET COMPLETED TRANSACTIONS
curl -X GET http://localhost:8000/api/transactions/completed/ \
  -H "Authorization: Token $TOKEN"


# 13. GET TRANSACTION SUMMARY (Statistics)
curl -X GET http://localhost:8000/api/transactions/summary/ \
  -H "Authorization: Token $TOKEN"


# 14. CHANGE PASSWORD
curl -X POST http://localhost:8000/api/users/change_password/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "testpass123",
    "new_password": "newpass456"
  }'

# Response: Returns new token


# 15. REFRESH TOKEN
curl -X POST http://localhost:8000/api/auth/refresh_token/ \
  -H "Authorization: Token $TOKEN"


# 16. LOGOUT (Delete Token)
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Token $TOKEN"

# After logout, token becomes invalid for future requests


# ============================================================================
# PYTHON REQUESTS EXAMPLE
# ============================================================================

import requests
import json

API_URL = "http://localhost:8000/api"

# Register user
response = requests.post(
    f"{API_URL}/auth/register/",
    json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "password2": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
)
data = response.json()
token = data['token']
print(f"Token: {token}")

# Set headers for authenticated requests
headers = {"Authorization": f"Token {token}"}

# Create transaction
response = requests.post(
    f"{API_URL}/transactions/",
    headers=headers,
    json={
        "reference": "TXN20260716001",
        "amount": "5000.00",
        "status": "pending"
    }
)
print(f"Transaction created: {response.json()}")

# List transactions
response = requests.get(
    f"{API_URL}/transactions/",
    headers=headers
)
print(f"Transactions: {response.json()}")

# Get summary
response = requests.get(
    f"{API_URL}/transactions/summary/",
    headers=headers
)
print(f"Summary: {response.json()}")

# Logout
response = requests.post(
    f"{API_URL}/auth/logout/",
    headers=headers
)
print(f"Logout: {response.json()}")


# ============================================================================
# KEY FEATURES DEMONSTRATED
# ============================================================================

"""
✅ SERIALIZERS:
   - UserRegistrationSerializer: Custom validation (password matching)
   - UserLoginSerializer: Credentials validation
   - TransactionSerializer: Amount & reference validation
   - UserDetailSerializer: Method fields (transaction_count)

✅ VIEWSETS:
   - AuthViewSet: Custom actions (register, login, logout, refresh_token)
   - UserViewSet: Profile management & password change
   - TransactionViewSet: Full CRUD + custom actions

✅ ROUTERS:
   - DefaultRouter: Automatic URL generation
   - Nested routes: /api/auth/register/, /api/transactions/pending/, etc.
   - DRF Browsable API: http://localhost:8000/api/

✅ AUTHENTICATION:
   - Token Authentication: Authorization header with token
   - Session Authentication: Cookie-based (for web frontend)
   - Permission Classes: IsAuthenticated for protected endpoints
   - Token Management: Create on signup, refresh, delete on logout

✅ ADVANCED FEATURES:
   - Field validation: amount > 0, unique reference
   - Status choices: pending, completed, failed, cancelled
   - Filtering: ?status=pending
   - Pagination: ?page=1 (10 items per page)
   - Custom actions: @action decorators
   - Error handling: Try/except with appropriate HTTP status codes
   - Timestamps: created_at, updated_at, date_joined
"""
