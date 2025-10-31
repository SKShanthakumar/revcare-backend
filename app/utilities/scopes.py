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