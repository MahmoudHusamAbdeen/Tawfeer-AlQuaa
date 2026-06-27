"""
Tawfeer Backend - MongoDB Database Connection
"""

from motor.motor_asyncio import AsyncIOMotorClient
from app.config import get_settings
from typing import Optional
import traceback

client: Optional[AsyncIOMotorClient] = None
database = None
_db_connected = False


async def connect_to_mongo():
    """Connect to MongoDB - won't crash if auth fails"""
    global client, database, _db_connected
    settings = get_settings()

    try:
        connection_uri = settings.MONGODB_URI
        if "authSource" not in connection_uri:
            separator = "&" if "?" in connection_uri else "?"
            connection_uri = f"{connection_uri}{separator}authSource=admin"

        client = AsyncIOMotorClient(
            connection_uri,
            serverSelectionTimeoutMS=15000,
            connectTimeoutMS=15000,
        )
        database = client[settings.MONGODB_DB_NAME]

        # Test connection
        await client.admin.command("ping")
        _db_connected = True
        print(f"[DB] Connected to MongoDB, database: {settings.MONGODB_DB_NAME}")

    except Exception as e:
        print(f"[DB ERROR] MongoDB connection failed: {e}")
        print("[DB WARNING] Server will start WITHOUT database connection")
        print("[DB WARNING] Fix MongoDB Atlas permissions and restart")
        _db_connected = False
        # DON'T raise — let the server start anyway

    # Try indexes only if connected
    if _db_connected:
        try:
            await create_indexes()
        except Exception as idx_err:
            print(f"[DB WARNING] Index creation failed: {idx_err}")


async def close_mongo_connection():
    """Disconnect from MongoDB"""
    global client
    if client:
        client.close()
        print("[DB] Disconnected from MongoDB")


async def create_indexes():
    """Create database indexes — each one wrapped safely"""
    if database is None:
        return

    collections_indexes = {
        "users": [
            {"keys": "email", "kwargs": {"unique": True}},
            {"keys": "username", "kwargs": {"unique": True}},
        ],
        "donations": [
            {"keys": "donor_id", "kwargs": {}},
            {"keys": "status", "kwargs": {}},
        ],
        "food_requests": [
            {"keys": "requester_id", "kwargs": {}},
            {"keys": "status", "kwargs": {}},
        ],
        "recipes": [
            {"keys": "user_id", "kwargs": {}},
            {"keys": "category", "kwargs": {}},
        ],
        "shopping_lists": [
            {"keys": "user_id", "kwargs": {}},
        ],
        "meal_plans": [
            {"keys": "user_id", "kwargs": {}},
        ],
        "favorites": [
            {"keys": [("user_id", 1), ("recipe_id", 1)], "kwargs": {"unique": True}},
        ],
        "drivers": [
            {"keys": "email", "kwargs": {"unique": True}},
        ],
        "orders": [
            {"keys": "driver_id", "kwargs": {}},
            {"keys": "status", "kwargs": {}},
        ],
    }

    for coll_name, indexes in collections_indexes.items():
        try:
            collection = database[coll_name]
            for idx in indexes:
                await collection.create_index(idx["keys"], **idx["kwargs"])
            print(f"[DB] ✓ {coll_name} indexes")
        except Exception as e:
            print(f"[DB] ✗ {coll_name} indexes: {e}")


# =============================================
# COLLECTION GETTERS
# =============================================

def get_database():
    return database

def get_users_collection():
    return database.users if database is not None else None

def get_donations_collection():
    return database.donations if database is not None else None

def get_food_requests_collection():
    return database.food_requests if database is not None else None

def get_recipes_collection():
    return database.recipes if database is not None else None

def get_shopping_lists_collection():
    return database.shopping_lists if database is not None else None

def get_meal_plans_collection():
    return database.meal_plans if database is not None else None

def get_favorites_collection():
    return database.favorites if database is not None else None

def get_drivers_collection():
    return database.drivers if database is not None else None

def get_orders_collection():
    return database.orders if database is not None else None