"""
Tawfeer Backend - Pydantic Models for User Authentication
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserType(str, Enum):
    household = "Household"
    restaurant = "Restaurant"
    supermarket = "Supermarket"
    organization = "Organization"
    other = "Other"


# ========== Request Models ==========

class UserRegisterRequest(BaseModel):
    """User registration request."""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=5, max_length=20)
    password: str = Field(..., min_length=4, max_length=100)
    type: UserType = UserType.household
    custom_type: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Ahmed Al Mansouri",
                "email": "ahmed@example.com",
                "phone": "+971501234567",
                "password": "securepassword123",
                "type": "Household"
            }
        }


class UserLoginRequest(BaseModel):
    """User login request - accepts email or phone."""
    email_or_phone: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "email_or_phone": "ahmed@example.com",
                "password": "securepassword123"
            }
        }


class DriverLoginRequest(BaseModel):
    """Driver login request."""
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class AdminLoginRequest(BaseModel):
    """Admin login request."""
    username: str
    password: str


class GovernmentLoginRequest(BaseModel):
    """Government login request."""
    username: str
    password: str


class ForgotPasswordRequest(BaseModel):
    """Forgot password request."""
    email: EmailStr


class UpdateProfileRequest(BaseModel):
    """Update user profile request."""
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    type: Optional[str] = None


class ChangePasswordRequest(BaseModel):
    """Change password request."""
    current_password: str
    new_password: str = Field(..., min_length=4)


# ========== Response Models ==========

class UserResponse(BaseModel):
    """User data returned in responses (no password)."""
    id: str
    name: str
    email: str
    phone: str
    type: str
    points: int = 0
    created_at: Optional[str] = None
    address: Optional[str] = None


class LoginResponse(BaseModel):
    """Login response with JWT token and user data."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    role: str = "user"  # user, admin, government, driver


class DonationHistoryItem(BaseModel):
    """Single donation history item."""
    id: str
    date: str
    food_type: str
    people: int
    status: str
    points_earned: int = 0
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    estimated_pickup: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    is_new: Optional[bool] = None
    is_consumable: Optional[bool] = None
    is_cooked: Optional[bool] = None
    image_uri: Optional[str] = None


class ActiveOrderItem(BaseModel):
    """Single active order item."""
    id: str
    type: str  # donation or request
    date: str
    status: str
    people: int
    location: Optional[str] = None
    food_type: Optional[str] = None
    reason: Optional[str] = None
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    estimated_pickup: Optional[str] = None
    estimated_delivery: Optional[str] = None
    points_earned: int = 0
    description: Optional[str] = None
    image_uri: Optional[str] = None
    just_approved: bool = False
    acknowledged: bool = False
    approved_at: Optional[str] = None


class MessageItem(BaseModel):
    """Single message item."""
    id: int
    type: str
    title: str
    content: str
    order_id: Optional[str] = None
    timestamp: str
    read: bool = False


class FullUserDataResponse(BaseModel):
    """Complete user data including donations, orders, messages."""
    user: UserResponse
    donation_history: List[DonationHistoryItem] = []
    active_orders: List[ActiveOrderItem] = []
    messages: List[MessageItem] = []
