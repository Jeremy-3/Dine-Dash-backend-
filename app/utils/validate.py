import re,phonenumbers
from pydantic import EmailStr, ValidationError

  
def valid_email(value:str) -> bool:
    try:
        EmailStr.validate_python(value)
        return True
    except ValidationError:
        return False

def validate_password(v: str) -> str:
    if valid_email:
        return v
    
    if len(v) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", v):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", v):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"[0-9]", v):
        raise ValueError("Password must contain at least one number")
    if not re.search(r"[\W_]", v):
        raise ValueError("Password must contain at least one special character")

    return v

def validate_kenyan_phone_number(phone: str) -> str:
    """
    Validates and formats Kenyan phone numbers to start with '2547' or '2541'.
    
    Accepts formats like:
        - 07xxxxxxxx
        - 01xxxxxxxx
        - 2547xxxxxxx
        - 2541xxxxxxx
    
    Returns:
        A formatted phone number starting with '2547' or '2541'.
    
    Raises:
        ValueError: If the phone number is invalid or doesn't start with 07, 01, or 2547/2541.
    """
    # Remove common non-numeric characters
    phone = re.sub(r"[^\d]", "", phone)

    # Format 07xxxxxxxx or 01xxxxxxxx
    if phone.startswith("07") or phone.startswith("01"):
        return f"254{phone[1:]}"
    
    # Format 2547xxxxxxxx or 2541xxxxxxxx
    if phone.startswith("2547") or phone.startswith("2541"):
        return phone
    
    raise ValueError("Invalid phone number. Must start with 07, 01, or 2547 / 2541.")
