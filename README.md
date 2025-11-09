# RevCare - Vehicle Service Management Application

A comprehensive web-based Vehicle Service Management System that streamlines service booking, tracking, invoicing, and management for customers, service staff, and administrators.

## Problem Statement

Managing vehicle servicing manually is time-consuming, prone to errors, and lacks transparency. Customers often face difficulties in booking service appointments, tracking service progress, and receiving timely updates. On the other side, service centers struggle with handling service records and staff allocation efficiently.

RevCare bridges this gap by providing a centralized platform for customers, service staff, and administrators to streamline service booking, tracking, invoicing, and management.

## Features

### Core Functionalities
- **User Management**: Registration and login for customers, mechanics, and admins with role-based access control
- **Service Booking & Scheduling**: Customers can book vehicle service appointments with date/time selection
- **Service Tracking**: Real-time service progress tracking with status updates (Pickup → Analysis → In Progress → Completed → Delivery)
- **Vehicle Management**: Add/manage multiple vehicles with complete service history
- **Billing & Payments**: Auto-generated invoices with support for online (Razorpay) and offline payments
- **Notifications**: Email notifications for booking confirmations, progress updates, invoices, and query responses
- **Service Analysis**: Mechanics can provide analysis reports with price quotes and recommendations
- **Progress Updates**: Mechanics can update service progress with images and descriptions
- **Customer Queries**: Query management system with admin responses
- **Content Management**: Dynamic content management for app content
- **Backup & Recovery**: Database backup and restore functionality for PostgreSQL and MongoDB
- **GST Management**: Configurable GST percentage management

### Role-Based Features

#### Customer
- Register/Login
- Add/manage vehicles
- Book/cancel service appointments
- Track service progress in real-time
- View service history
- Make payments (online/offline) & download invoices
- Receive email notifications
- Submit queries
- Add services to cart and favourites
- Review and rate services

#### Mechanic
- Login & view assigned services
- Update service status (Pickup, Analysis, In Progress, Drop)
- Create analysis reports with price quotes
- Update service progress with images
- Receive service assignments
- Handle cash on delivery payments

#### Admin
- Manage users (customers, mechanics, admins)
- Assign mechanics to bookings
- Validate progress updates and analysis reports
- View all bookings with action indicators
- Manage services, service categories, and pricing
- Manage content and GST settings
- View notification logs
- Create and restore database backups
- Respond to customer queries

## Technology Stack

- **Python**: 3.11+
- **FastAPI**: 0.120.0 - Modern, fast web framework for building APIs
- **PostgreSQL**: Primary database for structured data (async with SQLAlchemy)
- **MongoDB**: NoSQL database for queries, content, and GST management
- **SQLAlchemy**: 2.0.44 - Async ORM for database operations
- **Pydantic**: 2.12.3 - Data validation using Python type annotations
- **JWT (python-jose)**: Authentication and authorization
- **Argon2**: Password hashing
- **Razorpay**: Payment gateway integration
- **FastMail**: Email notification service
- **Motor**: Async MongoDB driver
- **Alembic**: Database migrations (optional)
- **Uvicorn**: ASGI server

## Prerequisites

- Python 3.11 or higher
- PostgreSQL 12+ (for primary database)
- MongoDB 4.4+ (for queries, content, GST)
- pip or poetry (package manager)
- Virtual environment tool (venv, virtualenv, or conda)

## Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/SKShanthakumar/revCare-phase2.git
cd revCare-phase2
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

#### PostgreSQL Setup

```bash
# Create PostgreSQL database
createdb revcare
```

#### MongoDB Setup

```bash
# Install MongoDB (if not installed)
# On macOS
brew install mongodb-community

# On Ubuntu/Debian
sudo apt-get install mongodb

# Start MongoDB service
# On macOS
brew services start mongodb-community
# On Linux
sudo systemctl start mongod
```

### 5. Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 6. Run Database Migrations (Optional)

The application uses SQLAlchemy to create tables automatically on startup. If you need to use Alembic for migrations:

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### 7. Seed Database (Optional)

Uncomment the seed function in `main.py` to populate initial data:

```python
# In main.py, uncomment:
await run_seed()
```

This will create:
- Default roles (admin, mechanic, customer)
- Sample users (admin, customers, mechanic)
- Service categories and services
- Areas, manufacturers, car classes, fuel types
- Statuses, assignment types, timeslots
- Payment methods
- Notification categories

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
POSTGRESQL_URL=postgresql+asyncpg://username:password@localhost:5432/revcare_db
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=revcare

# Authentication
SECRET_KEY=your-secret-key-here-change-in-production
REFRESH_SECRET_KEY=your-refresh-secret-key-here-change-in-production
HASH_ALGORITHM=argon2
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Payment Gateway (Razorpay)
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret

# Email Configuration
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=your-email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_FROM_NAME=Revcare
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
USE_CREDENTIALS=True
VALIDATE_CERTS=True

# Backup Configuration (Optional)
BACKUP_DIR=backups
MAX_BACKUP_SIZE_MB=500
AUTO_DELETE_OLD_BACKUPS=False
MAX_BACKUP_AGE_DAYS=30
```

### Environment Variables Explanation

- **POSTGRESQL_URL**: PostgreSQL database connection string (asyncpg driver)
- **MONGODB_URI**: MongoDB connection string
- **MONGODB_DB**: MongoDB database name
- **SECRET_KEY**: JWT access token secret key (keep secure)
- **REFRESH_SECRET_KEY**: JWT refresh token secret key (keep secure)
- **HASH_ALGORITHM**: Password hashing algorithm (argon2 recommended)
- **ACCESS_TOKEN_EXPIRE_MINUTES**: Access token expiration time in minutes
- **REFRESH_TOKEN_EXPIRE_DAYS**: Refresh token expiration time in days
- **RAZORPAY_KEY_ID**: Razorpay API key ID
- **RAZORPAY_KEY_SECRET**: Razorpay API key secret
- **MAIL_***: Email server configuration for sending notifications

## Running the Application

### Development Mode

```bash
# Using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
# Using uvicorn with workers
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Access the Application

- **API Base URL**: `http://localhost:8000`
- **API Documentation (Swagger UI)**: `http://localhost:8000/docs`
- **API Documentation (ReDoc)**: `http://localhost:8000/redoc`
- **API v1 Endpoints**: `http://localhost:8000/api/v1`

## API Documentation

### Interactive API Documentation

Once the application is running, you can access:

- **Swagger UI**: `http://localhost:8000/docs` - Interactive API documentation with try-it-out feature
- **ReDoc**: `http://localhost:8000/redoc` - Alternative API documentation

### Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Login**: POST `/api/v1/auth/login`
   - Request: `username` (phone number) and `password` as form data
   - Response: `access_token` and `refresh_token` (stored in HTTP-only cookie)

2. **Using Token**: Include the access token in the Authorization header:
   ```
   Authorization: Bearer <access_token>
   ```

3. **Refresh Token**: POST `/api/v1/auth/refresh`
   - Automatically uses refresh token from cookie
   - Returns new access token

4. **Logout**: POST `/api/v1/auth/logout`
   - Blacklists both access and refresh tokens

### Token Expiration

- **Access Token**: 30 minutes (configurable)
- **Refresh Token**: 7 days (configurable)

## Project Structure

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

## API Endpoints (Quick Reference)

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - User logout

### Customers
- `GET /api/v1/customers/` - Get customers
- `POST /api/v1/customers/` - Create customer
- `PUT /api/v1/customers/{id}` - Update customer
- `DELETE /api/v1/customers/{id}` - Delete customer
- `POST /api/v1/customers/cart/{service_id}` - Add to cart
- `DELETE /api/v1/customers/cart/{service_id}` - Remove from cart
- `POST /api/v1/customers/favourite/{service_id}` - Add to favourites
- `DELETE /api/v1/customers/favourite/{service_id}` - Remove from favourites

### Bookings
- `POST /api/v1/bookings/` - Create booking
- `GET /api/v1/bookings/customer` - Get customer bookings
- `GET /api/v1/bookings/{booking_id}` - Get booking details
- `PUT /api/v1/bookings/{booking_id}/confirm-services` - Confirm services
- `PUT /api/v1/bookings/{booking_id}/cancel` - Cancel booking
- `GET /api/v1/bookings/admin/dashboard` - Admin dashboard
- `POST /api/v1/bookings/admin/assign` - Assign mechanic
- `POST /api/v1/bookings/mechanic/progress` - Create progress update
- `POST /api/v1/bookings/mechanic/analysis` - Create analysis

### Services
- `GET /api/v1/services/` - Get services
- `POST /api/v1/services/` - Create service
- `PUT /api/v1/services/{id}` - Update service
- `DELETE /api/v1/services/{id}` - Delete service
- `GET /api/v1/services/category` - Get service categories
- `GET /api/v1/services/review/{service_id}` - Get service reviews
- `POST /api/v1/services/review` - Create review

### Cars
- `GET /api/v1/car/models` - Get car models
- `GET /api/v1/car/` - Get customer cars
- `POST /api/v1/car/` - Add customer car
- `PUT /api/v1/car/{id}` - Update customer car
- `DELETE /api/v1/car/{id}` - Delete customer car

### Payments
- `POST /api/v1/payment/verify` - Verify payment (webhook)
- `POST /api/v1/payment/cash-on-delivery/{booking_id}` - Process COD
- `POST /api/v1/payment/verify-cod` - Verify COD payment

### Admin
- `GET /api/v1/admins/` - Get admins
- `POST /api/v1/admins/` - Create admin
- `PUT /api/v1/admins/{id}` - Update admin
- `DELETE /api/v1/admins/{id}` - Delete admin

### Mechanics
- `GET /api/v1/mechanics/` - Get mechanics
- `POST /api/v1/mechanics/` - Create mechanic
- `PUT /api/v1/mechanics/{id}` - Update mechanic
- `DELETE /api/v1/mechanics/{id}` - Delete mechanic

### Content Management
- `GET /api/v1/content/{content_id}` - Get content
- `PUT /api/v1/content/` - Update content

### GST Management
- `PUT /api/v1/gst/` - Update GST percentage

### Queries
- `POST /api/v1/queries/` - Create query
- `GET /api/v1/queries/` - Get all queries
- `PUT /api/v1/queries/{query_id}/respond` - Respond to query

### Backup & Recovery
- `POST /api/v1/backup/create` - Create backup
- `GET /api/v1/backup/list` - List backups
- `POST /api/v1/backup/restore` - Restore backup
- `DELETE /api/v1/backup/delete/{backup_name}` - Delete backup

For detailed endpoint documentation, visit `/docs` when the application is running.

## Authentication & Authorization

### Getting JWT Token

1. **Login**:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=9841385379&password=your_password"
   ```

2. **Response**:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type": "bearer"
   }
   ```

### Using Token in Requests

Include the access token in the Authorization header:

```bash
curl -X GET "http://localhost:8000/api/v1/bookings/customer" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Role-Based Access Control (RBAC)

The application uses role-based access control with the following roles:

- **Admin** (role_id: 1): Full access to all endpoints
- **Mechanic** (role_id: 2): Access to assigned bookings, progress updates, analysis
- **Customer** (role_id: 3): Access to own bookings, vehicles, payments

Each endpoint requires specific permissions (scopes) that are checked during token validation.

## Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

### Test Structure

```
tests/
├── test_auth.py
├── test_bookings.py
├── test_services.py
└── ...
```

## Common Issues & Troubleshooting

### Database Connection Errors

**Issue**: `Could not connect to database`

**Solution**:
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check connection string in `.env` file
- Ensure database exists: `psql -U postgres -l`
- Check firewall settings

### Migration Issues

**Issue**: `Table already exists`

**Solution**:
- Drop and recreate database (development only)
- Or use Alembic migrations for production

### Port Conflicts

**Issue**: `Address already in use`

**Solution**:
- Change port in uvicorn command: `--port 8001`
- Or kill process using port 8000: `lsof -ti:8000 | xargs kill`

### MongoDB Connection Issues

**Issue**: `Cannot connect to MongoDB`

**Solution**:
- Verify MongoDB is running: `sudo systemctl status mongod`
- Check MongoDB URI in `.env` file
- Ensure MongoDB is accessible: `mongosh`

### Email Not Sending

**Issue**: Emails not being sent

**Solution**:
- Verify email credentials in `.env`
- For Gmail, use App Password instead of regular password
- Check SMTP server settings
- Verify firewall allows SMTP connections

### Token Validation Errors

**Issue**: `Invalid token` or `Token expired`

**Solution**:
- Check token expiration settings in `.env`
- Ensure token is included in Authorization header
- Verify secret keys are correct
- Check if token is blacklisted (after logout)

## Development Guidelines

### Code Style

- Follow PEP 8 Python style guide
- Use type hints for function parameters and return types
- Write docstrings for all functions and classes
- Use async/await for database operations

### Branch Naming

- `feature/feature-name` - New features
- `bugfix/bug-description` - Bug fixes
- `hotfix/critical-fix` - Critical production fixes
- `refactor/refactor-description` - Code refactoring

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -m 'feat: add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a pull request

## Modules & Sub-Modules

### 1. User Management
- User Registration & Authentication
- Role-Based Access Control (RBAC)
- Token Management (JWT)

### 2. Service Booking
- Book New Service
- Reschedule/Cancel Booking
- Assign Booking to Mechanic (Admin)

### 3. Service Tracking
- Update Service Status (Mechanic)
- Real-Time Service Tracking (Customer)
- Progress Updates with Images

### 4. Vehicle Management
- Add/Edit/Delete Vehicle
- View Vehicle Service History
- Manage Multiple Vehicles

### 5. Billing & Payments
- Invoice Generation
- Online/Offline Payment Processing
- Payment History
- Razorpay Integration

### 6. Notifications
- Email Notifications (Booking Confirmation, Progress Updates, Invoices, Query Responses)
- Service Reminders
- Completion Alerts

### 7. Service Analysis
- Analysis Reports with Price Quotes
- Service Recommendations
- Admin Validation

### 8. Content Management
- Dynamic Content Management
- GST Management
- Query Management

### 9. Backup & Recovery
- PostgreSQL Backup
- MongoDB Backup
- Backup Restoration
- Backup Management

## Future Enhancements

1. **Mobile App Integration** - Dedicated Android/iOS app for customers and staff with push notifications
2. **Chatbot Support** - LLM-based AI chatbot for customer queries, service suggestions, booking assistance
3. **AI-Powered Predictive Maintenance** - Predict when a vehicle might need servicing based on history and usage
4. **Multi-Language Support** - Support for regional languages for better accessibility
5. **Third-Party Integrations** - Payment gateways, CRM systems, accounting software (QuickBooks, Tally)
6. **Geo-Location Services** - Real-time vehicle pickup & drop tracking
7. **Loyalty & Rewards System** - Points or discounts for frequent customers
8. **Dynamic Pricing & Service Packages** - Personalized offers, seasonal discounts, bundled service packages
9. **SMS Notifications** - SMS alerts in addition to email notifications
10. **Advanced Analytics** - Dashboard with charts and graphs for business insights
