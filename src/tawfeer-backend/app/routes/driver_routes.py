"""
Tawfeer Backend - Driver Routes
Driver dashboard: view assigned orders, update delivery status, award points.
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends

from app.database import get_users_collection
from app.models.donation import UpdateOrderStatusRequest
from app.services.auth import get_current_driver

router = APIRouter(prefix="/api/driver", tags=["Driver"])


@router.get("/orders")
async def get_driver_orders(current_driver: dict = Depends(get_current_driver)):
    """
    Get all orders available for the driver (approved or in-progress).

    Returns orders from all users that are in approved or in_progress status.
    """
    users_col = get_users_collection()
    all_orders = []

    async for user in users_col.find({}):
        for order in user.get("active_orders", []):
            if order.get("status") in ["approved", "in_progress"]:
                all_orders.append({
                    **order,
                    "user_name": user.get("name", ""),
                    "user_email": user.get("email", ""),
                    "user_phone": user.get("phone", ""),
                    "user_type": user.get("type", ""),
                    "current_points": user.get("points", 0),
                })

    # Sort by date descending
    all_orders.sort(key=lambda x: x.get("date", ""), reverse=True)
    return {"orders": all_orders}


@router.post("/update-status")
async def update_order_status(request: UpdateOrderStatusRequest, current_driver: dict = Depends(get_current_driver)):
    """
    Update the status of an order (driver action).

    - Mark as 'in_progress' when starting delivery
    - Mark as 'completed' when delivery is done, with optional points to award
    """
    users_col = get_users_collection()

    user = await users_col.find_one({"email": request.user_email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    now = datetime.utcnow().isoformat()
    driver_name = current_driver.get("name", "")
    driver_phone = ""

    # Get driver phone from drivers collection
    from app.database import get_drivers_collection
    drivers_col = get_drivers_collection()
    driver_doc = await drivers_col.find_one({"username": current_driver.get("email", "")})
    if driver_doc:
        driver_phone = driver_doc.get("phone", "")

    points = request.points_to_award if request.new_status == "completed" else 0

    # Update orders
    updated_orders = []
    for order in user.get("active_orders", []):
        if order.get("id") == request.order_id:
            order["status"] = request.new_status
            order["driver_name"] = driver_name
            order["driver_phone"] = driver_phone
            order["delivery_notes"] = request.delivery_notes
            order["driver_location"] = request.driver_location
            order["updated_at"] = now

            if request.new_status == "completed":
                order["points_earned"] = points
                order["acknowledged"] = False
                order["completed_at"] = now
            break
        updated_orders.append(order)

    # Ensure the modified order is included
    found = any(o.get("id") == request.order_id for o in updated_orders)
    if not found:
        for order in user.get("active_orders", []):
            if order.get("id") == request.order_id:
                updated_orders.append(order)

    # Update donation history if applicable
    updated_history = []
    for d in user.get("donation_history", []):
        if d.get("id") == request.order_id:
            d["status"] = request.new_status
            if request.new_status == "completed":
                d["points_earned"] = points
                d["driver_name"] = driver_name
                d["driver_phone"] = driver_phone
        updated_history.append(d)

    # Update user points if completing
    new_points = user.get("points", 0)
    if request.new_status == "completed" and points > 0:
        new_points += points

    # Add status update message
    message_title = f"Order Completed - {points} Points Awarded!" if request.new_status == "completed" else f"Order {request.new_status}"
    message_content = (
        f"Your order has been completed. You've been awarded {points} points by driver {driver_name}."
        if request.new_status == "completed"
        else f"Your order has been marked as {request.new_status} by driver {driver_name}."
    )

    new_message = {
        "id": int(datetime.utcnow().timestamp() * 1000),
        "type": "status_update",
        "title": message_title,
        "content": message_content,
        "order_id": request.order_id,
        "timestamp": now,
        "read": False,
    }

    messages = user.get("messages", [])
    messages.append(new_message)

    await users_col.update_one(
        {"email": request.user_email},
        {"$set": {
            "active_orders": user.get("active_orders", []),  # Will be updated below
            "donation_history": updated_history,
            "messages": messages,
            "points": new_points,
            "updated_at": now,
        }}
    )

    # Do a proper update for the specific order
    # Re-fetch and update correctly
    await users_col.update_one(
        {"email": request.user_email, "active_orders.id": request.order_id},
        {
            "$set": {
                "active_orders.$.status": request.new_status,
                "active_orders.$.driver_name": driver_name,
                "active_orders.$.driver_phone": driver_phone,
                "active_orders.$.delivery_notes": request.delivery_notes,
                "active_orders.$.driver_location": request.driver_location,
                "active_orders.$.points_earned": points,
                "active_orders.$.acknowledged": False if request.new_status == "completed" else True,
                "active_orders.$.updated_at": now,
            }
        }
    )

    result_msg = f"Order status updated to {request.new_status}"
    if points > 0:
        result_msg += f" and {points} points awarded"

    return {"message": result_msg, "points_awarded": points}


@router.get("/stats")
async def get_driver_stats(current_driver: dict = Depends(get_current_driver)):
    """Get driver-specific statistics."""
    users_col = get_users_collection()

    total_approved = 0
    total_in_progress = 0

    async for user in users_col.find({}):
        for order in user.get("active_orders", []):
            if order.get("status") == "approved":
                total_approved += 1
            elif order.get("status") == "in_progress":
                total_in_progress += 1

    return {
        "active_orders": total_approved + total_in_progress,
        "pending_pickup": total_approved,
        "in_progress": total_in_progress,
    }
