"""
Tawfeer Backend - Government Dashboard Routes
Government analytics: statistics, charts, environmental impact, activities.
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional

from app.database import get_users_collection, get_donations_collection, get_food_requests_collection
from app.services.auth import get_current_government

router = APIRouter(prefix="/api/government", tags=["Government"])


@router.get("/stats")
async def get_government_stats(current_gov: dict = Depends(get_current_government)):
    """
    Get government dashboard statistics.

    Returns key metrics including total users, donations, points,
    growth rates, environmental impact, and recent activities.
    """
    users_col = get_users_collection()
    donations_col = get_donations_collection()

    users = []
    async for user in users_col.find({}):
        users.append(user)

    all_donations = []
    async for donation in donations_col.find({}):
        all_donations.append(donation)

    # Calculate totals
    total_points = sum(u.get("points", 0) for u in users)
    total_donations = len(all_donations)

    # Environmental impact (estimated based on donations)
    waste_reduced = total_donations * 2.5  # kg per donation
    co2_saved = total_donations * 4.2  # kg CO2 per donation
    water_saved = total_donations * 1000  # liters per donation

    # Growth calculation
    now = datetime.utcnow()
    one_week_ago = (now - timedelta(days=7)).isoformat()
    two_weeks_ago = (now - timedelta(days=14)).isoformat()

    current_week_users = sum(1 for u in users if u.get("created_at", "") >= one_week_ago)
    previous_week_users = sum(1 for u in users if two_weeks_ago <= u.get("created_at", "") < one_week_ago)

    user_growth = 0
    if previous_week_users > 0:
        user_growth = round(((current_week_users - previous_week_users) / previous_week_users) * 100, 1)
    elif current_week_users > 0:
        user_growth = 100

    current_week_donations = sum(1 for d in all_donations if d.get("created_at", "") >= one_week_ago)
    previous_week_donations = sum(1 for d in all_donations if two_weeks_ago <= d.get("created_at", "") < one_week_ago)

    donation_growth = 0
    if previous_week_donations > 0:
        donation_growth = round(((current_week_donations - previous_week_donations) / previous_week_donations) * 100, 1)
    elif current_week_donations > 0:
        donation_growth = 100

    return {
        "total_users": len(users),
        "total_donations": total_donations,
        "total_points": total_points,
        "user_growth": user_growth,
        "donation_growth": donation_growth,
        "environmental_impact": {
            "waste_reduced": round(waste_reduced, 1),
            "co2_saved": round(co2_saved, 1),
            "water_saved": round(water_saved),
        },
    }


@router.get("/charts")
async def get_chart_data(
    view_mode: str = "weekly",
    current_gov: dict = Depends(get_current_government)
):
    """
    Get chart data for donations and user growth.

    - **view_mode**: 'weekly' or 'monthly'
    """
    users_col = get_users_collection()
    donations_col = get_donations_collection()

    users = []
    async for user in users_col.find({}):
        users.append(user)

    all_donations = []
    async for donation in donations_col.find({}):
        all_donations.append(donation)

    now = datetime.utcnow()

    if view_mode == "weekly":
        donation_data = _generate_weekly_data(all_donations, now)
        user_data = _generate_weekly_data(
            [{"date": u.get("created_at", "")} for u in users],
            now
        )
    else:
        donation_data = _generate_monthly_data(all_donations, now)
        user_data = _generate_monthly_data(
            [{"date": u.get("created_at", "")} for u in users],
            now
        )

    return {
        "view_mode": view_mode,
        "donations": donation_data,
        "users": user_data,
    }


@router.get("/activities")
async def get_recent_activities(
    limit: int = 10,
    current_gov: dict = Depends(get_current_government)
):
    """Get recent activities across the platform."""
    users_col = get_users_collection()
    donations_col = get_donations_collection()

    activities = []

    # Get recent donations
    async for donation in donations_col.find({}).sort("created_at", -1).limit(limit):
        activities.append({
            "type": "donation",
            "user_name": donation.get("user_name", ""),
            "date": donation.get("created_at", ""),
            "status": donation.get("status", ""),
            "food_type": donation.get("food_type", ""),
        })

    # Get recent user registrations
    async for user in users_col.find({}).sort("created_at", -1).limit(limit):
        activities.append({
            "type": "registration",
            "user_name": user.get("name", ""),
            "date": user.get("created_at", ""),
            "user_type": user.get("type", ""),
        })

    # Sort by date and limit
    activities.sort(key=lambda x: x.get("date", ""), reverse=True)
    return {"activities": activities[:limit]}


@router.get("/top-users")
async def get_top_users(
    limit: int = 10,
    current_gov: dict = Depends(get_current_government)
):
    """Get top users by points."""
    users_col = get_users_collection()
    users = []
    async for user in users_col.find({}).sort("points", -1).limit(limit):
        users.append({
            "name": user.get("name", ""),
            "email": user.get("email", ""),
            "points": user.get("points", 0),
            "type": user.get("type", ""),
            "donation_count": len(user.get("donation_history", [])),
        })

    return {"top_users": users}


# ========== Helper Functions ==========

def _generate_weekly_data(items: list, now: datetime) -> list:
    """Generate weekly chart data starting from Friday."""
    current_day = now.weekday()  # 0=Monday
    # Calculate last Friday
    days_since_friday = (current_day - 4) % 7
    last_friday = now - timedelta(days=days_since_friday)

    data = []
    for i in range(5, -1, -1):
        week_start = last_friday - timedelta(weeks=i)
        week_end = week_start + timedelta(days=6)

        count = sum(1 for item in items
                    if week_start.isoformat() <= item.get("date", "") <= week_end.isoformat())

        data.append({
            "week": f"{week_start.month}/{week_start.day}",
            "count": count,
        })

    return data


def _generate_monthly_data(items: list, now: datetime) -> list:
    """Generate monthly chart data."""
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data = []

    for i in range(5, -1, -1):
        target = now - timedelta(days=i * 30)
        month_index = target.month - 1
        year = target.year

        count = sum(1 for item in items
                    if item.get("date", "")[:7] == f"{year}-{target.month:02d}")

        data.append({
            "week": month_names[month_index],
            "count": count,
        })

    return data
