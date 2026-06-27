"""
Tawfeer Backend - Admin Routes
Admin dashboard: user management, order approval, driver management, statistics.
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional

from app.database import (
    get_users_collection, get_drivers_collection,
    get_donations_collection, get_food_requests_collection
)
from app.models.donation import (
    ApproveOrderRequest, UpdateOrderStatusRequest, DeleteUserRequest,
    CreateDriverRequest, DriverResponse, DeleteDriverRequest
)
from app.services.auth import get_current_admin, hash_password, verify_password

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/stats")
async def get_admin_stats(current_admin: dict = Depends(get_current_admin)):
    """
    Get admin dashboard statistics.

    Returns total users, total orders, points, active users,
    pending/approved/completed orders, and total drivers.
    """
    users_col = get_users_collection()
    drivers_col = get_drivers_collection()

    users = []
    async for user in users_col.find({}):
        users.append(user)

    drivers = []
    async for driver in drivers_col.find({}):
        drivers.append(driver)

    # Calculate stats
    total_points = sum(u.get("points", 0) for u in users)
    active_users = sum(1 for u in users if u.get("points", 0) > 0)

    # Collect all orders
    all_orders = []
    pending = approved = completed = 0
    for user in users:
        for order in user.get("active_orders", []):
            all_orders.append({
                **order,
                "user_name": user["name"],
                "user_email": user["email"],
                "user_phone": user["phone"],
            })
            ostatus = order.get("status", "")
            if ostatus == "pending":
                pending += 1
            elif ostatus == "approved":
                approved += 1
            elif ostatus == "completed":
                completed += 1

    # Top users by points
    top_users = sorted(users, key=lambda u: u.get("points", 0), reverse=True)[:5]

    return {
        "total_users": len(users),
        "total_orders": len(all_orders),
        "total_points": total_points,
        "active_users": active_users,
        "pending_orders": pending,
        "approved_orders": approved,
        "completed_orders": completed,
        "total_drivers": len(drivers),
        "top_users": [
            {
                "name": u.get("name", ""),
                "email": u.get("email", ""),
                "points": u.get("points", 0),
                "type": u.get("type", ""),
            }
            for u in top_users
        ],
    }


@router.get("/users")
async def get_all_users(current_admin: dict = Depends(get_current_admin)):
    """Get list of all registered users."""
    users_col = get_users_collection()
    users = []
    async for user in users_col.find({}):
        users.append({
            "id": str(user["_id"]),
            "name": user.get("name", ""),
            "email": user.get("email", ""),
            "phone": user.get("phone", ""),
            "type": user.get("type", ""),
            "points": user.get("points", 0),
            "active_orders_count": len(user.get("active_orders", [])),
            "created_at": user.get("created_at", ""),
        })
    return {"users": users}


@router.get("/orders")
async def get_all_orders(current_admin: dict = Depends(get_current_admin)):
    """Get all orders from all users."""
    users_col = get_users_collection()
    all_orders = []
    async for user in users_col.find({}):
        for order in user.get("active_orders", []):
            all_orders.append({
                **order,
                "user_name": user["name"],
                "user_email": user["email"],
                "user_phone": user["phone"],
            })

    # Sort by date descending
    all_orders.sort(key=lambda x: x.get("date", ""), reverse=True)
    return {"orders": all_orders}


@router.post("/approve-order")
async def approve_order(request: ApproveOrderRequest, current_admin: dict = Depends(get_current_admin)):
    """
    Approve a pending order and assign a driver.

    Updates the order status to 'approved' and assigns driver information.
    Also sends a notification message to the user.
    """
    users_col = get_users_collection()

    # Find the user who owns this order
    user = await users_col.find_one({
        "active_orders.id": request.order_id
    })

    if not user:
        raise HTTPException(status_code=404, detail="Order not found")

    now = datetime.utcnow().isoformat()

    # Update the specific order in user's active_orders
    updated_orders = []
    for order in user.get("active_orders", []):
        if order.get("id") == request.order_id:
            order["status"] = "approved"
            order["driver_name"] = request.driver_name
            order["driver_phone"] = request.driver_phone
            if order.get("type") == "donation":
                order["estimated_pickup"] = request.estimated_time
            else:
                order["estimated_delivery"] = request.estimated_time
            order["just_approved"] = True
            order["acknowledged"] = False
            order["approved_at"] = now
        updated_orders.append(order)

    # Update donation history if applicable
    updated_history = []
    for d in user.get("donation_history", []):
        if d.get("id") == request.order_id:
            d["status"] = "approved"
            d["driver_name"] = request.driver_name
            d["driver_phone"] = request.driver_phone
            d["estimated_pickup"] = request.estimated_time
        updated_history.append(d)

    # Add approval message
    new_message = {
        "id": int(datetime.utcnow().timestamp() * 1000),
        "type": "approval",
        "title": "Order Approved",
        "content": f"Your order has been approved! Driver: {request.driver_name}",
        "order_id": request.order_id,
        "timestamp": now,
        "read": False,
    }

    messages = user.get("messages", [])
    messages.append(new_message)

    await users_col.update_one(
        {"email": user["email"]},
        {"$set": {
            "active_orders": updated_orders,
            "donation_history": updated_history,
            "messages": messages,
            "updated_at": now,
        }}
    )

    return {"message": "Order approved successfully"}


@router.post("/reject-order")
async def reject_order(order_id: str, current_admin: dict = Depends(get_current_admin)):
    """Reject a pending order."""
    users_col = get_users_collection()

    user = await users_col.find_one({"active_orders.id": order_id})
    if not user:
        raise HTTPException(status_code=404, detail="Order not found")

    now = datetime.utcnow().isoformat()
    updated_orders = []
    for order in user.get("active_orders", []):
        if order.get("id") == order_id:
            order["status"] = "rejected"
        updated_orders.append(order)

    updated_history = []
    for d in user.get("donation_history", []):
        if d.get("id") == order_id:
            d["status"] = "rejected"
        updated_history.append(d)

    await users_col.update_one(
        {"email": user["email"]},
        {"$set": {
            "active_orders": updated_orders,
            "donation_history": updated_history,
            "updated_at": now,
        }}
    )

    return {"message": "Order rejected"}


@router.post("/complete-order")
async def complete_order(order_id: str, current_admin: dict = Depends(get_current_admin)):
    """Mark an order as completed (admin action)."""
    users_col = get_users_collection()

    user = await users_col.find_one({"active_orders.id": order_id})
    if not user:
        raise HTTPException(status_code=404, detail="Order not found")

    now = datetime.utcnow().isoformat()
    updated_orders = []
    for order in user.get("active_orders", []):
        if order.get("id") == order_id:
            order["status"] = "completed"
            order["acknowledged"] = False
        updated_orders.append(order)

    updated_history = []
    for d in user.get("donation_history", []):
        if d.get("id") == order_id:
            d["status"] = "completed"
        updated_history.append(d)

    # Add completion message
    new_message = {
        "id": int(datetime.utcnow().timestamp() * 1000),
        "type": "completion",
        "title": "Order Completed",
        "content": f"Your order has been completed on {now}. Thank you for your contribution!",
        "order_id": order_id,
        "timestamp": now,
        "read": False,
    }

    messages = user.get("messages", [])
    messages.append(new_message)

    await users_col.update_one(
        {"email": user["email"]},
        {"$set": {
            "active_orders": updated_orders,
            "donation_history": updated_history,
            "messages": messages,
            "updated_at": now,
        }}
    )

    return {"message": "Order marked as completed"}


@router.delete("/user")
async def delete_user(request: DeleteUserRequest, current_admin: dict = Depends(get_current_admin)):
    """Delete a user by email."""
    users_col = get_users_collection()
    result = await users_col.delete_one({"email": request.user_email})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}


# ========== Driver Management ==========

@router.get("/drivers")
async def get_all_drivers(current_admin: dict = Depends(get_current_admin)):
    """Get list of all drivers."""
    drivers_col = get_drivers_collection()
    drivers = []
    async for driver in drivers_col.find({}):
        drivers.append({
            "id": str(driver["_id"]),
            "name": driver.get("name", ""),
            "username": driver.get("username", ""),
            "phone": driver.get("phone", ""),
        })
    return {"drivers": drivers}


@router.post("/drivers", status_code=status.HTTP_201_CREATED)
async def create_driver(request: CreateDriverRequest, current_admin: dict = Depends(get_current_admin)):
    """Create/assign a new driver."""
    drivers_col = get_drivers_collection()

    # Check if username exists
    existing = await drivers_col.find_one({"username": request.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    driver_doc = {
        "name": request.name,
        "username": request.username,
        "password": hash_password(request.password),
        "phone": request.phone,
        "created_at": datetime.utcnow().isoformat(),
    }

    result = await drivers_col.insert_one(driver_doc)

    return {
        "message": "Driver assigned successfully",
        "driver": {
            "id": str(result.inserted_id),
            "name": request.name,
            "username": request.username,
            "phone": request.phone,
        }
    }


@router.delete("/drivers")
async def delete_driver(request: DeleteDriverRequest, current_admin: dict = Depends(get_current_admin)):
    """Delete a driver by username."""
    drivers_col = get_drivers_collection()
    result = await drivers_col.delete_one({"username": request.username})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Driver not found")

    return {"message": "Driver removed successfully"}
