# System Architecture Document

**Project:** RevCare - Vehicle Service Management System  
**Version:** 1.0  
**Last Updated:** November 2025  
**Technology Stack:** FastAPI + PostgreSQL + MongoDB

## 1. Summary

RevCare is a RESTful API-based application designed to manage vehicle service bookings, tracking, invoicing, and management for customers, mechanics, and administrators. Built with FastAPI, PostgreSQL, and MongoDB, it provides secure, scalable endpoints for service centers to streamline vehicle servicing operations, from booking to delivery.

The system supports role-based access control, real-time service progress tracking, payment processing, email notifications, and comprehensive booking management workflows.

## 2. System Overview

### 2.1 Purpose

- Centralized management of vehicle service bookings and service records
- Role-based access for customers, mechanics, and administrators
- Real-time service progress tracking and status updates
- Secure authentication and authorization with JWT tokens
- Payment processing with online (Razorpay) and offline payment options
- Automated email notifications for booking confirmations, progress updates, and invoices
- Service analysis and recommendation system
- Dynamic content management for app configuration

### 2.2 Key Features

- **User Management**: Registration and login for customers, mechanics, and admins with role-based access control
- **Service Booking & Scheduling**: Customers can book vehicle service appointments with date/time selection
- **Service Tracking**: Real-time service progress tracking with status updates (Booked → Pickup → Received → Analysis → In Progress → Completed → Delivered)
- **Vehicle Management**: Add/manage multiple vehicles with complete service history
- **Service Analysis**: Mechanics can provide analysis reports with price quotes and service recommendations
- **Progress Updates**: Mechanics can update service progress with images and descriptions
- **Billing & Payments**: Auto-generated invoices with support for online (Razorpay) and offline payments
- **Notifications**: Email notifications for booking confirmations, progress updates, invoices, and query responses
- **Customer Queries**: Query management system with admin responses
- **Content Management**: Dynamic content management for app content (MongoDB)
- **GST Management**: Configurable GST percentage management
- **Backup & Recovery**: Database backup and restore functionality for both PostgreSQL and MongoDB

## 3. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                         │
│  (Web App, Mobile App, Third-party Integrations)            │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS/REST
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    API Gateway / Load Balancer              │
│                    (nginx/Cloud LB)                         │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   FastAPI Application                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Global Exception Handler Middleware          │   │
│  │         (HTTP, Database, General Exceptions)         │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                   │
│  ┌──────────────────────▼───────────────────────────────┐   │
│  │         Authentication Middleware                    │   │
│  │    (JWT Token Validation & RBAC Scope Check)         │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                   │
│  ┌──────────────────────▼───────────────────────────────┐   │
│  │              API Router Layer                        │   │
│  │  • /auth    • /bookings   • /services                │   │
│  │  • /customers • /mechanics • /admins                 │   │
│  │  • /payment • /queries   • /content                  │   │
│  │  • /backup  • /notification • /gst                   │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                   │
│  ┌──────────────────────▼───────────────────────────────┐   │
│  │            Business Logic Layer                      │   │
│  │  • Booking Management  • Service Management          │   │
│  │  • Payment Processing  • Notification Service        │   │
│  │  • Analysis & Progress • Content Management          │   │ 
│  │  • Backup & Recovery   • Query Management            │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                   │
│  ┌──────────────────────▼───────────────────────────────┐   │
│  │          Data Access Layer (ORM/ODM)                 │   │
│  │     SQLAlchemy (PostgreSQL) + Motor (MongoDB)        │   │
│  └──────────────────────┬───────────────────────────────┘   │
└─────────────────────────┼───────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼────────┐  ┌─────▼──────┐  ┌───────▼────────┐
│   PostgreSQL   │  │  MongoDB   │  │  External APIs │
│   (Primary DB) │  │  (NoSQL)   │  │  • Razorpay    │
│                │  │            │  │  • Email SMTP  │
│ • Users        │  │ • Queries  │  └────────────────┘
│ • Bookings     │  │ • Content  │
│ • Services     │  │ • GST      │
│ • Payments     │  │            │
│ • Vehicles     │  │            │
│ • Addresses    │  │            │
└────────────────┘  └────────────┘
```

## 4. Component Architecture

### 4.1 Application Layer Components

#### Authentication & Authorization Service
- JWT token generation and validation (access & refresh tokens)
- Password hashing using Argon2
- Role-based access control (RBAC) with permission scopes
- Token blacklist for revocation
- Session management with HTTP-only cookies
- Token refresh mechanism

#### User Management Service
- User CRUD operations (Customer, Mechanic, Admin)
- User registration with automatic ID generation (CST/MEC/ADM prefixes)
- Role assignment and permission management
- User profile updates with access control

#### Booking Management Service
- Booking creation with service selection and address management
- Booking status management (state machine: booked → pickup → received → analysis → in-progress → completed → delivered)
- Service confirmation after analysis
- Booking cancellation with fee calculation
- Booking assignment to mechanics
- Progress tracking and updates

#### Service Management Service
- Service CRUD operations
- Service category management
- Price chart management (car class-based pricing)
- Service-fuel type associations
- Service reviews and ratings
- Cart and favourites management

#### Vehicle Management Service
- Car model management (manufacturer, fuel type, car class)
- Customer car management
- Vehicle service history tracking
- Car class and fuel type management

#### Payment Service
- Razorpay integration for online payments
- Payment signature verification
- Payment status management
- Offline payment processing
- Cash on delivery (COD) handling
- Refund management
- Invoice generation

#### Notification Service
- Email notification sending (FastMail)
- Booking confirmation emails
- Progress update emails
- Invoice emails
- Query response emails
- Notification logging and tracking

#### Analysis & Progress Service
- Service analysis creation by mechanics
- Price quote generation
- Service recommendations
- Progress update creation with images
- Progress validation by admin
- Analysis validation by admin

#### Content Management Service
- Dynamic content storage in MongoDB
- Content retrieval by content_id
- Bulk content updates
- GST percentage management

#### Query Management Service
- Customer query creation
- Admin query responses
- Query storage in MongoDB
- Email notification on response

#### Backup & Recovery Service
- PostgreSQL backup creation and restoration
- MongoDB backup creation and restoration
- Full system backup
- Backup listing and deletion
- Metadata management

### 4.2 Data Layer Components

#### PostgreSQL Database
- Primary data store for structured data
- ACID compliance for transactional operations
- Relational data integrity with foreign keys
- Async operations with SQLAlchemy
- Connection pooling for performance

**Main Entities:**
- Users, Customers, Mechanics, Admins
- Bookings, BookedServices, BookingAssignments
- BookingProgress, BookingAnalysis, BookingRecommendations
- Services, ServiceCategories, PriceCharts
- Cars, CustomerCars, Manufacturers, CarClasses, FuelTypes
- Addresses, Areas
- Payments (Online, Offline), Refunds
- Carts, Favourites, ServiceReviews
- Statuses, AssignmentTypes, Timeslots, PaymentMethods
- Roles, Permissions, RefreshTokens, RevokedTokens
- NotificationLogs, NotificationCategories

#### MongoDB Database
- NoSQL data store for flexible schema data
- Used for queries, content, and GST management
- Async operations with Motor driver
- Document-based storage

**Collections:**
- `queries`: Customer queries and admin responses
- `content`: Dynamic app content (banners, text, etc.)
- `gst`: GST percentage configuration

### 4.3 External Services

#### Razorpay Payment Gateway
- Online payment processing
- Payment order creation
- Payment signature verification
- Webhook handling for payment confirmation

#### Email Service (SMTP)
- Email notification sending
- HTML template rendering
- Attachment support
- Email logging

## 5. Database Schema Overview

### 5.1 PostgreSQL Schema

#### User Management
```
Users (phone, password, role_id)
  ├── Customers (id: CST*, name, email, phone, role_id)
  ├── Mechanics (id: MEC*, name, email, phone, dob, pickup_drop, analysis, role_id, service_categories)
  └── Admins (id: ADM*, name, email, phone, role_id)

Roles (id, role_name)
  └── Permissions (id, permission)
      └── Role-Permission (many-to-many)
```

#### Booking Management
```
Bookings (id, customer_id, car_reg_number, status_id, pickup_address_id, 
          drop_address_id, pickup_date, drop_date, pickup_timeslot_id, 
          drop_timeslot_id, payment_method_id, created_at, completed_at)
  ├── BookedServices (booking_id, service_id, status_id, est_price, price, completed)
  ├── BookingAssignments (id, booking_id, mechanic_id, assignment_type_id, 
                           status_id, note, assigned_at)
  ├── BookingProgress (id, booking_id, mechanic_id, description, images, 
                        status_id, completed_service_ids, validated, created_at)
  ├── BookingAnalysis (booking_id, mechanic_id, description, recommendation, 
                        images, validated, created_at)
  ├── BookingRecommendations (booking_id, service_id, price)
  ├── OnlinePayments (id, booking_id, status_id, amount, gst, 
                       razorpay_order_id, razorpay_payment_id, razorpay_signature)
  ├── OfflinePayments (id, booking_id, status_id, amount, gst, paid_online)
  └── Refunds (id, booking_id, customer_id, status_id, amount)
```

#### Service Management
```
Services (id, title, description, category_id, works, warranty_kms, 
          warranty_months, time_hrs, difficulty, images, created_at)
  ├── PriceChart (service_id, car_class_id, price)
  ├── ServiceReviews (customer_id, service_id, rating, review, created_at)
  └── ServiceFuelTypes (service_id, fuel_type_id) [many-to-many]

ServiceCategories (id, name, description)

Carts (customer_id, service_id)
Favourites (customer_id, service_id)
```

#### Vehicle Management
```
Cars (id, model, manufacturer_id, fuel_type_id, car_class_id, year, img)
  └── CustomerCars (id, customer_id, car_id, reg_number)

Manufacturers (id, name)
CarClasses (id, class_)
FuelTypes (id, fuel_name)
```

#### Address Management
```
Areas (id, name, pincode)
Addresses (id, customer_id, label, line1, line2, area_id)
```

#### Utility Tables
```
Statuses (id, name)
AssignmentTypes (id, name)
Timeslots (id, name, start_time, end_time)
PaymentMethods (id, name)
NotificationCategories (id, name)
NotificationLogs (id, notification_category_id, recipient_email, 
                   subject, attachments, timestamp)
```

#### Token Management
```
RefreshTokens (jti, token, user_id, expires_at)
RevokedTokens (jti, expires_at)
```

### 5.2 MongoDB Schema

#### Queries Collection
```json
{
  "_id": ObjectId,
  "customer_email": "customer@example.com",
  "query": "Query text",
  "response": "Admin response",
  "responded_by": "ADM000001",
  "created_at": ISODate,
  "responded_at": ISODate
}
```

#### Content Collection
```json
{
  "_id": ObjectId,
  "content_id": "home_banner",
  "data": "https://cdn.example.com/banner.png",
  "updated_by": "ADM000001",
  "updated_at": ISODate
}
```

#### GST Collection
```json
{
  "_id": ObjectId,
  "percent": "18%",
  "updated_by": "ADM000001",
  "updated_at": ISODate
}
```

## 6. Data Flow Diagrams

### 6.1 Customer Booking Flow

```
Customer → API Gateway → FastAPI
                         │
                         ▼
                    Auth Middleware
            (Verify JWT, Check: WRITE:BOOKINGS)
                         │
                         ▼
                POST /api/v1/bookings/
                         │
                         ▼
                    Booking Service
                (Validate car ownership, 
                 Calculate service time, 
                 Get/create addresses)
                         │
                         ▼
                    SQLAlchemy ORM
            (Create booking + booked_services)
                         │
                         ▼
                    PostgreSQL
                (Commit transaction)
                         │
                         ▼
                    Notification Service
            (Send booking confirmation email)
                         │
                         ▼
                Return JSON Response
                (Booking details)
```

### 6.2 Service Analysis & Confirmation Flow

```
Mechanic → Create Analysis → API Gateway → FastAPI
                                         │
                                         ▼
                                    Auth Middleware
                                (Verify Role: Mechanic, 
                             Check: WRITE:BOOKING_ANALYSIS)
                                         │
                                         ▼
                        POST /api/v1/bookings/mechanic/analysis
                                         │
                                         ▼
                                    Analysis Service
                                (Create analysis report,
                                 Update service prices,
                                 Create recommendations)
                                         │
                                         ▼
                                    PostgreSQL
                        (Update booking status to 'analysed')
                                         │
                                         ▼
                                Return Analysis Response
                                         │
                                         ▼
Customer → Confirm Services → API Gateway → FastAPI
                                         │
                                         ▼
                                    Auth Middleware
                                    (Verify: WRITE:BOOKINGS)
                                         │
                                         ▼
                                    PUT /api/v1/bookings/{id}/confirm-services
                                         │
                                         ▼
                                    Booking Service
                                (Calculate total with GST,
                                 Create payment record)
                                         │
                                         ▼
                                    Payment Service
                            (Create Razorpay order if online)
                                         │
                                         ▼
                                    PostgreSQL
                            (Update services, create payment)
                                         │
                                         ▼
                                Return Payment Order
                                (or success for offline)
```

### 6.3 Payment Webhook Flow

```
Razorpay → Webhook → API Gateway → FastAPI
                                 │
                                 ▼
                            POST /api/v1/payment/verify
                                 │
                                 ▼
                            Payment Service
                            (Verify signature,
                         Check payment status)
                                 │
                                 ▼
                            Booking Service
                        (Confirm selected services,
                 Update booking status to 'in-progress')
                                 │
                                 ▼
                            PostgreSQL
                        (Update payment status,
                         Confirm services,
                         Update booking status)
                                 │
                                 ▼
                            Notification Service
                            (Send invoice email)
                                 │
                                 ▼
                        Return Success Response
```

### 6.4 Progress Update Flow

```
Mechanic → Update Progress → API Gateway → FastAPI
                                         │
                                         ▼
                                    Auth Middleware
                                (Verify Role: Mechanic,
                             Check: WRITE:BOOKING_PROGRESS)
                                         │
                                         ▼
                        POST /api/v1/bookings/mechanic/progress
                                         │
                                         ▼
                                    Booking Service
                                (Validate assignment,
                             Mark services as completed,
                                 Update booking status)
                                         │
                                         ▼
                                    PostgreSQL
                                (Create progress record,
                                 Update booking status,
                                 Update assignment status)
                                         │
                                         ▼
                                    Return Progress Response
                                         │
                                         ▼
Admin → Validate Progress → API Gateway → FastAPI
                                         │
                                         ▼
                                    Auth Middleware
                            (Verify: UPDATE:BOOKING_PROGRESS)
                                         │
                                         ▼
                    POST /api/v1/bookings/admin/progress/{id}/validate
                                         │
                                         ▼
                                    Booking Service
                                (Award mechanic score,
                         Update booking status if all completed,
                             Send progress update email)
                                         │
                                         ▼
                                    PostgreSQL
                            (Update progress validated,
                             Update mechanic score,
                                 Update booking status)
                                         │
                                         ▼
                                    Notification Service
                                (Send progress update email)
                                         │
                                         ▼
                                Return Success Response
```

## 7. Security Architecture

### 7.1 Authentication Flow

1. **User Login** → `POST /api/v1/auth/login`
   - Validate credentials (phone & password)
   - Verify password using Argon2
   - Generate JWT access token (30 min, configurable)
   - Generate refresh token (7 days, configurable)
   - Store refresh token in database
   - Set refresh token as HTTP-only cookie
   - Return access token

2. **Protected Request** → Header: `Authorization: Bearer {token}`
   - Middleware validates JWT signature
   - Check token expiration
   - Verify token not blacklisted
   - Extract user_id and role
   - Load user from database (Customer/Mechanic/Admin)
   - Load role permissions from database
   - Check required scopes against user permissions
   - Process request or return 401/403

3. **Token Refresh** → `POST /api/v1/auth/refresh`
   - Extract refresh token from HTTP-only cookie
   - Validate refresh token signature
   - Check token not blacklisted
   - Generate new access token
   - Return new access token

4. **Logout** → `POST /api/v1/auth/logout`
   - Blacklist access token (store in RevokedTokens)
   - Blacklist refresh token (store in RevokedTokens)
   - Remove refresh token from database
   - Delete refresh token cookie
   - Return success response

### 7.2 Authorization Matrix

| Resource | Action | Admin | Mechanic | Customer |
|----------|--------|:-----:|:--------:|:--------:|
| Bookings | Create | ✅ | ❌ | ✅ |
| Bookings | Read | ✅ (all) | ✅ (assigned) | ✅ (own) |
| Bookings | Update | ✅ | ❌ | ✅ (own) |
| Bookings | Delete | ✅ | ❌ | ❌ |
| Booking Assignment | Create | ✅ | ❌ | ❌ |
| Booking Assignment | Read | ✅ | ✅ (own) | ✅ |
| Booking Progress | Create | ✅ | ✅ (assigned) | ❌ |
| Booking Progress | Update | ✅ | ❌ | ❌ |
| Booking Analysis | Create | ✅ | ✅ (assigned) | ❌ |
| Booking Analysis | Update | ✅ | ❌ | ❌ |
| Services | Create | ✅ | ❌ | ❌ |
| Services | Read | ✅ | ✅ | ✅ |
| Services | Update | ✅ | ❌ | ❌ |
| Services | Delete | ✅ | ❌ | ❌ |
| Payments | Process | ✅ | ✅ (COD) | ✅ (own) |
| Customers | Manage | ✅ | ❌ | ✅ (own) |
| Mechanics | Manage | ✅ | ✅ (own) | ❌ |
| Admins | Manage | ✅ | ❌ | ❌ |
| Content | Manage | ✅ | ❌ | ❌ |
| Backup | Manage | ✅ | ❌ | ❌ |

### 7.3 Security Measures

- **Password Storage**: Argon2 hashing with salt (cryptographically secure)
- **API Security**: JWT with short expiration (30 minutes for access token)
- **Token Revocation**: Token blacklist in database for immediate revocation
- **Input Validation**: Pydantic models for all inputs with type validation
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **NoSQL Injection Prevention**: Motor driver with parameterized queries
- **CORS Configuration**: Configurable CORS for allowed origins
- **Audit Logging**: All critical operations logged (payments, status changes)
- **HTTP-Only Cookies**: Refresh tokens stored in HTTP-only cookies (XSS protection)
- **Token Type Validation**: Tokens include "type" field to prevent misuse
- **Scope-Based Access**: Fine-grained permission control using scopes
- **Payment Signature Verification**: Razorpay payment signature verification for webhooks


## 8. API Architecture Patterns

### 8.1 RESTful Design Principles

- **Resource-based URLs**: `/api/v1/bookings`, `/api/v1/services`
- **HTTP methods for CRUD operations**: GET, POST, PUT, DELETE
- **Stateless communication**: No server-side session state
- **JSON request/response format**: All requests and responses in JSON
- **Versioned APIs**: `/api/v1/` prefix for API versioning
- **Nested resources**: `/api/v1/bookings/{id}/confirm-services`
- **Query parameters**: Filtering, pagination, sorting

### 8.2 Response Format Standard

**Success Response:**
```json
{
  "id": 1,
  "customer": {...},
  "car": {...},
  "status": "booked",
  ...
}
```

**Error Response:**
```json
{
  "detail": "Error message description"
}
```

### 8.3 API Endpoint Organization

- **Authentication**: `/api/v1/auth/*`
- **Customers**: `/api/v1/customers/*`
- **Mechanics**: `/api/v1/mechanics/*`
- **Admins**: `/api/v1/admins/*`
- **Bookings**: `/api/v1/bookings/*`
- **Services**: `/api/v1/services/*`
- **Cars**: `/api/v1/car/*`
- **Addresses**: `/api/v1/address/*`
- **Payments**: `/api/v1/payment/*`
- **Content**: `/api/v1/content/*`
- **Queries**: `/api/v1/queries/*`
- **Backup**: `/api/v1/backup/*`
- **Notifications**: `/api/v1/notification/*`
- **GST**: `/api/v1/gst/*`
- **Utilities**: `/api/v1/utils/*`

## 9. Performance Considerations

### 9.1 Optimization Strategies

- **Database Indexing**: 
  - Primary keys on all tables
  - Foreign key indexes
  - Frequently queried fields (customer_id, booking_id, status_id)
  - Composite indexes for common query patterns

- **Query Optimization**: 
  - Eager loading with `selectinload` to prevent N+1 queries
  - Batch loading for related entities
  - Pagination for large datasets (default: 50-100 records)
  - Query result caching for frequently accessed data

- **Caching Strategy**: 
  - Cache service lists and categories
  - Cache price charts
  - Cache user permissions
  - Cache frequently accessed booking data

- **Async Operations**: 
  - All database operations are async
  - Background tasks for email sending
  - Async payment processing
  - Async backup operations

- **Connection Pooling**: 
  - Database connection reuse with SQLAlchemy
  - MongoDB connection pooling with Motor
  - Configurable pool size and timeout

- **Bulk Operations**: 
  - Bulk inserts for price charts
  - Bulk updates for service status
  - Batch processing for notifications

### 9.2 Scalability

- **Horizontal Scaling**: Multiple FastAPI instances behind load balancer
- **Database Scaling**: 
  - PostgreSQL read replicas for reporting queries
  - MongoDB replica set for high availability
- **Caching Layer**: Redis for session storage and frequently accessed data
- **CDN**: Static assets and API responses where appropriate
- **Microservices Ready**: Modular architecture allows service separation

### 9.3 Performance Metrics

- **API Response Time**: Target < 200ms for simple queries, < 500ms for complex operations
- **Database Query Time**: Target < 100ms for simple queries
- **Concurrent Users**: Support for 1000+ concurrent users
- **Throughput**: Handle 10,000+ requests per minute

## 10. Monitoring & Observability

### 10.1 Key Metrics

- **API Metrics**: 
  - Response times by endpoint
  - Request success/failure rates
  - Request count by endpoint
  - Error rates by endpoint

- **Database Metrics**: 
  - Query performance
  - Connection pool usage
  - Database size and growth
  - Slow query logs

- **Business Metrics**: 
  - Active bookings count
  - Booking completion rate
  - Payment success rate
  - Average service time
  - Customer satisfaction (reviews)

- **System Metrics**: 
  - CPU and memory usage
  - Disk I/O
  - Network traffic
  - Active user sessions

### 10.2 Alerting

- **Critical Alerts**: 
  - Database connection failures
  - Payment gateway failures
  - High error rates
  - System resource exhaustion

- **Warning Alerts**: 
  - Slow API responses
  - High database query times
  - Unusual request patterns
  - Backup failures

## 11. Future Enhancements

1. **Mobile App Integration**: Dedicated Android/iOS app with push notifications
2. **Real-time Notifications**: WebSocket support for real-time updates
3. **Chatbot Support**: LLM-based AI chatbot for customer queries and service suggestions
4. **AI-Powered Predictive Maintenance**: Predict when a vehicle might need servicing
5. **Multi-Language Support**: Support for regional languages
6. **Advanced Analytics Dashboard**: Charts and graphs for business insights
7. **SMS Notifications**: SMS alerts in addition to email notifications
8. **Geo-Location Services**: Real-time vehicle pickup & drop tracking
9. **Loyalty & Rewards System**: Points or discounts for frequent customers
10. **Dynamic Pricing**: Personalized offers and seasonal discounts
11. **Inventory Management**: Spare parts stock management
12. **Multi-Branch Support**: Support for multiple service center branches
13. **Advanced Reporting**: Custom report generation with filters
14. **Integration with CRM**: Customer relationship management integration
15. **Automated Scheduling**: AI-powered mechanic assignment optimization

## 12. Technology Stack Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| API Framework | FastAPI 0.120.0 | RESTful API server |
| Language | Python 3.11+ | Backend logic |
| ORM | SQLAlchemy 2.0.44 | PostgreSQL database abstraction |
| ODM | Motor 3.7.1 | MongoDB async driver |
| Primary Database | PostgreSQL 12+ | Structured data storage |
| NoSQL Database | MongoDB 4.4+ | Flexible schema data (queries, content, GST) |
| Authentication | JWT (python-jose) | Token-based authentication |
| Password Hashing | Argon2 | Secure password storage |
| Validation | Pydantic 2.12.3 | Input validation and serialization |
| Migration | Alembic | Database versioning (optional) |
| Payment Gateway | Razorpay | Online payment processing |
| Email Service | FastMail | Email notification sending |
| Documentation | OpenAPI/Swagger | Auto-generated API docs |
| ASGI Server | Uvicorn | FastAPI server |
| Template Engine | Jinja2 | Email template rendering |

## 13. Development Guidelines

### 13.1 Code Structure

```
revCare-phase2/
├── app/
│   ├── auth/                 # Authentication & authorization
│   │   ├── dependencies.py   
│   │   ├── hashing.py        
│   │   ├── jwt_handler.py    
│   │   └── token_blacklist.py 
│   ├── core/                 # Core configuration
│   │   └── config.py         
│   ├── database/             # Database configuration & dependencies
│   │   ├── dependencies.py   
│   │   ├── mongo.py          
│   │   ├── postgresql.py     
│   │   └── utils.py          
│   ├── middlewares/          # Middleware
│   │   └── error_handler.py  
│   ├── models/               # SQLAlchemy models
│   │   ├── booking.py        
│   │   ├── customer.py       
│   │   ├── mechanic.py       
│   │   ├── service.py        
│   │   └── ...               
│   ├── routes/               # API route handlers
│   │   ├── auth.py           
│   │   ├── bookings.py       
│   │   ├── customer.py       
│   │   ├── mechanic.py       
│   │   ├── service.py        
│   │   └── ...              
│   ├── schemas/              # Pydantic schemas
│   │   ├── bookings.py       
│   │   ├── customer.py       
│   │   └── ...               
│   ├── services/             # Business logic
│   │   ├── auth.py           
│   │   ├── bookings.py       
│   │   ├── crud.py           
│   │   ├── notification.py   
│   │   ├── payment.py     
│   │   └── ...             
│   ├── templates/            # HTML templates
│   │   ├── email/            # Email templates
│   │   └── ...               
│   ├── utilities/            # Utility functions
│   │   ├── data_utils.py     
│   │   ├── scopes.py         
│   │   ├── seed.py           
│   │   └── seed_data.py      
│   └── revare_v1.py          # API v1 router
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
└── README.md
```

### 13.2 Best Practices

- **Dependency Injection**: Use FastAPI's `Depends` for service injection
- **Type Hints**: Type hints throughout codebase for better IDE support
- **Comprehensive Error Handling**: Global exception handler for consistent error responses
- **Async/Await**: Use async operations for all I/O operations
- **Database Transactions**: Use transactions for multi-step operations
- **Input Validation**: Pydantic models for all inputs
- **Output Serialization**: Pydantic models for all outputs
- **API Versioning**: Version APIs from start (`/api/v1/`)
- **Database Migrations**: Use Alembic for all schema changes
- **Documentation**: Docstrings for all functions and classes
- **Testing**: Unit tests for business logic, integration tests for APIs
- **Code Organization**: Separate routes, services, and models
- **Security**: Always validate permissions and user access
- **Logging**: Log important operations and errors

### 13.3 Database Best Practices

- **Transactions**: Use database transactions for atomic operations
- **Eager Loading**: Use `selectinload` to prevent N+1 queries
- **Indexing**: Add indexes for frequently queried fields
- **Connection Pooling**: Configure appropriate pool size
- **Query Optimization**: Use EXPLAIN to analyze query performance
- **Migration Strategy**: Always test migrations on staging first

### 13.4 API Best Practices

- **RESTful Design**: Follow REST principles for resource naming
- **HTTP Status Codes**: Use appropriate status codes (200, 201, 400, 401, 403, 404, 500)
- **Error Messages**: Provide clear, actionable error messages
- **Pagination**: Implement pagination for list endpoints
- **Filtering**: Support filtering and sorting for list endpoints
- **Versioning**: Version APIs to allow backward compatibility
- **Documentation**: Keep API documentation up to date

## 14. Integration Points

### 14.1 External Services

- **Razorpay Payment Gateway**: 
  - Payment order creation
  - Payment verification
  - Webhook handling
  - Refund processing

- **Email Service (SMTP)**:
  - Booking confirmation emails
  - Progress update emails
  - Invoice emails
  - Query response emails

### 14.2 Internal Services

- **Authentication Service**: JWT token validation
- **Notification Service**: Email sending
- **Payment Service**: Payment processing
- **Backup Service**: Database backup and recovery
- **Content Service**: Dynamic content management

## 15. Data Flow Patterns

### 15.1 Booking Lifecycle

1. **Booked**: Customer creates booking
2. **Pickup**: Mechanic assigned for pickup
3. **Received**: Vehicle received at service center
4. **Analysis**: Mechanic creates analysis report
5. **Analysed**: Analysis validated, customer confirms services
6. **In Progress**: Services being performed
7. **Completed**: All services completed
8. **Out for Delivery**: Vehicle ready for delivery
9. **Delivered**: Vehicle delivered to customer

### 15.2 Payment Flow

1. **Pending**: Payment created (online or offline)
2. **Success**: Payment verified and confirmed
3. **Failed**: Payment verification failed

### 15.3 Service Selection Flow

1. Customer books services (estimated prices)
2. Mechanic analyzes vehicle and provides price quotes
3. Customer selects services to proceed with
4. Payment processed (online or offline)
5. Services confirmed and booking status updated to 'in-progress'

## 16. Error Handling Strategy

### 16.1 Error Types

- **HTTP Exceptions**: 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 500 (Internal Server Error)
- **Database Exceptions**: IntegrityError, OperationalError
- **Validation Exceptions**: Pydantic validation errors
- **Business Logic Exceptions**: Custom business rule violations

### 16.2 Global Exception Handler

All exceptions are caught by global exception handler middleware and returned in consistent format:

```json
{
  "detail": "Error message"
}
```

## 17. Backup & Recovery Strategy

### 17.1 Backup Types

- **PostgreSQL Backup**: SQL dump of all tables
- **MongoDB Backup**: JSON export of all collections
- **Full Backup**: Both PostgreSQL and MongoDB backups

### 17.2 Backup Schedule

- **Automated Backups**: Daily backups (configurable)
- **Manual Backups**: On-demand backups before major changes
- **Backup Retention**: 30 days (configurable)

### 17.3 Recovery Process

1. List available backups
2. Select backup to restore
3. Verify backup integrity
4. Restore database from backup
5. Verify data integrity
6. Test application functionality

## 18. Appendix

### 18.1 Acronyms

- **RBAC**: Role-Based Access Control
- **JWT**: JSON Web Token
- **API**: Application Programming Interface
- **ORM**: Object-Relational Mapping
- **ODM**: Object-Document Mapping
- **CRUD**: Create, Read, Update, Delete
- **GST**: Goods and Services Tax
- **COD**: Cash on Delivery
- **SMTP**: Simple Mail Transfer Protocol
- **HTTPS**: Hypertext Transfer Protocol Secure
- **CORS**: Cross-Origin Resource Sharing
- **XSS**: Cross-Site Scripting

### 18.2 Glossary

- **Booking**: A service appointment for a vehicle
- **Booked Service**: A service included in a booking
- **Booking Assignment**: Assignment of a mechanic to a booking
- **Booking Progress**: Progress update for a booking
- **Booking Analysis**: Analysis report with price quotes
- **Booking Recommendation**: Recommended service with price quote
- **Scope**: Permission required to access a resource
- **Token**: JWT token for authentication
- **Refresh Token**: Long-lived token for refreshing access tokens
- **Access Token**: Short-lived token for API access

