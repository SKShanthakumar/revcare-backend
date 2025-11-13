# RevCare – API Documentation

**Version:** 1.0.0
**Framework:** FastAPI  
**Authentication:** OAuth2 Password Flow with JWT Bearer (`Authorization: Bearer <access_token>`)  
**Content Type:** `application/json`  
**Last Updated:** 10 Nov 2025

---

## Overview

RevCare is a vehicle service management backend that supports three roles—**Admin**, **Mechanic**, and **Customer**—to streamline end-to-end service operations. Core features include vehicle onboarding, booking lifecycle tracking, secure payment processing, and proactive notifications.

The API is organised by resource-first routing (`/auth`, `/customers`, `/bookings`, etc.) and relies on scope-based RBAC. All protected endpoints require a valid access token with appropriate permission scopes.

---

## Roles & Permissions

| Role | Capabilities |
| --- | --- |
| **Admin** | Manage users (admins, mechanics, customers), services, bookings, payments, configurations, notifications, backups |
| **Mechanic** | View assigned jobs, publish analysis, update booking progress, confirm completions |
| **Customer** | Manage profile, vehicles, addresses, favourites, cart, create bookings, confirm services, track status, make payments |

> **Note:** Detailed scope-to-role mapping is available in `docs/Auth_Role_Documentation.md`.

---

## Authentication Flow

1. Customer/Admin/Mechanic submits credentials (`/auth/login`).
2. Access token (30 min) + HTTP-only refresh token (7 days) issued.
3. Attach access token to protected requests via `Authorization: Bearer <token>`.
4. When access token expires, call `/auth/refresh` to obtain a new one.
5. `/auth/logout` revokes both tokens (blacklisted in DB).

---

## Authentication Endpoints

### Login

| Method | Endpoint | Auth | Description |
| --- | --- | --- | --- |
| `POST` | `/auth/login` | No | Authenticate user and issue access/refresh tokens |

**Request (form-data):**
```json
{
  "username": "9841385379",
  "password": "Password@123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

Refresh token is stored in an HTTP-only cookie named `refresh_token`.

---

### Refresh Access Token

| Method | Endpoint | Auth | Description |
| --- | --- | --- | --- |
| `POST` | `/auth/refresh` | Yes (cookie) | Generate a new access token using a valid refresh token |

Send cookie `refresh_token=<token>`.

**Response:**
```json
{
  "access_token": "new_access_token",
  "token_type": "bearer"
}
```

---

### Logout

| Method | Endpoint | Auth | Description |
| --- | --- | --- | --- |
| `POST` | `/auth/logout` | Yes | Revoke tokens and clear refresh cookie |

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

---

## Admin Endpoints

Admin users manage platform-wide data. All endpoints require access tokens with admin scopes.

### Manage Admin Users

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/admins/` | Create new admin |
| `GET` | `/admins/` | List admins |
| `GET` | `/admins/{id}` | Fetch admin by ID |
| `PUT` | `/admins/{id}` | Update admin |
| `DELETE` | `/admins/{id}` | Delete admin |

**Sample Request** `POST /admins/`
```json
{
  "first_name": "Akhil",
  "last_name": "Joseph",
  "email": "akhil@revcare.in",
  "phone": "9000000001"
}
```

**Sample Response**
```json
{
  "id": "ADM000012",
  "first_name": "Akhil",
  "last_name": "Joseph",
  "email": "akhil@revcare.in"
}
```

---

### Manage Mechanics

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/mechanics/` | Create mechanic profile |
| `GET` | `/mechanics/` | List mechanics (filter by `mechanic_id`) |
| `PUT` | `/mechanics/{id}` | Update mechanic |
| `DELETE` | `/mechanics/{id}` | Delete mechanic |

Mechanic assignment utilities: `/mechanics/assignment_type` (CRUD) to maintain assignment categories.

---

### Service Catalogue Management

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/services/` | Create service |
| `PUT` | `/services/{id}` | Update service |
| `DELETE` | `/services/{id}` | Remove service |
| `POST` | `/services/category` | Create category |
| `PUT` | `/services/category/{id}` | Update category |
| `DELETE` | `/services/category/{id}` | Delete category |
| `PUT` | `/services/review/{service_id}` | Moderate reviews |

---

### Booking Oversight

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/bookings/admin/dashboard` | Aggregated view with status filters |
| `POST` | `/bookings/admin/assign` | Assign mechanic to booking |
| `PUT` | `/bookings/admin/progress/{progress_id}` | Edit mechanic progress |
| `POST` | `/bookings/admin/progress/{progress_id}/validate` | Validate progress |
| `PUT` | `/bookings/admin/analysis/{booking_id}` | Edit analysis report |
| `POST` | `/bookings/admin/analysis/{booking_id}/validate` | Approve analysis |

---

### Platform Settings

- **Content Management:** `PUT /content/` to update CMS entries (home banner, T&C, etc.).
- **GST Management:** `PUT /gst/?percent=18` to modify active GST rate.
- **Backup & Restore:**
  - `POST /backup/create`
  - `GET /backup/list`
  - `POST /backup/restore`
  - `DELETE /backup/delete/{backup_name}`
- **Notifications:** `GET /notification/notifications/logs` with filters (`notification_category`, `limit`).

---

## Mechanic Endpoints

Mechanics focus on assigned bookings. All routes require mechanic scopes.

### Assignments & Workflows

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/bookings/mechanic/assignments` | List assignments for logged-in mechanic |
| `POST` | `/bookings/mechanic/analysis` | Submit vehicle analysis (estimated cost/time) |
| `POST` | `/bookings/mechanic/progress` | Post progress updates (per service item) |

**Sample Request** `POST /bookings/mechanic/progress`
```json
{
  "booking_id": 1021,
  "service_id": 45,
  "status_id": 7,
  "notes": "Engine diagnostics completed"
}
```

**Sample Response**
```json
{
  "id": 501,
  "booking_id": 1021,
  "status": "in-progress",
  "updated_by": "MEC000034",
  "timestamp": "2025-11-13T08:41:24Z"
}
```

---

## Customer Endpoints

Customers manage personal data, vehicles, and bookings.

### Profile & Utilities

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/customers/` | Get current customer (optionally by `customer_id` for admins) |
| `PUT` | `/customers/{id}` | Update profile |
| `DELETE` | `/customers/{id}` | Delete account |
| `POST` | `/customers/cart/{service_id}` | Add service to cart |
| `DELETE` | `/customers/cart/{service_id}` | Remove from cart |
| `POST` | `/customers/favourite/{service_id}` | Add to favourites |
| `DELETE` | `/customers/favourite/{service_id}` | Remove favourite |

Addresses: CRUD at `/address/` and `/address/area` (creation limited to admins).

Vehicles: `/car/` (customer cars), `/car/models`, `/car/class`, `/car/fuel`, `/car/manufacturer` for reference data.

---

### Booking Lifecycle

| Step | Endpoint | Description |
| --- | --- | --- |
| 1 | `POST /bookings/` | Create booking (choose services, timeslot, pickup/drop) |
| 2 | `GET /bookings/customer` | View own bookings |
| 3 | `PUT /bookings/{booking_id}/confirm-services` | Confirm services & choose payment mode |
| 4 | `PUT /bookings/{booking_id}/cancel` | Cancel booking (with fees) |
| 5 | `GET /bookings/{booking_id}` | Detailed booking view (services, timeline, mechanics) |

**Sample Booking Request**
```json
{
  "customer_id": "CST000210",
  "vehicle_id": 88,
  "pickup_type": "doorstep",
  "timeslot_id": 12,
  "services": [
    { "service_id": 45, "quantity": 1 },
    { "service_id": 52, "quantity": 1 }
  ],
  "notes": "Need quick turnaround"
}
```

---

### Payments

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/payment/cash-on-delivery/{booking_id}` | Reserve booking for COD |
| `POST` | `/payment/verify` | Verify Razorpay online payment signature |
| `POST` | `/payment/verify-cod` | Confirm COD completion |

**Webhook Support:** configure Razorpay webhook to hit dedicated endpoints (see service code for signature validation).

---

## Utility Endpoints

- `GET /utils/status` & `POST /utils/status` – status master data.
- `GET /utils/timeslot` – available service slots.
- `GET /content/{content_id}` – fetch CMS content (e.g., offers banner).

---

## Error Handling

| Status | Meaning | Description |
| --- | --- | --- |
| `400` | Bad Request | Validation or business rule failure |
| `401` | Unauthorized | Missing or invalid token |
| `403` | Forbidden | Token lacks required scope |
| `404` | Not Found | Resource does not exist |
| `409` | Conflict | Duplicate entries or state conflict |
| `422` | Unprocessable Entity | Pydantic validation errors |
| `500` | Internal Server Error | Unexpected server failure |

Global exception middleware standardises error payloads:
```json
{
  "status": 403,
  "message": "Forbidden",
  "detail": "WRITE:BOOKINGS scope required"
}
```

---

## Token Lifecycle & Security

| Token | Validity | Stored | Notes |
| --- | --- | --- | --- |
| Access Token | 30 minutes | Client memory/local storage | Include as `Authorization` header |
| Refresh Token | 7 days | HttpOnly cookie (`refresh_token`) | Refresh flow at `/auth/refresh` |
| Revoked Tokens | Until TTL | PostgreSQL blacklist | Checked on every request |

Additional security controls:
- **Dependency Injection:** `validate_token` ensures scope validation per route.
- **Request Logging:** Middleware logs method, path, status, latency (PII excluded).
- **Password Hashing:** Argon2 via `passlib`.
- **Email & Payments:** Razorpay integration for online payments; FastMail for transactional mails.

---

## Sample Authorization Header

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Release Notes & Future Work

- **Planned:** pagination for large list endpoints, advanced filtering, webhook signatures in docs, multi-tenant support.
- **Documentation:** Auto-generated Swagger UI available at `/docs`; redoc at `/redoc` (if enabled).

---

**Contact:** backend@smartcliff.in  
**Repository Docs:** `README.md`, `docs/System_Architecture.md`, `docs/Auth_Role_Documentation.md`

**End of API Documentation**
