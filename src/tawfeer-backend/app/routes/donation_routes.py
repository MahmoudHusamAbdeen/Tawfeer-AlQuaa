"""
Tawfeer Backend - Donation and Food Request Routes
Handles food donations, food requests, and order management for users.
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends

from app.database import get_users_collection, get_donations_collection, get_food_requests_collection
from app.models.donation import (
    CreateDonationRequest, CreateFoodRequestRequest,
    DonationResponse, FoodRequestResponse, MarkOrderDoneRequest
)
from app.services.auth import get_current_user

router = APIRouter(prefix="/api/donations", tags=["Donations & Requests"])


@router.post("/donate", response_model=DonationResponse, status_code=status.HTTP_201_CREATED)
async def create_donation(request: CreateDonationRequest, current_user: dict = Depends(get_current_user)):
    """
    Submit a food donation.

    Creates a new donation order with pending status and adds 20 points
    to the user's account upon successful submission.
    """
    users_col = get_users_collection()
    donations_col = get_donations_collection()

    # Get user info
    user = await users_col.find_one({"email": request.user_email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    donation_id = str(int(datetime.utcnow().timestamp() * 1000))
    now = datetime.utcnow().isoformat()

    # Create donation document
    donation_doc = {
        "id": donation_id,
        "user_email": request.user_email,
        "user_name": user["name"],
        "user_phone": user["phone"],
        "type": "donation",
        "people": request.people,
        "food_type": request.food_type,
        "is_new": request.is_new,
        "is_consumable": request.is_consumable,
        "is_cooked": request.is_cooked,
        "uncooked_type": request.uncooked_type,
        "uncooked_quantity": request.uncooked_quantity,
        "uncooked_unit": request.uncooked_unit,
        "custom_uncooked_type": request.custom_uncooked_type,
        "description": request.description,
        "location": request.location,
        "phone": request.phone,
        "image_uri": request.image_uri,
        "status": "pending",
        "created_at": now,
        "updated_at": now,
    }

    # Save to donations collection
    await donations_col.insert_one(donation_doc)

    # Create order entry for user's active orders
    order_entry = {
        "id": donation_id,
        "type": "donation",
        "date": now,
        "status": "pending",
        "people": request.people,
        "food_type": request.food_type,
        "is_new": request.is_new,
        "is_consumable": request.is_consumable,
        "is_cooked": request.is_cooked,
        "description": request.description,
        "location": request.location,
        "image_uri": request.image_uri,
        "points_earned": 0,
        "driver_name": "",
        "driver_phone": "",
        "estimated_pickup": "",
        "just_approved": False,
        "acknowledged": False,
    }

    # Also add to donation history
    history_entry = {
        "id": donation_id,
        "date": now,
        "food_type": request.food_type,
        "people": request.people,
        "status": "pending",
        "points_earned": 0,
        "driver_name": "",
        "driver_phone": "",
        "estimated_pickup": "",
        "location": request.location,
        "description": request.description,
        "is_new": request.is_new,
        "is_consumable": request.is_consumable,
        "is_cooked": request.is_cooked,
        "image_uri": request.image_uri,
    }

    # Update user document
    await users_col.update_one(
        {"email": request.user_email},
        {
            "$push": {
                "active_orders": order_entry,
                "donation_history": history_entry,
            },
            "$set": {"updated_at": now}
        }
    )

    return DonationResponse(
        id=donation_id,
        user_email=request.user_email,
        user_name=user["name"],
        user_phone=user["phone"],
        type="donation",
        people=request.people,
        food_type=request.food_type,
        is_new=request.is_new,
        is_consumable=request.is_consumable,
        is_cooked=request.is_cooked,
        description=request.description,
        location=request.location,
        status="pending",
        image_uri=request.image_uri,
        created_at=now,
    )


@router.post("/request", response_model=FoodRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_food_request(request: CreateFoodRequestRequest, current_user: dict = Depends(get_current_user)):
    """
    Submit a food request.

    Creates a new food request order with pending status.
    """
    users_col = get_users_collection()
    requests_col = get_food_requests_collection()

    # Get user info
    user = await users_col.find_one({"email": request.user_email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    request_id = str(int(datetime.utcnow().timestamp() * 1000))
    now = datetime.utcnow().isoformat()

    # Create request document
    request_doc = {
        "id": request_id,
        "user_email": request.user_email,
        "user_name": user["name"],
        "user_phone": user["phone"],
        "type": "request",
        "reason": request.reason,
        "people": request.people,
        "location": request.location,
        "phone": request.phone,
        "status": "pending",
        "created_at": now,
        "updated_at": now,
    }

    await requests_col.insert_one(request_doc)

    # Create order entry for user's active orders
    order_entry = {
        "id": request_id,
        "type": "request",
        "date": now,
        "status": "pending",
        "people": request.people,
        "reason": request.reason,
        "location": request.location,
        "points_earned": 0,
        "driver_name": "",
        "driver_phone": "",
        "estimated_delivery": "",
        "just_approved": False,
        "acknowledged": False,
    }

    await users_col.update_one(
        {"email": request.user_email},
        {
            "$push": {"active_orders": order_entry},
            "$set": {"updated_at": now}
        }
    )

    return FoodRequestResponse(
        id=request_id,
        user_email=request.user_email,
        user_name=user["name"],
        user_phone=user["phone"],
        type="request",
        reason=request.reason,
        people=request.people,
        location=request.location,
        status="pending",
        created_at=now,
    )


@router.post("/mark-done")
async def mark_order_done(request: MarkOrderDoneRequest, current_user: dict = Depends(get_current_user)):
    """
    Mark an order as done (acknowledged by user).
    Removes the order from active orders.
    """
    users_col = get_users_collection()
    user = await users_col.find_one({"email": request.user_email})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    active_orders = user.get("active_orders", [])
    updated_orders = [o for o in active_orders if o.get("id") != request.order_id]

    await users_col.update_one(
        {"email": request.user_email},
        {
            "$set": {
                "active_orders": updated_orders,
                "updated_at": datetime.utcnow().isoformat()
            }
        }
    )

    return {"message": "Order completed and removed from active orders"}


@router.get("/history/{email}")
async def get_donation_history(email: str, current_user: dict = Depends(get_current_user)):
    """Get donation history for a specific user."""
    users_col = get_users_collection()
    user = await users_col.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"donation_history": user.get("donation_history", [])}


@router.get("/orders/{email}")
async def get_active_orders(email: str, current_user: dict = Depends(get_current_user)):
    """Get active orders for a specific user."""
    users_col = get_users_collection()
    user = await users_col.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"active_orders": user.get("active_orders", [])}


@router.get("/messages/{email}")
async def get_user_messages(email: str, current_user: dict = Depends(get_current_user)):
    """Get messages for a specific user."""
    users_col = get_users_collection()
    user = await users_col.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"messages": user.get("messages", [])}


@router.put("/messages/{email}/read/{message_id}")
async def mark_message_read(email: str, message_id: int, current_user: dict = Depends(get_current_user)):
    """Mark a message as read."""
    users_col = get_users_collection()
    user = await users_col.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    messages = user.get("messages", [])
    for msg in messages:
        if msg.get("id") == message_id:
            msg["read"] = True
            break

    await users_col.update_one(
        {"email": email},
        {"$set": {"messages": messages}}
    )

    return {"message": "Message marked as read"}


@router.post("/redeem-reward")
async def redeem_reward(email: str, points_cost: int, current_user: dict = Depends(get_current_user)):
    """Redeem a reward by deducting points."""
    users_col = get_users_collection()
    user = await users_col.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    current_points = user.get("points", 0)
    if current_points < points_cost:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient points. You have {current_points} but need {points_cost}"
        )

    new_points = current_points - points_cost
    await users_col.update_one(
        {"email": email},
        {"$set": {"points": new_points, "updated_at": datetime.utcnow().isoformat()}}
    )

    return {"message": "Reward redeemed successfully", "remaining_points": new_points}
