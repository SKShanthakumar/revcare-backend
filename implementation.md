# Car Service Booking System - Complete Implementation Guide

## Overview
This document provides a comprehensive guide to the booking management system for the car service application. The system handles the complete lifecycle of a booking from initial creation to final delivery.

## Table of Contents
1. [Setup](#setup)
2. [Database Schema](#database-schema)
3. [API Endpoints](#api-endpoints)
4. [Workflow](#workflow)
5. [Status Management](#status-management)
6. [User Roles](#user-roles)
7. [Frontend Integration](#frontend-integration)

---

## Setup

### 1. Add Models to `app/models/__init__.py`
```python
from .booking import Booking, BookedService, BookingRecommendation, BookingAssignment, BookingProgress, BookingAnalysis
```

### 2. Add Schemas to `app/schemas/__init__.py`
```python
from .booking import (
    BookingCreate, BookingResponse, MechanicAssignmentCreate,
    MechanicAssignmentResponse, BookingProgressCreate, BookingProgressUpdate,
    BookingProgressResponse, BookingAnalysisCreate, BookingAnalysisUpdate,
    BookingAnalysisResponse, CustomerServiceSelection, BookingProgressWithCompletion,
    BookedServiceResponse, AdminBookingDashboard, CustomerBookingView
)
```

### 3. Add Routes to `app/main.py`
```python
from app.routes import booking

app.include_router(booking.router, prefix="/api/v1/bookings", tags=["Bookings"])
```

### 4. Seed Required Data
Run the following SQL to populate required statuses and assignment types:

```sql
-- Insert required statuses
INSERT INTO status (name) VALUES
('booked'), ('pickup'), ('received'), ('analysis'), ('analysed'),
('in-progress'), ('completed'), ('out for delivery'), ('delivered'),
('cancelled'), ('assigned'), ('confirmed'), ('rejected')
ON CONFLICT (name) DO NOTHING;

-- Insert required assignment types
INSERT INTO assignment_types (name) VALUES
('pickup'), ('drop'), ('service'), ('analysis')
ON CONFLICT (name) DO NOTHING;
```

---

## Database Schema

### Key Tables

#### 1. `bookings`
Main booking record with customer, car, addresses, dates, and status.

#### 2. `booked_services`
Services included in a booking with pricing and completion status.

#### 3. `booking_recommendations`
Additional services recommended by mechanic during analysis.

#### 4. `booking_assignment`
History of mechanic assignments to bookings.

#### 5. `booking_progress`
Progress updates from mechanics during service execution.

#### 6. `booking_analysis`
Final analysis report with price quotes and recommendations.

---

## API Endpoints

### Customer Endpoints

#### POST `/api/v1/bookings/`
Create a new booking.
- **Scope**: `WRITE:BOOKINGS`
- **Body**: `BookingCreate`
- **Returns**: `BookingResponse`

#### GET `/api/v1/bookings/customer`
Get all bookings for logged-in customer.
- **Scope**: `READ:BOOKINGS`
- **Returns**: `List[CustomerBookingView]`

#### PUT `/api/v1/bookings/{booking_id}/confirm-services`
Confirm services after analysis.
- **Scope**: `UPDATE:BOOKINGS`
- **Body**: `CustomerServiceSelection`
- **Returns**: JSON message

#### PUT `/api/v1/bookings/{booking_id}/cancel`
Cancel a booking.
- **Scope**: `UPDATE:BOOKINGS`
- **Returns**: JSON message

### Admin Endpoints

#### GET `/api/v1/bookings/admin/dashboard`
Get all bookings with action indicators.
- **Scope**: `READ:BOOKINGS`, `READ:BOOKING_ASSIGNMENT`
- **Query Params**: `status_filter` (optional)
- **Returns**: `List[AdminBookingDashboard]`

#### GET `/api/v1/bookings/admin/{booking_id}`
Get detailed booking information.
- **Scope**: `READ:BOOKINGS`
- **Returns**: `BookingResponse`

#### GET `/api/v1/bookings/admin/{booking_id}/services`
Get all services for a booking.
- **Scope**: `READ:BOOKED_SERVICES`
- **Returns**: `List[BookedServiceResponse]`

#### POST `/api/v1/bookings/admin/assign`
Assign mechanic to a booking.
- **Scope**: `WRITE:BOOKING_ASSIGNMENT`
- **Body**: `MechanicAssignmentCreate`
- **Returns**: `MechanicAssignmentResponse`

#### PUT `/api/v1/bookings/admin/progress/{progress_id}`
Edit progress update.
- **Scope**: `UPDATE:BOOKING_PROGRESS`
- **Body**: `BookingProgressUpdate`
- **Returns**: `BookingProgressResponse`

#### POST `/api/v1/bookings/admin/progress/{progress_id}/validate`
Validate and approve progress update.
- **Scope**: `UPDATE:BOOKING_PROGRESS`
- **Returns**: JSON message

#### PUT `/api/v1/bookings/admin/analysis/{booking_id}`
Edit analysis report.
- **Scope**: `UPDATE:BOOKING_ANALYSIS`
- **Body**: `BookingAnalysisUpdate`
- **Returns**: `BookingAnalysisResponse`

#### POST `/api/v1/bookings/admin/analysis/{booking_id}/validate`
Validate and approve analysis report.
- **Scope**: `UPDATE:BOOKING_ANALYSIS`
- **Returns**: JSON message

### Mechanic Endpoints

#### GET `/api/v1/bookings/mechanic/assignments`
Get all assignments for logged-in mechanic.
- **Scope**: `READ:BOOKING_ASSIGNMENT`
- **Returns**: `List[MechanicAssignmentResponse]`

#### POST `/api/v1/bookings/mechanic/progress`
Create progress update (pickup/drop).
- **Scope**: `WRITE:BOOKING_PROGRESS`
- **Body**: `BookingProgressCreate`
- **Returns**: `BookingProgressResponse`

#### POST `/api/v1/bookings/mechanic/progress-with-completion`
Create progress update with service completion.
- **Scope**: `WRITE:BOOKING_PROGRESS`
- **Body**: `BookingProgressWithCompletion`
- **Returns**: `BookingProgressResponse`

#### POST `/api/v1/bookings/mechanic/analysis`
Create analysis report.
- **Scope**: `WRITE:BOOKING_ANALYSIS`
- **Body**: `BookingAnalysisCreate`
- **Returns**: `BookingAnalysisResponse`

---

## Workflow

### Step 1: Customer Books Service
- Customer selects car, services, addresses, and dates
- System creates booking in `booked` status
- All services added to `booked_services` with estimated prices

### Step 2: Admin Assigns Mechanic for Pickup
- Admin views bookings in `booked` status
- Assigns mechanic with assignment type `pickup`
- Booking status changes to `pickup`

### Step 3: Mechanic Picks Up Car
- Mechanic receives car and brings to service center
- Creates progress update
- Booking status changes to `received`
- Assignment status changes to `completed`

### Step 4: Admin Validates Pickup
- Admin reviews progress update
- Can edit if needed
- Validates and sends to customer
- Progress validated flag set to `true`

### Step 5: Admin Assigns Mechanic for Analysis
- Admin assigns mechanic with assignment type `analysis`
- Booking status changes to `analysis`

### Step 6: Mechanic Performs Analysis
- Mechanic analyzes car
- Creates analysis report with:
  - Final price quotes for booked services
  - Recommended additional services (if any)
- Booking status changes to `analysed`
- Assignment status changes to `completed`

### Step 7: Admin Validates Analysis
- Admin reviews analysis report
- Can edit if needed
- Validates and sends to customer
- Analysis validated flag set to `true`

### Step 8: Customer Confirms Services
- Customer views price quotes and recommendations
- Selects which services to proceed with
- Rejected services marked with `rejected` status
- Confirmed services marked with `confirmed` status
- Accepted recommendations added to `booked_services`
- Booking status changes to `in-progress`

### Step 9: Admin Assigns Mechanic for Service
- Admin assigns mechanic with assignment type `service`
- Mechanic performs services
- Creates progress updates marking services as completed

### Step 10: Admin Validates Service Progress
- Admin reviews progress updates
- Validates and sends to customer
- If all services completed, booking status changes to `completed`
- If services incomplete, admin assigns mechanic again

### Step 11: Admin Assigns Mechanic for Drop
- Admin assigns mechanic with assignment type `drop`
- Booking status changes to `out for delivery`

### Step 12: Mechanic Drops Car
- Mechanic delivers car to customer
- Creates progress update
- Booking status changes to `delivered`
- Assignment status changes to `completed`

### Step 13: Admin Final Validation
- Admin validates drop progress
- Customer receives final notification

---

## Status Management

### Internal Statuses
1. **booked** - Initial state after customer booking
2. **pickup** - Mechanic assigned for pickup
3. **received** - Car received at service center
4. **analysis** - Mechanic assigned for analysis
5. **analysed** - Analysis completed, waiting for customer approval
6. **in-progress** - Customer approved, services being performed
7. **completed** - All services completed
8. **out for delivery** - Mechanic assigned for drop
9. **delivered** - Car delivered to customer
10. **cancelled** - Booking cancelled by customer

### Customer-Facing Statuses
- **booked**: [booked, pickup, received, analysis]
- **analysed**: [analysed]
- **in-progress**: [in-progress]
- **completed**: [completed, out for delivery]
- **delivered**: [delivered]
- **cancelled**: [cancelled]

### Admin Action Indicators
The `action_required` field in admin dashboard indicates:
- **assign**: Admin needs to assign a mechanic
- **validate**: Admin needs to validate and approve update
- **waiting**: Waiting for customer approval
- **none**: No action required

---

## User Roles

### Customer
- Create bookings
- View own bookings (simplified status)
- Confirm services after analysis
- Cancel bookings

### Admin
- View all bookings (detailed)
- Assign mechanics
- Validate progress updates
- Validate analysis reports
- Edit updates before validation

### Mechanic
- View assigned bookings
- Create progress updates
- Create analysis reports
- Mark services as completed

---

## Frontend Integration

### Customer Dashboard
```javascript
// Fetch customer bookings
GET /api/v1/bookings/customer

// Response includes grouped_status for simplified display
{
  "booking_id": 1,
  "car_model": "Swift",
  "car_reg": "TN01AB1234",
  "grouped_status": "booked",  // or "analysed", "in-progress", etc.
  "booked_services": [...],
  "total_estimated_price": 5000.00
}
```

### Admin Dashboard
```javascript
// Fetch all bookings with action indicators
GET /api/v1/bookings/admin/dashboard?status_filter=booked

// Response includes action_required field
{
  "booking_id": 1,
  "customer_name": "John Doe",
  "status": "booked",
  "action_required": "assign",  // Shows what admin should do
  "latest_progress": null,
  "latest_analysis": null
}

// Based on action_required:
// - "assign": Show assign mechanic button
// - "validate": Show validate button
// - "waiting": Show waiting for approval message
// - "none": No action needed
```

### Mechanic Dashboard
```javascript
// Fetch mechanic assignments
GET /api/v1/bookings/mechanic/assignments

// Submit progress update
POST /api/v1/bookings/mechanic/progress
{
  "booking_id": 1,
  "description": "Car picked up successfully",
  "images": ["url1", "url2"]
}
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:
- **200**: Success
- **400**: Bad request (validation error)
- **403**: Forbidden (insufficient permissions)
- **404**: Resource not found
- **500**: Internal server error

Error responses follow this format:
```json
{
  "detail": "Error message here"
}
```

---

## Testing Checklist

- [ ] Customer can create booking with new addresses
- [ ] Customer can create booking with existing addresses
- [ ] Customer can view only their bookings
- [ ] Customer sees simplified status grouping
- [ ] Admin can view all bookings
- [ ] Admin sees correct action indicators
- [ ] Admin can assign mechanics
- [ ] Admin can validate progress
- [ ] Admin can validate analysis
- [ ] Mechanic can view assignments
- [ ] Mechanic can create progress updates
- [ ] Mechanic can create analysis
- [ ] Customer can confirm services
- [ ] Customer can cancel booking
- [ ] Status transitions work correctly
- [ ] Permissions are enforced correctly

---

## Common Issues & Solutions

### Issue: Status not found
**Solution**: Ensure all required statuses are seeded in the database.

### Issue: Assignment type not found
**Solution**: Ensure all assignment types are seeded in the database.

### Issue: Address validation fails
**Solution**: Ensure address belongs to the customer or new address data is provided.

### Issue: Mechanic can't see assignments
**Solution**: Verify mechanic_id starts with "MEC" and scopes are correct.

---

## Future Enhancements

1. **Notifications**: Integrate with notification system for status updates
2. **Payments**: Link bookings with payment processing
3. **Reviews**: Allow customers to review services after delivery
4. **Real-time Updates**: WebSocket support for live status updates
5. **Analytics**: Dashboard with booking statistics and trends