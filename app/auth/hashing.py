from passlib.context import CryptContext

# Uses argon2 (widely used, secure hashing algorithm).
# deprecated="auto" ensures older schemes are marked deprecated automatically if you ever change them.
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    """
    Hash a plain text password using argon2 algorithm.
    
    Takes a plain password string and returns a hashed password.
    Hashing is one-way, meaning you cannot reverse it to get the original password.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        str: Hashed password string
    """
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """
    Verify a plain password against a hashed password.
    
    Compares a plain password with a hashed password using the same algorithm
    used for hashing. Returns True if they match, False otherwise.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Previously hashed password to compare against
        
    Returns:
        bool: True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)
