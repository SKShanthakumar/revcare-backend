# Email Notification System - Quick Reference

## 📋 Checklist

- [ ] Install dependencies: `pip install fastapi-mail jinja2`
- [ ] Add email configuration to `.env`
- [ ] Create `app/core/email_config.py`
- [ ] Create `app/models/notification.py`
- [ ] Create `app/services/notification.py`
- [ ] Create `app/schemas/query.py`
- [ ] Create `app/routes/query.py`
- [ ] Create email templates in `app/templates/email/`
- [ ] Update models `__init__.py`
- [ ] Update schemas `__init__.py`
- [ ] Add seed function for notification categories
- [ ] Run migrations
- [ ] Register routes in `app/main.py`

---

## 🔌 Required Imports

### Update `app/models/__init__.py`
```python
from .notification import NotificationCategory, NotificationLog, Query
```

### Update `app/schemas/__init__.py`
```python
from .query import QueryCreate, QueryResponse, QueryResponseCreate, NotificationLogResponse
```

### Update `app/main.py`
```python
from app.routes import booking, query

app.include_router(booking.router, prefix="/api/v1/bookings", tags=["Bookings"])
app.include_router(query.router, prefix="/api/v1/queries", tags=["Queries"])
```

---

## 🎯 Send Email Functions

### Import
```python
from app.services.notification import (
    send_booking_confirmation,
    send_progress_update,
    send_invoice,
    send_query_response
)
```

### 1. Booking Confirmation
```python
# After creating booking
await send_booking_confirmation(db, booking)
```

### 2. Progress Update
```python
# After creating/validating progress
await send_progress_update(db, booking, progress)
```

### 3. Invoice
```python
# When booking is delivered/completed
await send_invoice(db, booking)
```

### 4. Query Response
```python
# After admin responds to query
await send_query_response(
    db=db,
    query_email="customer@email.com",
    query_text="Original query text",
    response_text="Admin's response",
    admin_name="Admin Name"
)
```

---

## 🔒 Required Scopes

Add these to your `app/utilities/scopes.py`:

```python
# Query scopes
"READ:QUERIES",
"WRITE:QUERIES",
"DELETE:QUERIES",

# Notification log scopes
"READ:NOTIFICATION_LOGS",
```

Update role permissions:
```python
def get_admin_scopes():
    return [
        # ... existing scopes ...
        "READ:QUERIES",
        "WRITE:QUERIES",
        "DELETE:QUERIES",
        "READ:NOTIFICATION_LOGS",
    ]
```

---

## 📁 File Structure

```
app/
├── core/
│   └── email_config.py          ← Email configuration
├── models/
│   ├── __init__.py              ← Add: NotificationCategory, NotificationLog, Query
│   └── notification.py          ← New file
├── schemas/
│   ├── __init__.py              ← Add: QueryCreate, QueryResponse, etc.
│   └── query.py                 ← New file
├── services/
│   └── notification.py          ← New file
├── routes/
│   └── query.py                 ← New file
├── templates/
│   └── email/
│       ├── booking_confirmation.html
│       ├── progress_update.html
│       ├── invoice.html
│       └── query_response.html
└── utilities/
    └── seed.py                  ← Add: seed_notification_categories()
```

---

## 🌐 API Endpoints

### Public (No Auth)
- `POST /api/v1/queries/` - Submit a query

### Admin Only
- `GET /api/v1/queries/` - Get all queries
- `GET /api/v1/queries/{id}` - Get query by ID
- `PUT /api/v1/queries/{id}/respond` - Respond to query (sends email)
- `DELETE /api/v1/queries/{id}` - Delete query
- `GET /api/v1/queries/notifications/logs` - Get notification logs
- `GET /api/v1/queries/notifications/stats` - Get notification statistics
- `POST /api/v1/queries/test-email` - Send test email

---

## 🔧 Integration Points

### 1. Booking Creation
**File**: `app/routes/booking.py` or `app/services/booking.py`

```python
# After booking creation
try:
    await send_booking_confirmation(db, new_booking)
except Exception as e:
    print(f"Failed to send confirmation email: {e}")
```

### 2. Progress Update
**File**: `app/routes/booking.py`

```python
# After mechanic creates progress OR after admin validates
try:
    await send_progress_update(db, booking, progress)
except Exception as e:
    print(f"Failed to send progress email: {e}")
```

### 3. Invoice Generation
**File**: `app/services/booking.py` in `create_progress_update()`

```python
# When status changes to 'delivered'
if current_status_name == "out for delivery":
    await update_booking_status(db, progress_data.booking_id, "delivered")
    
    try:
        await send_invoice(db, booking)
    except Exception as e:
        print(f"Failed to send invoice email: {e}")
```

---

## 🧪 Testing

### Test Query Response Email
```bash
curl -X POST "http://localhost:8000/api/v1/queries/test-email?email=test@example.com" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

### Submit a Query (Public)
```bash
curl -X POST "http://localhost:8000/api/v1/queries/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "query_text": "I have a question about your services"
  }'
```

### Get All Queries (Admin)
```bash
curl -X GET "http://localhost:8000/api/v1/queries/?status=pending" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

### Respond to Query (Admin)
```bash
curl -X PUT "http://localhost:8000/api/v1/queries/1/respond" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "Thank you for your query. Here is our response..."
  }'
```

---

## ⚠️ Important Notes

1. **Error Handling**: Always wrap email sending in try-except blocks. Email failures shouldn't break your main business logic.

2. **Async Operations**: All email functions are async and should be awaited.

3. **Environment Variables**: Never commit email credentials. Always use `.env` file.

4. **Gmail Setup**: 
   - Enable 2FA
   - Generate App Password
   - Use app password in `MAIL_PASSWORD`

5. **Template Variables**: Ensure all variables used in templates are provided in the data preparation functions.

6. **Logging**: All email attempts (success/failure) are logged in `notification_log` table.

7. **Testing**: Use the test endpoint to verify email configuration before production.

---

## 🐛 Common Issues

### Issue: Email not sending
**Solution**: Check `.env` configuration and Gmail app password

### Issue: Template not found
**Solution**: Verify template path in `email_config.py` and file location

### Issue: Variables missing in template
**Solution**: Check data preparation functions match template variables

### Issue: ImportError
**Solution**: Verify all imports in `__init__.py` files

---

## 📊 Monitoring Emails

### View Failed Notifications
```python
failed_logs = await db.execute(
    select(NotificationLog)
    .where(NotificationLog.status == "failed")
    .order_by(desc(NotificationLog.timestamp))
)
```

### Get Success Rate
```bash
GET /api/v1/queries/notifications/stats
```

Returns:
```json
{
  "total_sent": 150,
  "total_failed": 5,
  "success_rate": 96.77,
  "by_category": {
    "Booking Confirmation": 50,
    "Progress Update": 60,
    "Invoice": 30,
    "Query Response": 15
  }
}
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Booking creates successfully and email is sent
- [ ] Progress updates send email notifications
- [ ] Invoice is sent when booking is delivered
- [ ] Query submission works (public endpoint)
- [ ] Admin can respond to queries and email is sent
- [ ] Notification logs are being created
- [ ] Failed emails are logged with error messages
- [ ] Templates render correctly with all variables
- [ ] Email arrives in inbox (not spam)
- [ ] Images/attachments (if any) load correctly

---

Your email notification system is now complete and ready for production! 🎉