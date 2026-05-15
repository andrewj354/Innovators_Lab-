# API Endpoints Documentation

## Base URL
- Development: `http://localhost:8000`
- API Gateway: `http://localhost:8000/api`

## Authentication Endpoints

### 1. User Registration
**POST** `/api/auth/register/`

Request:
```json
{
  "email": "user@example.com",
  "username": "username",
  "first_name": "First",
  "last_name": "Last",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!"
}
```

Response (201):
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "first_name": "First",
  "last_name": "Last",
  "message": "User registered successfully"
}
```

---

### 2. User Login
**POST** `/api/auth/login/`

Request:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

Response (200):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "first_name": "First",
    "last_name": "Last",
    "two_fa_enabled": false
  }
}
```

---

### 3. Refresh Access Token
**POST** `/api/auth/refresh/`

Headers:
```
Content-Type: application/json
```

Request:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

Response (200):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### 4. Get Current User Profile
**GET** `/api/auth/me/`

Headers:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

Response (200):
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "first_name": "First",
  "last_name": "Last",
  "is_active": true,
  "date_joined": "2025-09-09T12:00:00Z",
  "profile": {
    "phone": "",
    "address": "",
    "date_of_birth": null
  }
}
```

---

## Password Reset Endpoints

### 5. Request Password Reset
**POST** `/api/auth/forgot-password/`

Request:
```json
{
  "email": "user@example.com"
}
```

Response (200):
```json
{
  "message": "Password reset link sent to email",
  "token": "reset_token_here"
}
```

---

### 6. Reset Password
**POST** `/api/auth/reset-password/`

Request:
```json
{
  "token": "reset_token_here",
  "new_password": "NewSecurePass123!"
}
```

Response (200):
```json
{
  "message": "Password reset successfully"
}
```

---

## Two-Factor Authentication (2FA) Endpoints

### 7. Enable 2FA - Generate Secret
**POST** `/api/auth/2fa/enable/`

Headers:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

Response (200):
```json
{
  "secret": "JBSWY3DPEBLW64TMMQ======",
  "qr_code_uri": "otpauth://totp/user@example.com?secret=JBSWY3DPEBLW64TMMQ%3D%3D%3D%3D%3D%3D&issuer=Innovators+Lab",
  "message": "Scan this QR code with your authenticator app"
}
```

---

### 8. Verify and Enable 2FA
**POST** `/api/auth/2fa/verify/`

Headers:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

Request:
```json
{
  "secret": "JBSWY3DPEBLW64TMMQ======",
  "code": "123456"
}
```

Response (200):
```json
{
  "message": "2FA enabled successfully",
  "two_fa_enabled": true
}
```

---

### 9. Verify 2FA Code During Login
**POST** `/api/auth/2fa/verify-login/`

Headers:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

Request:
```json
{
  "code": "123456"
}
```

Response (200):
```json
{
  "message": "2FA verification successful",
  "verified": true
}
```

---

### 10. Disable 2FA
**POST** `/api/auth/2fa/disable/`

Headers:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

Response (200):
```json
{
  "message": "2FA disabled",
  "two_fa_enabled": false
}
```

---

## User Profile Endpoints

### 11. Get User Profile
**GET** `/api/users/profile/`

Headers:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

Response (200):
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "first_name": "First",
  "last_name": "Last",
  "is_active": true,
  "date_joined": "2025-09-09T12:00:00Z",
  "profile": {
    "phone": "+1-234-567-8900",
    "address": "123 Main St",
    "date_of_birth": "1990-01-15"
  }
}
```

---

### 12. Update User Profile
**PUT/PATCH** `/api/users/profile/update/`

Headers:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

Request:
```json
{
  "phone": "+1-234-567-8900",
  "address": "123 Main St",
  "date_of_birth": "1990-01-15"
}
```

Response (200):
```json
{
  "phone": "+1-234-567-8900",
  "address": "123 Main St",
  "date_of_birth": "1990-01-15"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Error message describing what went wrong"
}
```

### 401 Unauthorized
```json
{
  "error": "Invalid credentials"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Frontend Integration Notes

1. **Base URL**: Frontend configuration should use `VITE_API_URL=http://localhost:8000`
2. **Token Storage**: Access and refresh tokens are stored in localStorage
3. **Token Refresh**: Client automatically refreshes tokens when 401 is received
4. **CORS**: All endpoints support CORS with proper headers
5. **2FA Flow**:
   - User enables 2FA: POST `/api/auth/2fa/enable/` → Get secret & QR code
   - User scans QR with authenticator app
   - User verifies code: POST `/api/auth/2fa/verify/` → Enable 2FA
   - On login, user provides 2FA code for verification

---

## Running Services

### User Service (Port 8000)
```bash
cd services/user-service
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### API Gateway (Port 8000)
```bash
cd api-gateway
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### Frontend (Port 3000)
```bash
cd frontend
npm install
npm run dev
```

---

## Testing Workflow

1. **Register new user**: POST `/api/auth/register/`
2. **Login**: POST `/api/auth/login/` → Get access & refresh tokens
3. **Get profile**: GET `/api/users/profile/` (requires token)
4. **Enable 2FA**: POST `/api/auth/2fa/enable/` → Get QR code
5. **Verify 2FA**: POST `/api/auth/2fa/verify/` with code
6. **Refresh token**: POST `/api/auth/refresh/` when token expires

---
