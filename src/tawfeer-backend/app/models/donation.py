"""
Tawfeer Backend - Pydantic Models for Donations, Requests, and Orders
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ========== Donation Models ==========

class CreateDonationRequest(BaseModel):
    """Create a new food donation."""
    user_email: str
    people: int = Field(..., gt=0)
    is_new: Optional[bool] = None
    is_consumable: Optional[bool] = None
    is_cooked: Optional[bool] = None
    food_type: str = ""
    uncooked_type: Optional[str] = None
    uncooked_quantity: Optional[str] = None
    uncooked_unit: Optional[str] = None
    custom_uncooked_type: Optional[str] = None
    description: Optional[str] = None
    location: str = ""
    phone: str = ""
    image_uri: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "user_email": "ahmed@example.com",
                "people": 5,
                "is_new": True,
                "is_consumable": True,
                "is_cooked": True,
                "food_type": "Rice and Chicken",
                "location": "Dubai Marina",
                "phone": "+971501234567"
            }
        }


class CreateFoodRequestRequest(BaseModel):
    """Create a new food request."""
    user_email: str
    reason: str = Field(..., min_length=5)
    people: int = Field(..., gt=0)
    location: str = ""
    phone: str = ""

    class Config:
        json_schema_extra = {
            "example": {
                "user_email": "ahmed@example.com",
                "reason": "Family in need of food support",
                "people": 4,
                "location": "Abu Dhabi",
                "phone": "+971501234567"
            }
        }


class DonationResponse(BaseModel):
    """Donation response."""
    id: str
    user_email: str
    user_name: str
    user_phone: str
    type: str = "donation"
    people: int
    food_type: str = ""
    is_new: Optional[bool] = None
    is_consumable: Optional[bool] = None
    is_cooked: Optional[bool] = None
    description: Optional[str] = None
    location: str
    status: str = "pending"
    image_uri: Optional[str] = None
    created_at: str


class FoodRequestResponse(BaseModel):
    """Food request response."""
    id: str
    user_email: str
    user_name: str
    user_phone: str
    type: str = "request"
    reason: str
    people: int
    location: str
    status: str = "pending"
    created_at: str


# ========== Order Models ==========

class ApproveOrderRequest(BaseModel):
    """Admin approves an order."""
    order_id: str
    driver_name: str = ""
    driver_phone: str = ""
    estimated_time: str = ""


class UpdateOrderStatusRequest(BaseModel):
    """Driver updates order status."""
    order_id: str
    user_email: str
    new_status: str  # in_progress, completed
    delivery_notes: Optional[str] = None
    driver_location: Optional[str] = None
    points_to_award: int = 0


class MarkOrderDoneRequest(BaseModel):
    """User marks an order as done/acknowledged."""
    order_id: str
    user_email: str


class DeleteUserRequest(BaseModel):
    """Admin deletes a user."""
    user_email: str


# ========== Driver Models ==========

class CreateDriverRequest(BaseModel):
    """Create a new driver (admin action)."""
    name: str = Field(..., min_length=2)
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=4)
    phone: str = ""


class DriverResponse(BaseModel):
    """Driver response (no password)."""
    id: str
    name: str
    username: str
    phone: str


class DeleteDriverRequest(BaseModel):
    """Delete a driver by username."""
    username: str
