from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    """Funkce pro hachovani hesla"""
    safe_password = password[:72]
    return pwd_context.hash(safe_password)

def verify_password(password: str, hashed: str) -> bool:
    """Funkce pro overeni spravnosti heshovaneho hesla"""
    safe_password = password[:72]
    return pwd_context.verify(safe_password, hashed)