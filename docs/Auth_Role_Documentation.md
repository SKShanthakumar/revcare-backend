# Authentication & Role Documentation

**Project:** RevCare - Vehicle Service Management System (FastAPI)  
**Version:** v1.0  
**Last Updated:** November 2025

## Overview

This document explains how authentication and role-based access control (RBAC) are implemented in the RevCare backend system built with FastAPI.

It covers login/registration flow, token management, permission scopes, and permissions assigned to each user role (Admin, Mechanic, Customer).

## Authentication Flow

| Step | Description |
|------|-------------|
| 1. Register | User registers using phone, email, and password (with role-specific data). |
| 2. Login | System verifies credentials (phone & password) and issues both Access and Refresh tokens. |
| 3. Access Token | Short-lived JWT (default: 30 min) for authenticated requests. |
| 4. Refresh Token | Long-lived JWT (default: 7 days) stored in HTTP-only cookie to renew access tokens. |
| 5. Token Revocation | Logout invalidates both access and refresh tokens (stored in database blacklist). |
| 6. Protected Routes | Middleware verifies token, checks blacklist, and validates required scopes before route access. |

## JWT Token Structure

### Access Token Payload Example

```json
{
  "sub": "CST000001",
  "role": 3,
  "jti": "550e8400-e29b-41d4-a716-446655440000",
  "type": "access",
  "iat": 1730000000,
  "exp": 1730001800
}
```

### Refresh Token Payload Example

```json
{
  "sub": "CST000001",
  "role": 3,
  "jti": "660e8400-e29b-41d4-a716-446655440001",
  "type": "refresh",
  "iat": 1730000000,
  "exp": 1730604800
}
```

### Token Fields

- **sub**: User ID (CST000001 for Customer, MEC000001 for Mechanic, ADM000001 for Admin)
- **role**: Role ID (1=Admin, 2=Mechanic, 3=Customer)
- **jti**: Unique token identifier (UUID4) for revocation tracking
- **type**: Token type ("access" or "refresh")
- **iat**: Issued at timestamp
- **exp**: Expiration timestamp

## Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/login` | Login and get JWT tokens | No |
| POST | `/api/v1/auth/refresh` | Refresh expired access token | No (uses cookie) |
| POST | `/api/v1/auth/logout` | Logout and revoke tokens | Yes |

### Login Endpoint

**Request:**
```bash
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=9841385379&password=your_password
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Cookie Set:**
- `refresh_token`: HTTP-only cookie containing refresh token

### Refresh Endpoint

**Request:**
```bash
POST /api/v1/auth/refresh
Cookie: refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Logout Endpoint

**Request:**
```bash
POST /api/v1/auth/logout
Authorization: Bearer <access_token>
Cookie: refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

## Role-Based Access Control (RBAC)

### Roles

| Role| Description | User ID Prefix |
|------|-------------|----------------|
| Admin | Full system access, manages users, services, bookings, and system settings | ADM |
| Mechanic | Handles assigned bookings, creates analysis reports, updates service progress | MEC |
| Customer | Books services, tracks progress, makes payments, manages vehicles | CST |

### Role Permissions Matrix

#### User Management

| Resource | Action | Admin | Mechanic | Customer |
|----------|--------|:-----:|:--------:|:--------:|
| Users | Read | ✅ | ✅ | ✅ |
| Users | Create | ✅ | ❌ | ❌ |
| Users | Update | ✅ | ❌ | ❌ |
| Users | Delete | ✅ | ❌ | ❌ |
| Customers | Read | ✅ | ✅ | ✅ |
| Customers | Create | ✅ | ❌ | ❌ |
| Customers | Update | ✅ | ❌ | ✅ (own) |
| Customers | Delete | ✅ | ❌ | ✅ (own) |
| Mechanics | Read | ✅ | ✅ | ✅ |
| Mechanics | Create | ✅ | ❌ | ❌ |
| Mechanics | Update | ✅ | ✅ (own) | ❌ |
| Mechanics | Delete | ✅ | ❌ | ❌ |
| Admins | Read | ✅ | ❌ | ❌ |
| Admins | Create | ✅ | ❌ | ❌ |
| Admins | Update | ✅ | ❌ | ❌ |
| Admins | Delete | ✅ | ❌ | ❌ |

#### Service Management

| Resource | Action | Admin | Mechanic | Customer |
|----------|--------|:-----:|:--------:|:--------:|
| Services | Read | ✅ | ✅ | ✅ |
| Services | Create | ✅ | ❌ | ❌ |
| Services | Update | ✅ | ❌ | ❌ |
| Services | Delete | ✅ | ❌ | ❌ |
| Service Categories | Read | ✅ | ✅ | ✅ |
| Service Categories | Create | ✅ | ❌ | ❌ |
| Service Categories | Update | ✅ | ❌ | ❌ |
| Service Categories | Delete | ✅ | ❌ | ❌ |
| Price Chart | Read | ✅ | ✅ | ✅ |
| Price Chart | Create | ✅ | ❌ | ❌ |
| Price Chart | Update | ✅ | ❌ | ❌ |
| Price Chart | Delete | ✅ | ❌ | ❌ |
| Service Reviews | Read | ✅ | ✅ | ✅ |
| Service Reviews | Create | ✅ | ❌ | ✅ |
| Service Reviews | Update | ✅ | ❌ | ✅ (own) |
| Service Reviews | Delete | ✅ | ❌ | ✅ (own) |

#### Booking Management

| Resource | Action | Admin | Mechanic | Customer |
|----------|--------|:-----:|:--------:|:--------:|
| Bookings | Read | ✅ | ✅ | ✅ (own) |
| Bookings | Create | ✅ | ❌ | ✅ |
| Bookings | Update | ✅ | ❌ | ✅ (own) |
| Bookings | Delete | ✅ | ❌ | ❌ |
| Booking Assignment | Read | ✅ | ✅ | ✅ |
| Booking Assignment | Create | ✅ | ❌ | ❌ |
| Booking Assignment | Update | ✅ | ✅ (own) | ❌ |
| Booking Assignment | Delete | ✅ | ❌ | ❌ |
| Booking Analysis | Read | ✅ | ✅ | ✅ |
| Booking Analysis | Create | ✅ | ✅ | ❌ |
| Booking Analysis | Update | ✅ | ❌ | ❌ |
| Booking Analysis | Delete | ✅ | ❌ | ❌ |
| Booking Progress | Read | ✅ | ✅ | ✅ |
| Booking Progress | Create | ✅ | ✅ | ❌ |
| Booking Progress | Update | ✅ | ❌ | ❌ |
| Booking Progress | Delete | ✅ | ❌ | ❌ |

#### Vehicle Management

| Resource | Action | Admin | Mechanic | Customer |
|----------|--------|:-----:|:--------:|:--------:|
| Car Models | Read | ✅ | ✅ | ✅ |
| Car Models | Create | ✅ | ❌ | ❌ |
| Car Models | Update | ✅ | ❌ | ❌ |
| Car Models | Delete | ✅ | ❌ | ❌ |
| Customer Cars | Read | ✅ | ✅ | ✅ (own) |
| Customer Cars | Create | ✅ | ❌ | ✅ |
| Customer Cars | Update | ✅ | ❌ | ✅ (own) |
| Customer Cars | Delete | ✅ | ❌ | ✅ (own) |

#### Address Management

| Resource | Action | Admin | Mechanic | Customer |
|----------|--------|:-----:|:--------:|:--------:|
| Addresses | Read | ✅ | ✅ | ✅ (own) |
| Addresses | Create | ✅ | ❌ | ✅ |
| Addresses | Update | ✅ | ❌ | ✅ (own) |
| Addresses | Delete | ✅ | ❌ | ✅ (own) |
| Areas | Read | ✅ | ✅ | ✅ |
| Areas | Create | ✅ | ❌ | ❌ |
| Areas | Update | ✅ | ❌ | ❌ |
| Areas | Delete | ✅ | ❌ | ❌ |

#### Cart & Favourites

| Resource | Action | Admin | Mechanic | Customer |
|----------|--------|:-----:|:--------:|:--------:|
| Cart | Read | ✅ | ✅ | ✅ (own) |
| Cart | Create | ✅ | ❌ | ✅ |
| Cart | Update | ✅ | ❌ | ❌ |
| Cart | Delete | ✅ | ❌ | ✅ (own) |
| Favourites | Read | ✅ | ✅ | ✅ (own) |
| Favourites | Create | ✅ | ❌ | ✅ |
| Favourites | Update | ✅ | ❌ | ❌ |
| Favourites | Delete | ✅ | ❌ | ✅ (own) |

#### Content & System Management

| Resource | Action | Admin | Mechanic | Customer |
|----------|--------|:-----:|:--------:|:--------:|
| Content | Read | ✅ | ✅ | ✅ |
| Content | Update | ✅ | ❌ | ❌ |
| GST | Read | ✅ | ✅ | ✅ |
| GST | Update | ✅ | ❌ | ❌ |
| Queries | Read | ✅ | ❌ | ✅ (own) |
| Queries | Create | ✅ | ❌ | ✅ |
| Queries | Update | ✅ | ❌ | ❌ |
| Notification Logs | Read | ✅ | ❌ | ❌ |
| Notification Logs | Create | ✅ | ❌ | ❌ |
| Backup | Read | ✅ | ❌ | ❌ |
| Backup | Create | ✅ | ❌ | ❌ |
| Backup | Restore | ✅ | ❌ | ❌ |
| Backup | Delete | ✅ | ❌ | ❌ |

## Permission Scopes

The system uses permission scopes to control access to specific resources and actions. Each scope follows the format: `<ACTION>:<RESOURCE>`.

### Scope Format

- **READ**: Read access to resource
- **WRITE**: Create access to resource
- **UPDATE**: Update access to resource
- **DELETE**: Delete access to resource

### Example Scopes

- `READ:BOOKINGS` - Read bookings
- `WRITE:BOOKINGS` - Create bookings
- `UPDATE:BOOKINGS` - Update bookings
- `DELETE:BOOKINGS` - Delete bookings
- `READ:BOOKING_ASSIGNMENT` - Read booking assignments
- `WRITE:BOOKING_ASSIGNMENT` - Create booking assignments
- `WRITE:BOOKING_PROGRESS` - Create progress updates
- `WRITE:BOOKING_ANALYSIS` - Create analysis reports

### All Available Scopes

#### RBAC Management
- `READ:RBAC`, `WRITE:RBAC`, `UPDATE:RBAC`, `DELETE:RBAC`

#### User Management
- `READ:USERS`, `WRITE:USERS`, `UPDATE:USERS`, `DELETE:USERS`
- `READ:CUSTOMERS`, `WRITE:CUSTOMERS`, `UPDATE:CUSTOMERS`, `DELETE:CUSTOMERS`
- `READ:MECHANICS`, `WRITE:MECHANICS`, `UPDATE:MECHANICS`, `DELETE:MECHANICS`
- `READ:ADMINS`, `WRITE:ADMINS`, `UPDATE:ADMINS`, `DELETE:ADMINS`

#### Service Management
- `READ:SERVICES`, `WRITE:SERVICES`, `UPDATE:SERVICES`, `DELETE:SERVICES`
- `READ:SERVICE_CATEGORIES`, `WRITE:SERVICE_CATEGORIES`, `UPDATE:SERVICE_CATEGORIES`, `DELETE:SERVICE_CATEGORIES`
- `READ:PRICE_CHART`, `WRITE:PRICE_CHART`, `UPDATE:PRICE_CHART`, `DELETE:PRICE_CHART`
- `READ:SERVICE_REVIEWS`, `WRITE:SERVICE_REVIEWS`, `UPDATE:SERVICE_REVIEWS`, `DELETE:SERVICE_REVIEWS`

#### Booking Management
- `READ:BOOKINGS`, `WRITE:BOOKINGS`, `UPDATE:BOOKINGS`, `DELETE:BOOKINGS`
- `READ:BOOKED_SERVICES`, `WRITE:BOOKED_SERVICES`, `UPDATE:BOOKED_SERVICES`, `DELETE:BOOKED_SERVICES`
- `READ:BOOKING_ASSIGNMENT`, `WRITE:BOOKING_ASSIGNMENT`, `UPDATE:BOOKING_ASSIGNMENT`, `DELETE:BOOKING_ASSIGNMENT`
- `READ:BOOKING_ANALYSIS`, `WRITE:BOOKING_ANALYSIS`, `UPDATE:BOOKING_ANALYSIS`, `DELETE:BOOKING_ANALYSIS`
- `READ:BOOKING_PROGRESS`, `WRITE:BOOKING_PROGRESS`, `UPDATE:BOOKING_PROGRESS`, `DELETE:BOOKING_PROGRESS`
- `READ:BOOKING_RECOMMENDATIONS`, `WRITE:BOOKING_RECOMMENDATIONS`, `UPDATE:BOOKING_RECOMMENDATIONS`, `DELETE:BOOKING_RECOMMENDATIONS`

#### Vehicle Management
- `READ:CARS`, `WRITE:CARS`, `UPDATE:CARS`, `DELETE:CARS`
- `READ:CUSTOMER_CARS`, `WRITE:CUSTOMER_CARS`, `UPDATE:CUSTOMER_CARS`, `DELETE:CUSTOMER_CARS`

#### Address Management
- `READ:ADDRESSES`, `WRITE:ADDRESSES`, `UPDATE:ADDRESSES`, `DELETE:ADDRESSES`
- `READ:AREAS`, `WRITE:AREAS`, `UPDATE:AREAS`, `DELETE:AREAS`

#### Cart & Favourites
- `READ:CART`, `WRITE:CART`, `UPDATE:CART`, `DELETE:CART`
- `READ:FAVOURITES`, `WRITE:FAVOURITES`, `UPDATE:FAVOURITES`, `DELETE:FAVOURITES`

#### Content & System Management
- `READ:CONTENT`, `UPDATE:CONTENT`
- `READ:GST`, `UPDATE:GST`
- `READ:QUERIES`, `WRITE:QUERIES`, `UPDATE:QUERIES`
- `READ:NOTIFICATION_LOG`, `WRITE:NOTIFICATION_LOG`, `UPDATE:NOTIFICATION_LOG`, `DELETE:NOTIFICATION_LOG`
- `READ:BACKUP`, `WRITE:BACKUP`, `UPDATE:BACKUP`, `DELETE:BACKUP`

#### Utilities
- `READ:UTILS`, `WRITE:UTILS`, `UPDATE:UTILS`, `DELETE:UTILS`

#### Token Management
- `READ:REFRESH_TOKENS`, `WRITE:REFRESH_TOKENS`, `UPDATE:REFRESH_TOKENS`, `DELETE:REFRESH_TOKENS`

## Middleware & Token Validation

All protected routes include a dependency that validates tokens, checks blacklist, and verifies required scopes.

### Token Validation Flow

1. **Extract Token**: Token extracted from `Authorization: Bearer <token>` header
2. **Decode Token**: JWT decoded and signature verified using secret key
3. **Check Blacklist**: Token JTI checked against revoked tokens database
4. **Load User**: User loaded from database based on user ID prefix (CST/MEC/ADM)
5. **Load Role Permissions**: Role permissions loaded from database
6. **Validate Scopes**: Required scopes checked against user's role permissions
7. **Return Payload**: User data and token info returned for route handler

### Implementation Example

```python
from fastapi import Depends, Security
from app.auth.dependencies import validate_token

@router.get("/bookings/customer")
async def get_customer_bookings(
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["READ:BOOKINGS"])
):
    # payload contains: user_id, role, user_data, jti, exp
    return await booking_service.get_customer_bookings(db, payload)
```

### Scope-Based Dependency

The `validate_token` dependency automatically validates:
- Token signature and expiration
- Token revocation status (blacklist)
- Required scopes for the endpoint
- User existence and role

If any validation fails, an `HTTPException` is raised:
- **401**: Invalid token, expired token, or insufficient permissions
- **403**: Token has been revoked/blacklisted

## Frontend Integration Notes

### Token Storage

- **Access Token**: Store in memory or secure storage (not localStorage for XSS protection)
- **Refresh Token**: Automatically stored in HTTP-only cookie (more secure)

### Making Authenticated Requests

Always include the access token in the Authorization header:

```javascript
fetch('/api/v1/bookings/customer', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
})
```

### Handling Token Expiration

1. **Automatic Refresh**: When access token expires (401 response), automatically call `/auth/refresh`
2. **Cookie Handling**: Refresh endpoint uses HTTP-only cookie, so no manual token handling needed
3. **Retry Request**: After receiving new access token, retry the original request

### Example Frontend Flow

```javascript
// Login
const loginResponse = await fetch('/api/v1/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: 'username=9841385379&password=password',
  credentials: 'include' // Important for cookies
});

const { access_token } = await loginResponse.json();
// Store access_token in memory

// Make authenticated request
let response = await fetch('/api/v1/bookings/customer', {
  headers: { 'Authorization': `Bearer ${access_token}` },
  credentials: 'include'
});

// If token expired, refresh and retry
if (response.status === 401) {
  const refreshResponse = await fetch('/api/v1/auth/refresh', {
    method: 'POST',
    credentials: 'include' // Cookie automatically sent
  });
  const { access_token: newToken } = await refreshResponse.json();
  
  // Retry original request with new token
  response = await fetch('/api/v1/bookings/customer', {
    headers: { 'Authorization': `Bearer ${newToken}` },
    credentials: 'include'
  });
}
```

## Token Expiry Policy

| Token Type | Lifetime | Storage | Rotation |
|------------|----------|---------|----------|
| Access Token | 30 minutes (configurable) | In-memory / Header | Auto-rotated via refresh endpoint |
| Refresh Token | 7 days (configurable) | HTTP-only Cookie / Database | Revoked on logout or expiry |

### Configuration

Token expiration times are configured in `.env` file:

```env
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Example Sequence (Login → Access → Refresh → Logout)

### 1. User Login

```bash
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=9841385379&password=password123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Cookie Set:**
```
Set-Cookie: refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...; HttpOnly; SameSite=Lax
```

### 2. Access Protected Endpoint

```bash
GET /api/v1/bookings/customer
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
[
  {
    "id": 1,
    "car": {...},
    "status": "booked",
    ...
  }
]
```

### 3. Token Expired - Refresh

```bash
POST /api/v1/auth/refresh
Cookie: refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 4. User Logout

```bash
POST /api/v1/auth/logout
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Cookie: refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

**Both tokens are now blacklisted and invalid.**

## Security Considerations

### Best Practices

1. **HTTPS in Production**: Always use HTTPS in production to encrypt token transmission
2. **Strong Secret Keys**: Use strong, randomly generated secret keys for JWT signing
3. **Token Revocation**: Tokens are blacklisted on logout and cannot be reused
4. **HTTP-Only Cookies**: Refresh tokens stored in HTTP-only cookies prevent XSS attacks
5. **Scope Validation**: Every endpoint validates required scopes before allowing access
6. **Password Hashing**: Passwords hashed using Argon2 (cryptographically secure)
7. **Token Expiration**: Short-lived access tokens reduce risk of token theft
8. **JTI Tracking**: Unique token identifiers (JTI) enable token revocation tracking

### Security Features

- **Token Blacklist**: Revoked tokens stored in database and checked on every request
- **Role-Based Access**: Fine-grained permission control using scopes
- **User ID Prefixes**: User IDs have prefixes (CST/MEC/ADM) for easy role identification
- **Separate Secret Keys**: Access and refresh tokens use different secret keys
- **Token Type Validation**: Tokens include "type" field to prevent token misuse

### Monitoring & Logging

- Failed login attempts should be monitored for brute-force protection
- Token validation failures should be logged for security auditing
- Unauthorized access attempts should be tracked

## Error Responses

### Authentication Errors

**401 Unauthorized - Invalid Token:**
```json
{
  "detail": "Invalid token."
}
```

**401 Unauthorized - Insufficient Permissions:**
```json
{
  "detail": "Insufficient permissions."
}
```

**403 Forbidden - Token Revoked:**
```json
{
  "detail": "Token has been revoked."
}
```

**401 Unauthorized - Invalid Credentials:**
```json
{
  "detail": "Invalid phone number."
}
```

or

```json
{
  "detail": "Incorrect password."
}
```

**401 Unauthorized - Refresh Token Missing:**
```json
{
  "detail": "Refresh token missing"
}
```

## User Registration

Users are registered through role-specific endpoints:

- **Customer**: `POST /api/v1/customers/`
- **Mechanic**: `POST /api/v1/mechanics/`
- **Admin**: `POST /api/v1/admins/`

Each registration creates:
1. User record in `users` table (for authentication)
2. Role-specific record (Customer/Mechanic/Admin table)
3. Automatic user ID generation with prefix (CST/MEC/ADM)

## Role Assignment

Roles are assigned automatically during user creation:
- Customer registration → Role ID: 3
- Mechanic registration → Role ID: 2
- Admin registration → Role ID: 1

Roles cannot be changed after user creation (in current implementation).

## Permission Scope Assignment

Permission scopes are assigned to roles in the database during system initialization (seed data). The mapping is defined in `app/utilities/scopes.py` and seeded into the `roles` and `permissions` tables.

### Adding New Permissions

1. Add new scope to `scopes` dictionary in `app/utilities/scopes.py`
2. Run database seed to update permissions
3. Assign scope to appropriate roles
4. Use scope in route dependencies: `Security(validate_token, scopes=["NEW:SCOPE"])`

## Testing Authentication

### Test Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=9841385379&password=Sk18102004." \
  -c cookies.txt
```

### Test Protected Endpoint

```bash
curl -X GET "http://localhost:8000/api/v1/bookings/customer" \
  -H "Authorization: Bearer <access_token>" \
  -b cookies.txt
```

### Test Refresh

```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -b cookies.txt
```

### Test Logout

```bash
curl -X POST "http://localhost:8000/api/v1/auth/logout" \
  -H "Authorization: Bearer <access_token>" \
  -b cookies.txt
```

## Additional Resources

- **API Documentation**: Visit `/docs` when application is running for interactive API documentation
- **ReDoc Documentation**: Visit `/redoc` for alternative API documentation
- **Source Code**: 
  - Authentication: `app/auth/`
  - Token Validation: `app/auth/dependencies.py`
  - JWT Handler: `app/auth/jwt_handler.py`
  - Permission Scopes: `app/utilities/scopes.py`
