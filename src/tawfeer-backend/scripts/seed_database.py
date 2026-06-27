#!/usr/bin/env python3
"""
Tawfeer Backend - Database Seeding Script
Run this script to add sample data to MongoDB for testing.
Usage: python scripts/seed_database.py
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB_NAME", "tawfeer")


async def seed():
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]

    print(f"Seeding database: {DB_NAME}")

    # Clear existing data
    await db.users.delete_many({})
    await db.drivers.delete_many({})
    await db.donations.delete_many({})
    await db.food_requests.delete_many({})

    # Create sample users
    sample_users = [
        {
            "name": "Ahmed Al Mansouri",
            "email": "ahmed@example.com",
            "phone": "+971501234567",
            "password": pwd_context.hash("123"),
            "type": "Household",
            "points": 80,
            "donation_history": [
                {
                    "id": "1001",
                    "date": "2026-05-01T10:00:00",
                    "food_type": "Rice and Chicken",
                    "people": 5,
                    "status": "completed",
                    "points_earned": 20,
                    "driver_name": "Mohammed",
                    "driver_phone": "+971509876543",
                    "estimated_pickup": "2 hours",
                    "location": "Dubai Marina",
                    "description": "Leftover biryani from family gathering",
                    "is_new": False,
                    "is_consumable": True,
                    "is_cooked": True,
                }
            ],
            "active_orders": [],
            "messages": [
                {
                    "id": 1,
                    "type": "approval",
                    "title": "Order Approved",
                    "content": "Your donation has been approved! Driver: Mohammed",
                    "order_id": "1001",
                    "timestamp": "2026-05-01T11:00:00",
                    "read": True,
                }
            ],
            "address": "Dubai Marina, Dubai",
            "created_at": "2026-04-15T09:00:00",
            "updated_at": "2026-05-01T11:00:00",
        },
        {
            "name": "Fatima Al Zaabi",
            "email": "fatima@example.com",
            "phone": "+971507654321",
            "password": pwd_context.hash("123"),
            "type": "Restaurant",
            "points": 120,
            "donation_history": [
                {
                    "id": "1002",
                    "date": "2026-05-05T14:00:00",
                    "food_type": "Fresh Vegetables",
                    "people": 10,
                    "status": "completed",
                    "points_earned": 20,
                    "location": "Abu Dhabi City",
                    "is_new": True,
                    "is_consumable": True,
                    "is_cooked": False,
                },
                {
                    "id": "1003",
                    "date": "2026-05-10T16:00:00",
                    "food_type": "Cooked Meals",
                    "people": 8,
                    "status": "approved",
                    "points_earned": 0,
                    "driver_name": "Ali",
                    "location": "Abu Dhabi City",
                    "is_new": False,
                    "is_consumable": True,
                    "is_cooked": True,
                },
            ],
            "active_orders": [
                {
                    "id": "1003",
                    "type": "donation",
                    "date": "2026-05-10T16:00:00",
                    "status": "approved",
                    "people": 8,
                    "food_type": "Cooked Meals",
                    "location": "Abu Dhabi City",
                    "driver_name": "Ali",
                    "driver_phone": "+971501112222",
                    "estimated_pickup": "1 hour",
                    "just_approved": True,
                    "acknowledged": False,
                    "points_earned": 0,
                }
            ],
            "messages": [
                {
                    "id": 2,
                    "type": "approval",
                    "title": "Order Approved",
                    "content": "Your donation has been approved! Driver: Ali",
                    "order_id": "1003",
                    "timestamp": "2026-05-10T17:00:00",
                    "read": False,
                }
            ],
            "address": "Abu Dhabi City",
            "created_at": "2026-04-20T11:00:00",
            "updated_at": "2026-05-10T17:00:00",
        },
        {
            "name": "Saeed Electronics LLC",
            "email": "saeed@company.com",
            "phone": "+971509998877",
            "password": pwd_context.hash("123"),
            "type": "Organization",
            "points": 40,
            "donation_history": [],
            "active_orders": [],
            "messages": [],
            "address": "Sharjah",
            "created_at": "2026-05-01T08:00:00",
            "updated_at": "2026-05-01T08:00:00",
        },
    ]

    result = await db.users.insert_many(sample_users)
    print(f"  Created {len(result.inserted_ids)} sample users")

    # Create sample drivers
    sample_drivers = [
        {
            "name": "Mohammed Hassan",
            "username": "driver1",
            "password": pwd_context.hash("123"),
            "phone": "+971509876543",
            "created_at": "2026-04-10T09:00:00",
        },
        {
            "name": "Ali Reza",
            "username": "driver2",
            "password": pwd_context.hash("123"),
            "phone": "+971501112222",
            "created_at": "2026-04-12T09:00:00",
        },
    ]

    result = await db.drivers.insert_many(sample_drivers)
    print(f"  Created {len(result.inserted_ids)} sample drivers")

    # Create indexes
    await db.users.create_index("email", unique=True)
    await db.drivers.create_index("username", unique=True)
    print("  Database indexes created")

    print("\nSeeding complete!")
    print("\nTest accounts:")
    print("  User:   ahmed@example.com / 123")
    print("  User:   fatima@example.com / 123")
    print("  User:   saeed@company.com / 123")
    print("  Admin:  admin123 / 123")
    print("  Gov:    gov123 / 123")
    print("  Driver: driver1 / 123")
    print("  Driver: driver2 / 123")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
