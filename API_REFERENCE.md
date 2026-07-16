# SasaPay API - Complete Reference

## Authentication Endpoints

### Register New User
**POST** `/api/auth/register/`
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_pass123",
  "password2": "secure_pass123",
  "first_name": "John",
  "last_name": "Doe"
}
```
**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "token": "abc123xyz789",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "date_joined": "2026-07-16T10:00:00Z"
  }
}
```

### Login User
**POST** `/api/auth/login/`
```json
{
  "username": "john_doe",
  "password": "secure_pass123"
}
```
**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "abc123xyz789",
  "user": {...}
}
```

### Logout User
**POST** `/api/auth/logout/` *(Requires Token Auth)*
```
Header: Authorization: Token abc123xyz789
```

### Refresh Token
**POST** `/api/auth/refresh_token/` *(Requires Token Auth)*

---

## User Profile Endpoints

### Get Current User Profile
**GET** `/api/users/me/` *(Requires Token Auth)*

### Get All Users (Admin Only)
**GET** `/api/users/` *(Requires Token Auth)*

### Update Profile
**PATCH** `/api/users/update_profile/` *(Requires Token Auth)*
```json
{
  "first_name": "Jonathan",
  "last_name": "Smith"
}
```

### Change Password
**POST** `/api/users/change_password/` *(Requires Token Auth)*
```json
{
  "old_password": "secure_pass123",
  "new_password": "new_secure_pass456"
}
```

---

## Transaction Endpoints

### List All Transactions (Paginated)
**GET** `/api/transactions/` *(Requires Token Auth)*
Query Parameters:
- `status=pending` - Filter by status
- `page=1` - Pagination

### Create Transaction
**POST** `/api/transactions/` *(Requires Token Auth)*
```json
{
  "reference": "TXN001",
  "amount": "1500.50",
  "status": "pending"
}
```

### Get Transaction
**GET** `/api/transactions/{id}/` *(Requires Token Auth)*

### Update Transaction
**PUT** `/api/transactions/{id}/` *(Requires Token Auth)*
```json
{
  "status": "completed"
}
```

### Delete Transaction
**DELETE** `/api/transactions/{id}/` *(Requires Token Auth)*

### Mark Transaction as Completed
**POST** `/api/transactions/{id}/mark_completed/` *(Requires Token Auth)*

### Mark Transaction as Failed
**POST** `/api/transactions/{id}/mark_failed/` *(Requires Token Auth)*

### Get All Pending Transactions
**GET** `/api/transactions/pending/` *(Requires Token Auth)*

### Get All Completed Transactions
**GET** `/api/transactions/completed/` *(Requires Token Auth)*

### Get Transaction Summary
**GET** `/api/transactions/summary/` *(Requires Token Auth)*
```json
{
  "total_transactions": 50,
  "pending": 10,
  "completed": 35,
  "failed": 5,
  "total_amount": 75000.50
}
```

---

## Authentication Methods

### 1. Token Authentication
Include token in request header:
```
Authorization: Token abc123xyz789
```

### 2. Session Authentication
Login via session and CSRF token (for web frontend)

---

## Key Features Demonstrated

### Serializers
- **UserRegistrationSerializer**: Custom validation (password matching, unique fields)
- **UserLoginSerializer**: Authentication validation
- **UserDetailSerializer**: Nested/method fields (transaction_count)
- **TransactionSerializer**: Field-level validation, create method override

### ViewSets
- **AuthViewSet**: Custom actions (register, login, logout, refresh_token)
- **UserViewSet**: Full CRUD with custom actions (me, update_profile, change_password)
- **TransactionViewSet**: Full CRUD with filtering, custom actions, and business logic

### Routers
- DefaultRouter with automatic URL generation
- Nested endpoints support
- Browsable API integration

### Authentication
- Token-based (DRF TokenAuthentication)
- Session-based (SessionAuthentication)
- Permission classes (IsAuthenticated, AllowAny)
- Custom permission handling

---

## Testing Flow

1. Register: POST `/api/auth/register/` → Get token
2. Use token in Authorization header for all protected endpoints
3. Create transaction: POST `/api/transactions/`
4. Update transaction: PUT/PATCH `/api/transactions/{id}/`
5. Get summary: GET `/api/transactions/summary/`
6. Change password: POST `/api/users/change_password/` → Get new token
7. Logout: POST `/api/auth/logout/` → Token deleted
