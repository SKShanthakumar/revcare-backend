# Booking API Testing Guide

## Prerequisites
- Ensure all tables are created
- Run the seed script to populate statuses and assignment types
- Have test users (customer, admin, mechanic) with proper roles and permissions
- Have test data for cars, services, addresses, etc.

---

## Test Sequence

### 1. Customer Creates Booking

**Endpoint**: `POST /api/v1/bookings/`

**Headers**:
```
Authorization: Bearer <customer_token>
```

**Request Body**:
```json
{
  "customer_car_id": 1,
  "pickup_address_id": 1,
  "drop_address_id": 2,
  "pickup_date": "2025-11-10",
  "drop_date": "2025-11-15",
  "pickup_timeslot_id": 1,
  "drop_timeslot_id": 2,
  "service_price": {
    "1": 2500.00,
    "2": 3500.00
  }
}
```

**Expected Response**:
```json
{
  "id": 1,
  "customer_id": "CST000001",
  "car_reg_number": "TN01AB1234",
  "status_id": 1,
  "pickup_address_id": 1,
  "pickup_date": "2025-11-10",
  ...
}
```

**Alternative with New Address**:
```json
{
  "customer_car_id": 1,
  "pickup_address": {
    "label": "Home",
    "line1": "123 Main St",
    "line2": "Apt 4B",
    "area_id": 1
  },
  "drop_address_id": 2,
  "pickup_date": "2025-11-10",
  "drop_date": "2025-11-15",
  "pickup_timeslot_id": 1,
  "drop_timeslot_id": 2,
  "service_price": {
    "1": 2500.00
  }
}
```

---

### 2. Customer Views Bookings

**Endpoint**: `GET /api/v1/bookings/customer`

**Headers**:
```
Authorization: Bearer <customer_token>
```

**Expected Response**:
```json
[
  {
    "booking_id": 1,
    "car_model": "Swift",
    "car_reg": "TN01AB1234",
    "grouped_status": "booked",
    "pickup_date": "2025-11-10",
    "drop_date": "2025-11-15",
    "created_at": "2025-11-06T10:30:00",
    "booked_services": [
      {
        "service_id": 1,
        "service_name": "Oil Change",
        "est_price": 2500.00,
        "final_price": null,
        "status": "booked",
        "completed": false
      }
    ],
    "total_estimated_price": 2500.00,
    "total_final_price": null
  }
]
```

---

### 3. Admin Views Dashboard

**Endpoint**: `GET /api/v1/bookings/admin/dashboard`

**Headers**:
```
Authorization: Bearer <admin_token>
```

**Expected Response**:
```json
[
  {
    "booking_id": 1,
    "customer_name": "John Doe",
    "car_model": "Swift",
    "car_reg": "TN01AB1234",
    "status": "booked",
    "status_id": 1,
    "pickup_date": "2025-11-10",
    "created_at": "2025-11-06T10:30:00",
    "action_required": "assign",
    "latest_progress": null,
    "latest_analysis": null,
    "latest_assignment": null
  }
]
```

---

### 4. Admin Assigns Mechanic for Pickup

**Endpoint**: `POST /api/v1/bookings/admin/assign`

**Headers**:
```
Authorization: Bearer <admin_token>
```

**Request Body**:
```json
{
  "mechanic_id": "MEC000001",
  "booking_id": 1,
  "assignment_type_id": 1
}
```

**Note**: Get assignment_type_id for "pickup" from assignment_types table

**Expected Response**:
```json
{
  "id": 1,
  "mechanic_id": "MEC000001",
  "booking_id": 1,
  "assignment_type_id": 1,
  "status_id": 11,
  "assigned_at": "2025-11-06T11:00:00"
}
```

**Result**: Booking status changes to "pickup"

---

### 5. Mechanic Views Assignments

**Endpoint**: `GET /api/v1/bookings/mechanic/assignments`

**Headers**:
```
Authorization: Bearer <mechanic_token>
```

**Expected Response**:
```json
[
  {
    "id": 1,
    "mechanic_id": "MEC000001",
    "booking_id": 1,
    "assignment_type_id": 1,
    "status_id": 11,
    "assigned_at": "2025-11-06T11:00:00"
  }
]
```

---

### 6. Mechanic Creates Progress Update (Pickup)

**Endpoint**: `POST /api/v1/bookings/mechanic/progress`

**Headers**:
```
Authorization: Bearer <mechanic_token>
```

**Request Body**:
```json
{
  "booking_id": 1,
  "description": "Car picked up successfully from customer address. No visible damage observed.",
  "images": [
    "https://example.com/images/pickup1.jpg",
    "https://example.com/images/pickup2.jpg"
  ]
}
```

**Expected Response**:
```json
{
  "id": 1,
  "mechanic_id": "MEC000001",
  "booking_id": 1,
  "description": "Car picked up successfully...",
  "images": ["https://example.com/images/pickup1.jpg", "..."],
  "status_id": 2,
  "validated": false,
  "timestamp": "2025-11-06T12:00:00"
}
```

**Result**: 
- Booking status changes to "received"
- Assignment status changes to "completed"

---

### 7. Admin Validates Progress

**Endpoint**: `POST /api/v1/bookings/admin/progress/1/validate`

**Headers**:
```
Authorization: Bearer <admin_token>
```

**Expected Response**:
```json
{
  "message": "Progress validated and sent to customer"
}
```

**Result**: Progress validated flag set to true

---

### 8. Admin Assigns Mechanic for Analysis

**Endpoint**: `POST /api/v1/bookings/admin/assign`

**Headers**:
```
Authorization: Bearer <admin_token>
```

**Request Body**:
```json
{
  "mechanic_id": "MEC000002",
  "booking_id": 1,
  "assignment_type_id": 4
}
```

**Note**: assignment_type_id = 4 for "analysis"

**Result**: Booking status changes to "analysis"

---

### 9. Mechanic Creates Analysis

**Endpoint**: `POST /api/v1/bookings/mechanic/analysis`

**Headers**:
```
Authorization: Bearer <mechanic_token>
```

**Request Body**:
```json
{
  "booking_id": 1,
  "description": "Completed thorough inspection. Oil filter needs replacement. Brake pads at 40% wear.",
  "recommendation": "Recommend brake pad replacement within next 3 months. All other components in good condition.",
  "images": [
    "https://example.com/images/analysis1.jpg"
  ],
  "price_quote": {
    "1": 2800.00,
    "2": 3800.00
  },
  "recommended_services": {
    "3": 1500.00,
    "4": 2000.00
  }
}
```

**Expected Response**:
```json
{
  "booking_id": 1,
  "mechanic_id": "MEC000002",
  "description": "Completed thorough inspection...",
  "recommendation": "Recommend brake pad replacement...",
  "images": ["https://example.com/images/analysis1.jpg"],
  "validated": false,
  "created_at": "2025-11-06T14:00:00"
}
```

**Result**: 
- Booking status changes to "analysed"
- Booked services prices updated
- Recommendations added
- Assignment status changes to "completed"

---

### 10. Admin Validates Analysis

**Endpoint**: `POST /api/v1/bookings/admin/analysis/1/validate`

**Headers**:
```
Authorization: Bearer <admin_token>
```

**Expected Response**:
```json
{
  "message": "Analysis validated and sent to customer"
}
```

**Result**: Analysis validated flag set to true

---

### 11. Customer Confirms Services

**Endpoint**: `PUT /api/v1/bookings/1/confirm-services`

**Headers**:
```
Authorization: Bearer <customer_token>
```

**Request Body**:
```json
{
  "service_ids": [1, 2, 3]
}
```

**Note**: 
- service_ids [1, 2] are from booked_services (originally booked)
- service_id [3] is from booking_recommendations (mechanic recommended)
- Service 4 is not selected, so it remains as recommendation

**Expected Response**:
```json
{
  "message": "Services confirmed successfully"
}
```

**Result**: 
- Services 1, 2, 3 marked as "confirmed"
- Service 3 moved from recommendations to booked_services
- Booking status changes to "in-progress"

---

### 12. Admin Assigns Mechanic for Service

**Endpoint**: `POST /api/v1/bookings/admin/assign`

**Headers**:
```
Authorization: Bearer <admin_token>
```

**Request Body**:
```json
{
  "mechanic_id": "MEC000003",
  "booking_id": 1,
  "assignment_type_id": 3
}
```

**Note**: assignment_type_id = 3 for "service"

---

### 13. Mechanic Creates Progress with Service Completion

**Endpoint**: `POST /api/v1/bookings/mechanic/progress-with-completion`

**Headers**:
```
Authorization: Bearer <mechanic_token>
```

**Request Body**:
```json
{
  "booking_id": 1,
  "description": "Completed oil change and brake pad replacement. All services performed as per standard procedure.",
  "images": [
    "https://example.com/images/service1.jpg"
  ],
  "services_completed_ids": [1, 3]
}
```

**Expected Response**:
```json
{
  "id": 2,
  "mechanic_id": "MEC000003",
  "booking_id": 1,
  "description": "Completed oil change...",
  "images": ["https://example.com/images/service1.jpg"],
  "status_id": 6,
  "validated": false,
  "timestamp": "2025-11-07T10:00:00"
}
```

**Result**: Services 1 and 3 marked as completed

---

### 14. Admin Validates Service Progress

**Endpoint**: `POST /api/v1/bookings/admin/progress/2/validate`

**Headers**:
```
Authorization: Bearer <admin_token>
```

**Expected Response**:
```json
{
  "message": "Progress validated and sent to customer"
}
```

**Note**: If all services are completed, booking status changes to "completed"

---

### 15. Admin Assigns Mechanic for Drop

**Endpoint**: `POST /api/v1/bookings/admin/assign`

**Headers**:
```
Authorization: Bearer <admin_token>
```

**Request Body**:
```json
{
  "mechanic_id": "MEC000001",
  "booking_id": 1,
  "assignment_type_id": 2
}
```

**Note**: assignment_type_id = 2 for "drop"

**Result**: Booking status changes to "out for delivery"

---

### 16. Mechanic Creates Progress Update (Drop)

**Endpoint**: `POST /api/v1/bookings/mechanic/progress`

**Headers**:
```
Authorization: Bearer <mechanic_token>
```

**Request Body**:
```json
{
  "booking_id": 1,
  "description": "Car delivered successfully to customer. Customer satisfied with services.",
  "images": [
    "https://example.com/images/drop1.jpg"
  ]
}
```

**Expected Response**:
```json
{
  "id": 3,
  "mechanic_id": "MEC000001",
  "booking_id": 1,
  "description": "Car delivered successfully...",
  "images": ["https://example.com/images/drop1.jpg"],
  "status_id": 9,
  "validated": false,
  "timestamp": "2025-11-07T16:00:00"
}
```

**Result**: 
- Booking status changes to "delivered"
- completed_at timestamp set
- Assignment status changes to "completed"

---

### 17. Admin Final Validation

**Endpoint**: `POST /api/v1/bookings/admin/progress/3/validate`

**Headers**:
```
Authorization: Bearer <admin_token>
```

**Expected Response**:
```json
{
  "message": "Progress validated and sent to customer"
}
```

**Result**: Booking fully completed

---

## Alternative Flow: Customer Cancels Booking

**Endpoint**: `PUT /api/v1/bookings/1/cancel`

**Headers**:
```
Authorization: Bearer <customer_token>
```

**Expected Response**:
```json
{
  "message": "Booking cancelled successfully"
}
```

**Result**: Booking status changes to "cancelled"

---

## Error Scenarios to Test

### 1. Customer tries to access another customer's booking
**Expected**: 403 Forbidden

### 2. Mechanic tries to create progress for unassigned booking
**Expected**: Should work (no explicit check, but best practice would be to add validation)

### 3. Customer tries to confirm services before analysis validation
**Expected**: 400 Bad Request

### 4. Admin tries to assign mechanic with invalid assignment_type_id
**Expected**: 404 Not Found

### 5. Customer creates booking with invalid car_id
**Expected**: 403 Forbidden (car doesn't belong to customer)

---

## Postman Collection Tips

1. **Environment Variables**:
   - `{{base_url}}`: http://localhost:8000
   - `{{customer_token}}`: Bearer token for customer
   - `{{admin_token}}`: Bearer token for admin
   - `{{mechanic_token}}`: Bearer token for mechanic

2. **Request Chaining**:
   - Save booking_id from response and use in subsequent requests
   - Save progress_id from response for validation endpoints

3. **Test Scripts**:
   ```javascript
   // Save booking_id for next request
   pm.environment.set("booking_id", pm.response.json().id);
   
   // Verify status code
   pm.test("Status code is 200", function () {
       pm.response.to.have.status(200);
   });
   ```