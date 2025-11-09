scopes = {
    "READ:RBAC": [1, 2, 3],
    "WRITE:RBAC": [1],
    "DELETE:RBAC": [1],
    "UPDATE:RBAC": [1],

    # User management
    "READ:USERS": [1, 2, 3],
    "WRITE:USERS": [1],
    "DELETE:USERS": [1],
    "UPDATE:USERS": [1],

    # Mechanic management
    "READ:MECHANICS": [1, 2, 3],
    "WRITE:MECHANICS": [1],
    "DELETE:MECHANICS": [1],
    "UPDATE:MECHANICS": [1, 2],

    # Admin management
    "READ:ADMINS": [1],
    "WRITE:ADMINS": [1],
    "DELETE:ADMINS": [1],
    "UPDATE:ADMINS": [1],

    # Customer management
    "READ:CUSTOMERS": [1, 2, 3],
    "WRITE:CUSTOMERS": [1],
    "DELETE:CUSTOMERS": [1, 3],
    "UPDATE:CUSTOMERS": [1, 3],

    # Refresh tokens (admin can do all, mechanic/customer can read/update only)
    "READ:REFRESH_TOKENS": [1, 2, 3],
    "WRITE:REFRESH_TOKENS": [1],
    "DELETE:REFRESH_TOKENS": [1],
    "UPDATE:REFRESH_TOKENS": [1, 2, 3],

    # for all utility tables
    "READ:UTILS": [1, 2, 3],
    "WRITE:UTILS": [1],
    "DELETE:UTILS": [1],
    "UPDATE:UTILS": [1],

    "READ:CARS": [1, 2, 3],
    "WRITE:CARS": [1],
    "DELETE:CARS": [1],
    "UPDATE:CARS": [1],

    "READ:CUSTOMER_CARS": [1, 2, 3],
    "WRITE:CUSTOMER_CARS": [1, 3],
    "DELETE:CUSTOMER_CARS": [1, 3],
    "UPDATE:CUSTOMER_CARS": [1, 3],

    "READ:AREAS": [1, 2, 3],
    "WRITE:AREAS": [1],
    "DELETE:AREAS": [1],
    "UPDATE:AREAS": [1],

    "READ:ADDRESSES": [1, 2, 3],
    "WRITE:ADDRESSES": [1, 3],
    "DELETE:ADDRESSES": [1, 3],
    "UPDATE:ADDRESSES": [1, 3],

    "READ:SERVICE_CATEGORIES": [1, 2, 3],
    "WRITE:SERVICE_CATEGORIES": [1],
    "DELETE:SERVICE_CATEGORIES": [1],
    "UPDATE:SERVICE_CATEGORIES": [1],

    "READ:SERVICES": [1, 2, 3],
    "WRITE:SERVICES": [1],
    "DELETE:SERVICES": [1],
    "UPDATE:SERVICES": [1],

    "READ:PRICE_CHART": [1, 2, 3],
    "WRITE:PRICE_CHART": [1],
    "DELETE:PRICE_CHART": [1],
    "UPDATE:PRICE_CHART": [1],

    "READ:SERVICE_REVIEWS": [1, 2, 3],
    "WRITE:SERVICE_REVIEWS": [1, 3],
    "DELETE:SERVICE_REVIEWS": [1, 3],
    "UPDATE:SERVICE_REVIEWS": [1, 3],

    "READ:FAVOURITES": [1, 2, 3],
    "WRITE:FAVOURITES": [1, 3],
    "DELETE:FAVOURITES": [1, 3],
    "UPDATE:FAVOURITES": [1],

    "READ:CART": [1, 2, 3],
    "WRITE:CART": [1, 3],
    "DELETE:CART": [1, 3],
    "UPDATE:CART": [1],

    "READ:BOOKINGS": [1, 2, 3],
    "WRITE:BOOKINGS": [1, 3],
    "DELETE:BOOKINGS": [1],
    "UPDATE:BOOKINGS": [1, 3],
    
    "READ:BOOKED_SERVICES": [1, 2, 3],
    "WRITE:BOOKED_SERVICES": [1, 3],
    "DELETE:BOOKED_SERVICES": [1],
    "UPDATE:BOOKED_SERVICES": [1, 3],
    
    "READ:BOOKING_ASSIGNMENT": [1, 2, 3],
    "WRITE:BOOKING_ASSIGNMENT": [1],
    "DELETE:BOOKING_ASSIGNMENT": [1],
    "UPDATE:BOOKING_ASSIGNMENT": [1, 2],
    
    "READ:BOOKING_ANALYSIS": [1, 2, 3],
    "WRITE:BOOKING_ANALYSIS": [1, 2],
    "DELETE:BOOKING_ANALYSIS": [1],
    "UPDATE:BOOKING_ANALYSIS": [1],
    
    "READ:BOOKING_PROGRESS": [1, 2, 3],
    "WRITE:BOOKING_PROGRESS": [1, 2],
    "DELETE:BOOKING_PROGRESS": [1],
    "UPDATE:BOOKING_PROGRESS": [1],
    
    "READ:BOOKING_RECOMMENDATIONS": [1, 2, 3],
    "WRITE:BOOKING_RECOMMENDATIONS": [1, 2],
    "DELETE:BOOKING_RECOMMENDATIONS": [1],
    "UPDATE:BOOKING_RECOMMENDATIONS": [1],

    "READ:CONTENT": [1, 2, 3],
    "UPDATE:CONTENT": [1],

    "READ:GST": [1, 2, 3],
    "UPDATE:GST": [1],

    "READ:QUERIES": [1, 3],
    "WRITE:QUERIES": [1, 3],
    "UPDATE:QUERIES": [1],

    "READ:NOTIFICATION_LOG": [1],
    "WRITE:NOTIFICATION_LOG": [1],
    "DELETE:NOTIFICATION_LOG": [1],
    "UPDATE:NOTIFICATION_LOG": [1],
}

def get_all_scopes():
    return list(scopes.keys())

def get_scope_for_role(role_id: int):
    res = []
    for permission, allowed in scopes.items():
        if role_id in allowed:
            res.append(permission)
    return res

def get_admin_scopes():
    return get_scope_for_role(1)

def get_mechanic_scopes():
    return get_scope_for_role(2)

def get_customer_scopes():
    return get_scope_for_role(3)