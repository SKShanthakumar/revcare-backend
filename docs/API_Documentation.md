# RevCare API API Documentation

**Version:** 0.1.0

**Generated on:** 2025-11-09 23:41:21


---
API Documentation
---


## `/api/v1/customers/cart/{service_id}`

### POST: Add To Cart

**Description:** Add a service to the customer's cart.

Args:
    service_id: ID of the service to add to cart
    db: Database session
    payload: Validated token payload
    
Returns:
    JSONResponse: Success message

**Tags:** Customers


**Parameters:**

- `service_id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### DELETE: Remove From Cart

**Description:** Remove a service from the customer's cart.

Args:
    service_id: ID of the service to remove from cart
    db: Database session
    payload: Validated token payload
    
Returns:
    JSONResponse: Success message

**Tags:** Customers


**Parameters:**

- `service_id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/customers/favourite/{service_id}`

### POST: Add To Favourite

**Description:** Add a service to the customer's favourites.

Args:
    service_id: ID of the service to add to favourites
    db: Database session
    payload: Validated token payload
    
Returns:
    JSONResponse: Success message

**Tags:** Customers


**Parameters:**

- `service_id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### DELETE: Remove From Favourite

**Description:** Remove a service from the customer's favourites.

Args:
    service_id: ID of the service to remove from favourites
    db: Database session
    payload: Validated token payload
    
Returns:
    JSONResponse: Success message

**Tags:** Customers


**Parameters:**

- `service_id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/customers/`

### GET: Get Customers

**Description:** Get customer(s) information.

If customer_id is provided, returns that specific customer.
Otherwise, returns all customers based on user permissions.

Args:
    customer_id: Optional customer ID to filter by
    db: Database session
    payload: Validated token payload
    
Returns:
    List[CustomerResponse]: List of customer information

**Tags:** Customers


**Parameters:**

- `customer_id` (query) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### POST: Create Customer

**Description:** Create a new customer account.

Args:
    customer: Customer creation data
    db: Database session
    
Returns:
    CustomerResponse: Created customer information

**Tags:** Customers


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/customers/{id}`

### PUT: Update Customer

**Description:** Update customer information.

Args:
    id: Customer ID to update
    customer_data: Updated customer data
    db: Database session
    payload: Validated token payload
    
Returns:
    CustomerResponse: Updated customer information

**Tags:** Customers


**Parameters:**

- `id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### DELETE: Delete Customer

**Description:** Delete a customer account.

Args:
    id: Customer ID to delete
    db: Database session
    payload: Validated token payload
    
Returns:
    JSONResponse: Success message

**Tags:** Customers


**Parameters:**

- `id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/admins/`

### GET: Get All Admins

**Description:** 

**Tags:** Admins


**Responses:**

- `200` — Successful Response


---

### POST: Create Admin

**Description:** 

**Tags:** Admins


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/admins/{id}`

### GET: Get Admin By Id

**Description:** 

**Tags:** Admins


**Parameters:**

- `id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### PUT: Update Admin

**Description:** 

**Tags:** Admins


**Parameters:**

- `id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### DELETE: Delete Admin

**Description:** 

**Tags:** Admins


**Parameters:**

- `id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/mechanics/assignment_type`

### GET: Get Assignment Types

**Description:** 

**Tags:** Mechanics


**Responses:**

- `200` — Successful Response


---

### POST: Create Assignment Type

**Description:** 

**Tags:** Mechanics


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/mechanics/assignment_type/{id}`

### PUT: Update Assignment Type By Id

**Description:** 

**Tags:** Mechanics


**Parameters:**

- `id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### DELETE: Delete Assignment Type By Id

**Description:** 

**Tags:** Mechanics


**Parameters:**

- `id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/mechanics/`

### GET: Get All Mechanics

**Description:** 

**Tags:** Mechanics


**Parameters:**

- `mechanic_id` (query) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### POST: Create Mechanic

**Description:** 

**Tags:** Mechanics


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/mechanics/{id}`

### PUT: Update Mechanic

**Description:** 

**Tags:** Mechanics


**Parameters:**

- `id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### DELETE: Delete Mechanic

**Description:** 

**Tags:** Mechanics


**Parameters:**

- `id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/auth/login`

### POST: Login

**Description:** Authenticate user and generate access/refresh tokens.

Validates user credentials (phone and password) and generates JWT tokens.
Sets refresh token as HTTP-only cookie for security.

Args:
    response: FastAPI Response object for setting cookies
    username: User's phone number (used as username)
    password: User's plain text password
    db: Database session
    
Returns:
    dict: Dictionary containing access_token and token_type
    
Raises:
    HTTPException: 401 if credentials are invalid

**Tags:** Authentication


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/auth/refresh`

### POST: Refresh Token

**Description:** Refresh access token using refresh token from cookie.

Validates the refresh token from HTTP-only cookie and generates a new access token.
Used to obtain a new access token without re-authenticating.

Args:
    request: FastAPI Request object to access cookies
    db: Database session
    
Returns:
    JSONResponse: Contains new access_token and token_type
    
Raises:
    HTTPException: 401 if refresh token is missing or invalid

**Tags:** Authentication


**Responses:**

- `200` — Successful Response


---


## `/api/v1/auth/logout`

### POST: Logout

**Description:** Logout user and revoke tokens.

Blacklists both access and refresh tokens, removes refresh token from database,
and deletes the refresh token cookie.

Args:
    request: FastAPI Request object to access cookies
    response: FastAPI Response object for deleting cookies
    payload: Validated token payload from validate_token dependency
    db: Database session
    
Returns:
    dict: Success message

**Tags:** Authentication


**Responses:**

- `200` — Successful Response


---


## `/api/v1/car/models`

### GET: Get Car Models

**Description:** 

**Tags:** Cars


**Responses:**

- `200` — Successful Response


---

### POST: Create Car Model

**Description:** 

**Tags:** Cars


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/car/models/{id}`

### PUT: Update Car Model By Id

**Description:** 

**Tags:** Cars


**Parameters:**

- `id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### DELETE: Delete Car Model By Id

**Description:** 

**Tags:** Cars


**Parameters:**

- `id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/car/class`

### GET: Get Car Classes

**Description:** 

**Tags:** Cars


**Responses:**

- `200` — Successful Response


---

### POST: Create Car Class

**Description:** 

**Tags:** Cars


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/car/class/{id}`

### PUT: Update Car Class By Id

**Description:** 

**Tags:** Cars


**Parameters:**

- `id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### DELETE: Delete Car Class By Id

**Description:** 

**Tags:** Cars


**Parameters:**

- `id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/car/fuel`

### GET: Get Fuel Types

**Description:** 

**Tags:** Cars


**Responses:**

- `200` — Successful Response


---

### POST: Create Fuel Type

**Description:** 

**Tags:** Cars


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/car/fuel/{id}`

### PUT: Update Fuel Type By Id

**Description:** 

**Tags:** Cars


**Parameters:**

- `id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### DELETE: Delete Fuel Type By Id

**Description:** 

**Tags:** Cars


**Parameters:**

- `id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/car/manufacturer`

### GET: Get Manufacturers

**Description:** 

**Tags:** Cars


**Responses:**

- `200` — Successful Response


---

### POST: Create Manufacturer

**Description:** 

**Tags:** Cars


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/car/manufacturer/{id}`

### PUT: Update Manufacturer By Id

**Description:** 

**Tags:** Cars


**Parameters:**

- `id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### DELETE: Delete Manufacturer By Id

**Description:** 

**Tags:** Cars


**Parameters:**

- `id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/car/`

### GET: Get Customer Cars

**Description:** 

**Tags:** Cars


**Parameters:**

- `customer_id` (query) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### POST: Create Customer Car

**Description:** 

**Tags:** Cars


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/car/{id}`

### GET: Get Customer Car By Id

**Description:** 

**Tags:** Cars


**Parameters:**

- `id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### PUT: Update Customer Car By Id

**Description:** 

**Tags:** Cars


**Parameters:**

- `id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### DELETE: Delete Customer Car By Id

**Description:** 

**Tags:** Cars


**Parameters:**

- `id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/address/area`

### GET: Get Areas

**Description:** 

**Tags:** Address


**Responses:**

- `200` — Successful Response


---

### POST: Create Area

**Description:** 

**Tags:** Address


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/address/area/{id}`

### PUT: Update Area By Id

**Description:** 

**Tags:** Address


**Parameters:**

- `id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### DELETE: Delete Area By Id

**Description:** 

**Tags:** Address


**Parameters:**

- `id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/address/`

### GET: Get Customer Addresses

**Description:** 

**Tags:** Address


**Parameters:**

- `customer_id` (query) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### POST: Create Address

**Description:** 

**Tags:** Address


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/address/{id}`

### PUT: Update Address By Id

**Description:** 

**Tags:** Address


**Parameters:**

- `id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### DELETE: Delete Address By Id

**Description:** 

**Tags:** Address


**Parameters:**

- `id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/services/category`

### GET: Get Categories

**Description:** 

**Tags:** Services


**Responses:**

- `200` — Successful Response


---

### POST: Create Category

**Description:** 

**Tags:** Services


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/services/category/{id}`

### PUT: Update Category By Id

**Description:** 

**Tags:** Services


**Parameters:**

- `id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### DELETE: Delete Category By Id

**Description:** 

**Tags:** Services


**Parameters:**

- `id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/services/review/{service_id}`

### GET: Get Reviews For Service

**Description:** 

**Tags:** Services


**Parameters:**

- `service_id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### PUT: Update Review By Id

**Description:** 

**Tags:** Services


**Parameters:**

- `service_id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### DELETE: Delete Review By Id

**Description:** 

**Tags:** Services


**Parameters:**

- `service_id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/services/review`

### POST: Create Review

**Description:** 

**Tags:** Services


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/services/`

### GET: Get Services By Category Id

**Description:** 

**Tags:** Services


**Parameters:**

- `category_id` (query) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### POST: Create Service

**Description:** 

**Tags:** Services


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/services/{service_id}`

### GET: Get Services By Service Id

**Description:** 

**Tags:** Services


**Parameters:**

- `service_id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/services/{id}`

### PUT: Update Service By Id

**Description:** 

**Tags:** Services


**Parameters:**

- `id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### DELETE: Delete Service By Id

**Description:** 

**Tags:** Services


**Parameters:**

- `id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/utils/status`

### GET: Get Status

**Description:** 

**Tags:** Utilities


**Responses:**

- `200` — Successful Response


---

### POST: Create Status

**Description:** 

**Tags:** Utilities


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/utils/status/{id}`

### PUT: Update Status By Id

**Description:** 

**Tags:** Utilities


**Parameters:**

- `id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### DELETE: Delete Status By Id

**Description:** 

**Tags:** Utilities


**Parameters:**

- `id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/utils/timeslot`

### GET: Get Timeslots

**Description:** 

**Tags:** Utilities


**Responses:**

- `200` — Successful Response


---

### POST: Create Timeslot

**Description:** 

**Tags:** Utilities


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/utils/timeslot/{id}`

### PUT: Update Timeslot By Id

**Description:** 

**Tags:** Utilities


**Parameters:**

- `id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---

### DELETE: Delete Timeslot By Id

**Description:** 

**Tags:** Utilities


**Parameters:**

- `id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/bookings/`

### POST: Create Booking

**Description:** Customer creates a new booking

**Tags:** Bookings


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/bookings/customer`

### GET: Get Customer Bookings

**Description:** Get all bookings for logged-in customer with simplified status

**Tags:** Bookings


**Responses:**

- `200` — Successful Response


---


## `/api/v1/bookings/{booking_id}/confirm-services`

### PUT: Confirm Services

**Description:** Customer confirms which services to proceed with after analysis

**Tags:** Bookings


**Parameters:**

- `booking_id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/bookings/{booking_id}/cancel`

### PUT: Cancel Booking

**Description:** Customer cancels a booking

**Tags:** Bookings


**Parameters:**

- `booking_id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/bookings/admin/dashboard`

### GET: Get Admin Bookings Dashboard

**Description:** Get all bookings with action indicators for admin dashboard

**Tags:** Bookings


**Parameters:**

- `status_id` (query) — 

- `action_required` (query) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/bookings/admin/assign`

### POST: Assign Mechanic

**Description:** Admin assigns mechanic to a booking

**Tags:** Bookings


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/bookings/admin/progress/{progress_id}`

### PUT: Update Progress

**Description:** Admin edits progress update

**Tags:** Bookings


**Parameters:**

- `progress_id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/bookings/admin/progress/{progress_id}/validate`

### POST: Validate Progress

**Description:** Admin validates and approves progress update

**Tags:** Bookings


**Parameters:**

- `progress_id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/bookings/admin/analysis/{booking_id}`

### PUT: Update Analysis

**Description:** Admin edits analysis report

**Tags:** Bookings


**Parameters:**

- `booking_id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/bookings/admin/analysis/{booking_id}/validate`

### POST: Validate Analysis

**Description:** Admin validates and approves analysis report

**Tags:** Bookings


**Parameters:**

- `booking_id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/bookings/mechanic/assignments`

### GET: Get Mechanic Assignments

**Description:** Get all assignments for logged-in mechanic

**Tags:** Bookings


**Responses:**

- `200` — Successful Response


---


## `/api/v1/bookings/mechanic/progress`

### POST: Create Progress Update

**Description:** Mechanic creates progress update (pickup/drop received)

**Tags:** Bookings


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/bookings/mechanic/analysis`

### POST: Create Analysis

**Description:** Mechanic creates analysis report

**Tags:** Bookings


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/bookings/{booking_id}`

### GET: Get Booking Details

**Description:** Get detailed booking information

**Tags:** Bookings


**Parameters:**

- `booking_id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/payment/verify`

### POST: Verify Payment

**Description:** 

**Tags:** Payment


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/payment/cash-on-delivery/{booking_id}`

### POST: Process Cash On Delivery

**Description:** 

**Tags:** Payment


**Parameters:**

- `booking_id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/payment/verify-cod`

### POST: Verify Cash On Delivery Payment

**Description:** 

**Tags:** Payment


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/payment_demo/confirm_booking/{booking_id}`

### GET: Render Confirm Service Page

**Description:** Render simple payment confirmation page.

**Tags:** 


**Parameters:**

- `booking_id` (path) — 

- `access_token` (query) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/payment_demo/cash_on_delivery/{booking_id}`

### GET: Render Cod Page

**Description:** 

**Tags:** 


**Parameters:**

- `booking_id` (path) — 

- `access_token` (query) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/content/{content_id}`

### GET: Get Content

**Description:** Retrieve a content record by its unique `content_id`.

Args:
    content_id (str): The unique content identifier (e.g., 'home_banner').
    payload (dict): Auth token payload from JWT validation.
    db (AsyncIOMotorDatabase): MongoDB database connection.

Returns:
    Content: The content record if found.

**Tags:** Content Management


**Parameters:**

- `content_id` (path) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/content/`

### PUT: Update Content

**Description:** Update multiple content records.

Args:
    updates (Dict[str, str]): Dictionary mapping `content_id` to new data.
        Example:
        {
            "home_banner": "https://cdn.example.com/new_banner.png",
            "about_us": "Updated about us text"
        }
    payload (dict): Auth token payload from JWT validation.
    db (AsyncIOMotorDatabase): MongoDB database connection.

Returns:
    List[ContentUpdateResponse]: A list of update results showing which
    content IDs were updated or created.

**Tags:** Content Management


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/gst/`

### PUT: Update Gst

**Description:** Get content by its unique content_id.

**Tags:** GST


**Parameters:**

- `percent` (query) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/queries/`

### GET: Get All Queries

**Description:** Retrieve all customer queries.

**Tags:** Queries


**Responses:**

- `200` — Successful Response


---

### POST: Create Query

**Description:** Create a new customer query.

**Tags:** Queries


**Request Body Example:**


**Responses:**

- `201` — Successful Response

- `422` — Validation Error


---


## `/api/v1/queries/{query_id}/respond`

### PUT: Respond To Query

**Description:** Respond to a specific customer query (admin only).

**Tags:** Queries


**Parameters:**

- `query_id` (path) — 


**Request Body Example:**


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/notification/notifications/logs`

### GET: Get Notification Logs

**Description:** Get notification logs with optional filters
Admin can view all logs, or filter by customer/status/type

**Tags:** Notification


**Parameters:**

- `notification_category` (query) — 

- `limit` (query) — 


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/backup/create`

### POST: Create Full Backup

**Description:** Create a backup of both PostgreSQL and MongoDB databases

**Tags:** Backup & Recovery


**Responses:**

- `200` — Successful Response


---


## `/api/v1/backup/list`

### GET: List Backups

**Description:** List all available backups for both databases

**Tags:** Backup & Recovery


**Responses:**

- `200` — Successful Response


---


## `/api/v1/backup/restore`

### POST: Restore Full Backup

**Description:** Restore both databases from backups

- **postgresql_backup**: Name of the PostgreSQL backup file
- **mongodb_backup**: Name of the MongoDB backup directory

Warning: This will delete all existing data in both databases

**Tags:** Backup & Recovery


**Parameters:**

- `postgresql_backup` (query) — PostgreSQL backup file name

- `mongodb_backup` (query) — MongoDB backup directory name


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/api/v1/backup/delete/{backup_name}`

### DELETE: Delete Backup

**Description:** Delete a backup file or directory

- **backup_name**: Name of the backup to delete
- **backup_type**: Type of backup ('postgresql' or 'mongodb')

**Tags:** Backup & Recovery


**Parameters:**

- `backup_name` (path) — 

- `backup_type` (query) — Type of backup: 'postgresql' or 'mongodb'


**Responses:**

- `200` — Successful Response

- `422` — Validation Error


---


## `/`

### GET: Welcome Message

**Description:** 

**Tags:** 


**Responses:**

- `200` — Successful Response


---
