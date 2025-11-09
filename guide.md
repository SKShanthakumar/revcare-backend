# Email Notification Service - Integration Guide

## 📦 Installation

```bash
pip install fastapi-mail jinja2
```

## 🔧 Setup

### 1. Environment Variables

Add to your `.env` file:

```env
# Email Configuration
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=your-email@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_FROM_NAME=RevCare
```

**For Gmail:**
1. Enable 2-Factor Authentication
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the app password in `MAIL_PASSWORD`

### 2. Directory Structure

Create template directory:
```
app/
├── templates/
│   └── email/
│       ├── booking_confirmation.html
│       ├── progress_update.html
│       ├── invoice.html
│       └── query_response.html
```

### 3. Update Models __init__.py

```python
# app/models/__init__.py
from .notification import NotificationCategory, NotificationLog, Query
```

### 4. Run Migrations

Create and run migrations for the new tables:
```bash
alembic revision --autogenerate -m "Add notification tables"
alembic upgrade head
```

### 5. Seed Notification Categories

Run your seed script to populate notification categories.

---

## 🚀 Usage Examples

### 1. Booking Confirmation

**In your booking creation endpoint:**

```python
# app/routes/booking.py
from app.services.notification import send_booking_confirmation

@router.post("/", response_model=BookingResponse)
async def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["WRITE:BOOKINGS"])
):
    # Create booking
    new_booking = await booking_service.create_booking(db, booking, payload)
    
    # Send confirmation email
    try:
        await send_booking_confirmation(db, new_booking)
    except Exception as e:
        print(f"Failed to send confirmation email: {e}")
        # Don't fail the booking if email fails
    
    return new_booking
```

### 2. Progress Update

**After mechanic creates progress update:**

```python
# app/routes/booking.py
from app.services.notification import send_progress_update

@router.post("/mechanic/progress", response_model=BookingProgressResponse)
async def create_progress_update(
    progress: BookingProgressCreate,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["WRITE:BOOKING_PROGRESS"])
):
    # Create progress update
    new_progress = await booking_service.create_progress_update(db, progress, payload)
    
    # Fetch booking
    booking = await db.get(Booking, progress.booking_id)
    
    # Send email notification
    try:
        await send_progress_update(db, booking, new_progress)
    except Exception as e:
        print(f"Failed to send progress email: {e}")
    
    return new_progress
```

**Or after admin validates progress:**

```python
@router.post("/admin/progress/{progress_id}/validate", response_class=JSONResponse)
async def validate_progress(
    progress_id: int,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["UPDATE:BOOKING_PROGRESS"])
):
    # Validate progress
    await booking_service.validate_progress(db, progress_id)
    
    # Fetch progress and booking
    progress = await db.get(BookingProgress, progress_id)
    booking = await db.get(Booking, progress.booking_id)
    
    # Send email after validation
    try:
        await send_progress_update(db, booking, progress)
    except Exception as e:
        print(f"Failed to send progress email: {e}")
    
    return JSONResponse(content={"message": "Progress validated and sent to customer"})
```

### 3. Invoice on Completion

**When booking is marked as delivered:**

```python
# app/services/booking.py
from app.services.notification import send_invoice

async def create_progress_update(db: Session, progress_data: BookingProgressCreate, payload: dict):
    # ... existing code ...
    
    # Update booking status to 'delivered'
    current_status_name = booking.status.name.lower()
    if current_status_name == "out for delivery":
        await update_booking_status(db, progress_data.booking_id, "delivered")
        
        # Send invoice email
        try:
            await send_invoice(db, booking)
        except Exception as e:
            print(f"Failed to send invoice email: {e}")
    
    # ... rest of the code ...
```

### 4. Query Response

**Create Query endpoint:**

```python
# app/routes/query.py
from fastapi import APIRouter, Depends, Security
from app.models import Query
from app.schemas import QueryCreate, QueryResponse, QueryResponseCreate
from app.services.notification import send_query_response

router = APIRouter()

@router.post("/", response_model=QueryResponse)
async def create_query(
    query: QueryCreate,
    db: Session = Depends(get_postgres_db)
):
    """Customer submits a query (no authentication required)"""
    new_query = Query(
        customer_email=query.email,
        query=query.query_text
    )
    db.add(new_query)
    await db.commit()
    await db.refresh(new_query)
    
    return new_query


@router.put("/{query_id}/respond", response_model=QueryResponse)
async def respond_to_query(
    query_id: int,
    response_data: QueryResponseCreate,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["WRITE:QUERIES"])
):
    """Admin responds to a query"""
    query = await db.get(Query, query_id)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    
    admin_id = payload.get("user_id")
    
    # Update query
    query.response = response_data.response
    query.responded_by = admin_id
    query.responded_at = datetime.now()
    
    await db.commit()
    await db.refresh(query)
    
    # Send email response
    try:
        await send_query_response(
            db=db,
            query_email=query.customer_email,
            query_text=query.query,
            response_text=query.response,
            admin_name=query.admin.name
        )
    except Exception as e:
        print(f"Failed to send query response email: {e}")
    
    return query
```

**Query Schemas:**

```python
# app/schemas/query.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class QueryCreate(BaseModel):
    email: EmailStr
    query_text: str

class QueryResponseCreate(BaseModel):
    response: str

class QueryResponse(BaseModel):
    id: int
    customer_email: str
    query: str
    response: Optional[str]
    responded_by: Optional[str]
    created_at: datetime
    responded_at: Optional[datetime]
    
    class Config:
        from_attributes = True
```

---

## 📊 Viewing Notification Logs

**Admin endpoint to view notification logs:**

```python
# app/routes/notification.py
from fastapi import APIRouter, Depends, Security
from app.models import NotificationLog

router = APIRouter()

@router.get("/logs", response_model=List[NotificationLogResponse])
async def get_notification_logs(
    customer_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["READ:NOTIFICATION_LOGS"])
):
    """Get notification logs with optional filters"""
    query = select(NotificationLog).options(
        selectinload(NotificationLog.category),
        selectinload(NotificationLog.customer)
    ).order_by(desc(NotificationLog.timestamp))
    
    if customer_id:
        query = query.where(NotificationLog.customer_id == customer_id)
    
    if status:
        query = query.where(NotificationLog.status == status)
    
    query = query.limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()
```

---

## 🎨 Customizing Email Templates

All templates use Jinja2. You can customize them by editing the HTML files.

**Available variables per template:**

### booking_confirmation.html
- `customer_name`
- `booking_id`
- `car_model`
- `car_reg`
- `pickup_date`, `pickup_time`, `pickup_address`
- `drop_date`, `drop_time`, `drop_address`
- `services` (list of dicts with `name`, `price`)
- `total_price`
- `created_at`

### progress_update.html
- `customer_name`
- `booking_id`
- `car_model`, `car_reg`
- `status`
- `progress_description`
- `update_time`
- `mechanic_name`
- `images` (list of URLs)

### invoice.html
- `customer_name`, `customer_email`, `customer_phone`
- `booking_id`
- `invoice_date`
- `car_model`, `car_reg`
- `services` (list with `name`, `price`, `warranty`)
- `subtotal`, `gst_rate`, `gst_amount`, `total`

### query_response.html
- `query`
- `response`
- `admin_name`
- `response_date`

---

## 🔒 Security Best Practices

1. **Never commit credentials** - Always use environment variables
2. **Use App Passwords** - For Gmail, use app-specific passwords
3. **Rate Limiting** - Implement rate limiting for email sending
4. **Async Operations** - Emails are sent asynchronously to not block requests
5. **Error Handling** - Email failures don't break the main flow
6. **Logging** - All emails are logged to `notification_log` table

---

## 🐛 Troubleshooting

### Email not sending

1. **Check credentials**:
   ```python
   from app.core.email_config import email_settings
   print(email_settings.MAIL_USERNAME)
   print(email_settings.MAIL_SERVER)
   ```

2. **Test connection**:
   ```python
   from fastapi_mail import FastMail
   from app.core.email_config import email_conf
   
   fm = FastMail(email_conf)
   # Check if connection works
   ```

3. **Gmail specific**:
   - Enable "Less secure app access" OR use App Password
   - Check if 2FA is enabled

4. **Check logs**:
   ```python
   # Query failed notifications
   failed_logs = await db.execute(
       select(NotificationLog).where(NotificationLog.status == "failed")
   )
   ```

### Templates not found

Ensure templates are in correct directory:
```
app/templates/email/booking_confirmation.html
```

Update path in `email_config.py` if needed.

---

## 📈 Monitoring

**Get email statistics:**

```python
@router.get("/stats")
async def get_email_stats(
    db: Session = Depends(get_postgres_db),
    payload = Security(validate_token, scopes=["READ:NOTIFICATION_LOGS"])
):
    # Total sent
    total_sent = await db.execute(
        select(func.count()).select_from(NotificationLog)
        .where(NotificationLog.status == "sent")
    )
    
    # Total failed
    total_failed = await db.execute(
        select(func.count()).select_from(NotificationLog)
        .where(NotificationLog.status == "failed")
    )
    
    # By category
    by_category = await db.execute(
        select(
            NotificationCategory.name,
            func.count(NotificationLog.id)
        )
        .join(NotificationCategory)
        .group_by(NotificationCategory.name)
    )
    
    return {
        "total_sent": total_sent.scalar(),
        "total_failed": total_failed.scalar(),
        "by_category": dict(by_category.all())
    }
```

---

## ✅ Testing

**Test email sending:**

```python
# Create a test endpoint
@router.post("/test-email")
async def test_email(
    email: str,
    db: Session = Depends(get_postgres_db)
):
    """Send a test email"""
    from app.services.notification import send_query_response
    
    try:
        await send_query_response(
            db=db,
            query_email=email,
            query_text="This is a test query",
            response_text="This is a test response",
            admin_name="Test Admin"
        )
        return {"message": "Test email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 🎯 Summary

1. ✅ Install `fastapi-mail` and `jinja2`
2. ✅ Configure email settings in `.env`
3. ✅ Create email templates in `app/templates/email/`
4. ✅ Seed notification categories
5. ✅ Import notification service in your routes
6. ✅ Call appropriate send functions after actions
7. ✅ Handle errors gracefully (don't break main flow)
8. ✅ Monitor logs via admin endpoints

Your notification system is now ready to use! 🚀