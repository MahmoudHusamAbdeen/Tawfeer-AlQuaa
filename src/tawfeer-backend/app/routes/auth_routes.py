"""
Tawfeer Backend - Authentication Routes
User registration, login, profile management, and password reset.
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends

from app.database import get_users_collection
from app.models.user import (
    UserRegisterRequest, UserLoginRequest, DriverLoginRequest,
    AdminLoginRequest, GovernmentLoginRequest,
    UpdateProfileRequest, ChangePasswordRequest,
    LoginResponse, UserResponse, FullUserDataResponse,
    DonationHistoryItem, ActiveOrderItem, MessageItem
)
from app.services.auth import (
    hash_password, verify_password, create_access_token,
    get_current_user
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Admin and Government credentials (can be moved to DB later)
ADMIN_CREDENTIALS = {"admin123": "123"}
GOVERNMENT_CREDENTIALS = {"gov123": "123"}


@router.post("/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
async def register_user(request: UserRegisterRequest):
    """
    Register a new user account.

    - Creates a new user with hashed password
    - Returns JWT token and user data
    """
    users_col = get_users_collection()

    # Check if email already exists
    existing_user = await users_col.find_one({"email": request.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already in use"
        )

    # Check if phone already exists
    existing_phone = await users_col.find_one({"phone": request.phone})
    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This phone number is already in use"
        )

    # Determine user type
    user_type = request.custom_type if request.type == UserType.other and request.custom_type else request.type.value

    # Create user document
    user_doc = {
        "name": request.name,
        "email": request.email,
        "phone": request.phone,
        "password": hash_password(request.password),
        "type": user_type,
        "points": 0,
        "donation_history": [],
        "active_orders": [],
        "messages": [],
        "address": "",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }

    result = await users_col.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id

    # Create JWT token
    token = create_access_token(data={
        "email": request.email,
        "name": request.name,
        "role": "user",
        "type": user_type,
    })

    return LoginResponse(
        access_token=token,
        user=UserResponse(
            id=str(result.inserted_id),
            name=request.name,
            email=request.email,
            phone=request.phone,
            type=user_type,
            points=0,
            created_at=user_doc["created_at"],
        ),
        role="user"
    )


@router.post("/login", response_model=LoginResponse)
async def login_user(request: UserLoginRequest):
    """
    Login a user with email/phone and password.

    - Accepts email or phone as identifier
    - Returns JWT token and user data
    - Also handles admin and government logins
    """
    users_col = get_users_collection()

    # Check for admin credentials
    if request.email_or_phone == "admin123" and request.password == "123":
        token = create_access_token(data={
            "email": "admin@tawfeer.ae",
            "name": "Admin",
            "role": "admin",
        })
        return LoginResponse(
            access_token=token,
            user=UserResponse(
                id="admin",
                name="Admin",
                email="admin@tawfeer.ae",
                phone="",
                type="Admin",
                points=0,
            ),
            role="admin"
        )

    # Check for government credentials
    if request.email_or_phone == "gov123" and request.password == "123":
        token = create_access_token(data={
            "email": "gov@tawfeer.ae",
            "name": "Government Official",
            "role": "government",
        })
        return LoginResponse(
            access_token=token,
            user=UserResponse(
                id="gov",
                name="Government Official",
                email="gov@tawfeer.ae",
                phone="",
                type="Government",
                points=0,
            ),
            role="government"
        )

    # Find user by email or phone
    user = await users_col.find_one({
        "$or": [
            {"email": request.email_or_phone},
            {"phone": request.email_or_phone}
        ]
    })

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Verify password
    if not verify_password(request.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Create JWT token
    token = create_access_token(data={
        "email": user["email"],
        "name": user["name"],
        "role": "user",
        "type": user.get("type", ""),
    })

    return LoginResponse(
        access_token=token,
        user=UserResponse(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            phone=user["phone"],
            type=user.get("type", ""),
            points=user.get("points", 0),
            created_at=user.get("created_at", ""),
            address=user.get("address", ""),
        ),
        role="user"
    )


@router.post("/driver-login", response_model=LoginResponse)
async def driver_login(request: DriverLoginRequest):
    """
    Login a driver with username and password.
    """
    from app.database import get_drivers_collection
    drivers_col = get_drivers_collection()

    driver = await drivers_col.find_one({"username": request.username})
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not verify_password(request.password, driver["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token(data={
        "email": driver["username"],
        "name": driver["name"],
        "role": "driver",
        "driver_id": str(driver["_id"]),
    })

    return LoginResponse(
        access_token=token,
        user=UserResponse(
            id=str(driver["_id"]),
            name=driver["name"],
            email=driver["username"],
            phone=driver.get("phone", ""),
            type="Driver",
            points=0,
        ),
        role="driver"
    )


@router.get("/me", response_model=FullUserDataResponse)
async def get_current_user_data(current_user: dict = Depends(get_current_user)):
    """
    Get complete current user data including donations, orders, and messages.
    """
    users_col = get_users_collection()
    user = await users_col.find_one({"email": current_user["email"]})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Convert donation history
    donation_history = [
        DonationHistoryItem(
            id=d.get("id", str(i)),
            date=d.get("date", ""),
            food_type=d.get("food_type", ""),
            people=d.get("people", 0),
            status=d.get("status", ""),
            points_earned=d.get("points_earned", 0),
            driver_name=d.get("driver_name"),
            driver_phone=d.get("driver_phone"),
            estimated_pickup=d.get("estimated_pickup"),
            location=d.get("location"),
            description=d.get("description"),
            is_new=d.get("is_new"),
            is_consumable=d.get("is_consumable"),
            is_cooked=d.get("is_cooked"),
            image_uri=d.get("image_uri"),
        )
        for i, d in enumerate(user.get("donation_history", []))
    ]

    # Convert active orders
    active_orders = [
        ActiveOrderItem(
            id=o.get("id", str(i)),
            type=o.get("type", "donation"),
            date=o.get("date", ""),
            status=o.get("status", "pending"),
            people=o.get("people", 0),
            location=o.get("location"),
            food_type=o.get("food_type"),
            reason=o.get("reason"),
            driver_name=o.get("driver_name"),
            driver_phone=o.get("driver_phone"),
            estimated_pickup=o.get("estimated_pickup"),
            estimated_delivery=o.get("estimated_delivery"),
            points_earned=o.get("points_earned", 0),
            description=o.get("description"),
            image_uri=o.get("image_uri"),
            just_approved=o.get("just_approved", False),
            acknowledged=o.get("acknowledged", False),
            approved_at=o.get("approved_at"),
        )
        for i, o in enumerate(user.get("active_orders", []))
    ]

    # Convert messages
    messages = [
        MessageItem(
            id=m.get("id", i),
            type=m.get("type", ""),
            title=m.get("title", ""),
            content=m.get("content", ""),
            order_id=m.get("order_id"),
            timestamp=m.get("timestamp", ""),
            read=m.get("read", False),
        )
        for i, m in enumerate(user.get("messages", []))
    ]

    return FullUserDataResponse(
        user=UserResponse(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            phone=user["phone"],
            type=user.get("type", ""),
            points=user.get("points", 0),
            created_at=user.get("created_at", ""),
            address=user.get("address", ""),
        ),
        donation_history=donation_history,
        active_orders=active_orders,
        messages=messages,
    )


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    request: UpdateProfileRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Update user profile information.
    """
    users_col = get_users_collection()

    update_fields = {}
    if request.name is not None:
        update_fields["name"] = request.name
    if request.phone is not None:
        update_fields["phone"] = request.phone
    if request.address is not None:
        update_fields["address"] = request.address
    if request.type is not None:
        update_fields["type"] = request.type

    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )

    update_fields["updated_at"] = datetime.utcnow().isoformat()

    result = await users_col.update_one(
        {"email": current_user["email"]},
        {"$set": update_fields}
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or no changes made"
        )

    # Fetch updated user
    user = await users_col.find_one({"email": current_user["email"]})

    return UserResponse(
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"],
        phone=user["phone"],
        type=user.get("type", ""),
        points=user.get("points", 0),
        created_at=user.get("created_at", ""),
        address=user.get("address", ""),
    )


@router.put("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user)
):
    """Change user password."""
    users_col = get_users_collection()
    user = await users_col.find_one({"email": current_user["email"]})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(request.current_password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    await users_col.update_one(
        {"email": current_user["email"]},
        {"$set": {
            "password": hash_password(request.new_password),
            "updated_at": datetime.utcnow().isoformat()
        }}
    )

    return {"message": "Password changed successfully"}


@router.post("/logout")
async def logout():
    """Logout endpoint (client-side token removal)."""
    return {"message": "Logged out successfully. Please remove the token on client side."}
