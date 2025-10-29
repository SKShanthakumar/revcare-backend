from passlib.context import CryptContext

'''Uses bcrypt (widely used, secure hashing algorithm).
   deprecated="auto" ensures older schemes are marked deprecated automatically if you ever change them.'''
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

'''Takes a plain password (string) and returns a hashed password.Hashing is one-way, meaning you cannot reverse it to get the original password.'''
def hash_password(password: str):
    return pwd_context.hash(password)

'''Compares a plain password with a hashed password.Returns True if they match, False otherwise.'''
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
