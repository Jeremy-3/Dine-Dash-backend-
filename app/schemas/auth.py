from pydantic import BaseModel,EmailStr,field_validator
from app.utils.validate import validate_password

class Login(BaseModel):
    email:EmailStr
    password:str
    
class LoginVerify(BaseModel):
    email:EmailStr
    otp:int
    
class Token(BaseModel):
    email:str
    access_token :str
    token_type :str = "bearer"
    
# class ForgotPassword(BaseModel):
#     email:EmailStr
    
# class ResetPassword(BaseModel):
#      email:EmailStr
#      password:str
#      otp:str         
        
#      @field_validator("password")
#      def validate_password_filed(cls,v:str) -> str:
#         return validate_password(v) 
            