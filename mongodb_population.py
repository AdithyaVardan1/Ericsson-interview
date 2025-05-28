
import pymongo
from datetime import datetime, timedelta
import random

client = pymongo.MongoClient("")
db = client["ecommerce_system"]

orders_collection = db["orders"]
products_collection = db["products"]
customers_collection = db["customers"]

orders_collection.delete_many({})
products_collection.delete_many({})
customers_collection.delete_many({})

sample_orders = [
    {
        "order_id": "ORD001",
        "customer_id": "CUST001",
        "status": "delivered",
        "items": [
            {"product_id": "PRD001", "quantity": 2, "price": 29.99},
            {"product_id": "PRD002", "quantity": 1, "price": 149.99}
        ],
        "total_amount": 209.97,
        "order_date": datetime.now() - timedelta(days=7),
        "shipping_address": "123 Main St, New York, NY",
        "can_cancel": False,
        "can_return": True
    },
    {
        "order_id": "ORD002",
        "customer_id": "CUST002",
        "status": "processing",
        "items": [
            {"product_id": "PRD003", "quantity": 1, "price": 89.99}
        ],
        "total_amount": 89.99,
        "order_date": datetime.now() - timedelta(days=1),
        "shipping_address": "456 Oak Ave, Los Angeles, CA",
        "can_cancel": True,
        "can_return": False
    },
    {
        "order_id": "ORD003",
        "customer_id": "CUST003",
        "status": "shipped",
        "items": [
            {"product_id": "PRD004", "quantity": 3, "price": 19.99}
        ],
        "total_amount": 59.97,
        "order_date": datetime.now() - timedelta(days=3),
        "shipping_address": "789 Pine St, Chicago, IL",
        "can_cancel": False,
        "can_return": True
    },
    {
        "order_id": "ORD004",
        "customer_id": "CUST001",
        "status": "pending",
        "items": [
            {"product_id": "PRD005", "quantity": 1, "price": 299.99}
        ],
        "total_amount": 299.99,
        "order_date": datetime.now(),
        "shipping_address": "123 Main St, New York, NY",
        "can_cancel": True,
        "can_return": False
    }
]

sample_products = [
    {
        "product_id": "PRD001",
        "name": "Wireless Bluetooth Headphones",
        "category": "Electronics",
        "price": 29.99,
        "availability": 150,
        "description": "High-quality wireless headphones with noise cancellation",
        "recommendations": ["PRD002", "PRD003"],
        "weather_suitable": ["all_weather"]
    },
    {
        "product_id": "PRD002",
        "name": "Smart Fitness Watch",
        "category": "Electronics",
        "price": 149.99,
        "availability": 75,
        "description": "Advanced fitness tracking with heart rate monitor",
        "recommendations": ["PRD001", "PRD006"],
        "weather_suitable": ["all_weather"]
    },
    {
        "product_id": "PRD003",
        "name": "Portable Phone Charger",
        "category": "Electronics",
        "price": 89.99,
        "availability": 200,
        "description": "20000mAh power bank with fast charging",
        "recommendations": ["PRD001", "PRD002"],
        "weather_suitable": ["all_weather"]
    },
    {
        "product_id": "PRD004",
        "name": "Waterproof Jacket",
        "category": "Clothing",
        "price": 19.99,
        "availability": 50,
        "description": "Lightweight waterproof jacket for outdoor activities",
        "recommendations": ["PRD005", "PRD007"],
        "weather_suitable": ["rainy", "snowy"]
    },
    {
        "product_id": "PRD005",
        "name": "Hiking Boots",
        "category": "Footwear",
        "price": 299.99,
        "availability": 30,
        "description": "Durable hiking boots with ankle support",
        "recommendations": ["PRD004", "PRD008"],
        "weather_suitable": ["all_weather", "rainy"]
    },
    {
        "product_id": "PRD006",
        "name": "Yoga Mat",
        "category": "Fitness",
        "price": 24.99,
        "availability": 100,
        "description": "Non-slip yoga mat for home workouts",
        "recommendations": ["PRD002"],
        "weather_suitable": ["all_weather"]
    },
    {
        "product_id": "PRD007",
        "name": "Umbrella",
        "category": "Accessories",
        "price": 15.99,
        "availability": 80,
        "description": "Compact foldable umbrella",
        "recommendations": ["PRD004"],
        "weather_suitable": ["rainy"]
    },
    {
        "product_id": "PRD008",
        "name": "Thermal Gloves",
        "category": "Clothing",
        "price": 12.99,
        "availability": 60,
        "description": "Insulated gloves for cold weather",
        "recommendations": ["PRD005", "PRD004"],
        "weather_suitable": ["cold", "snowy"]
    }
]

sample_customers = [
    {
        "customer_id": "CUST001",
        "name": "John Smith",
        "email": "john.smith@email.com",
        "age": 32,
        "preferences": ["Electronics", "Fitness"],
        "loyalty_points": 1250,
        "membership_tier": "Gold",
        "location": "New York, NY"
    },
    {
        "customer_id": "CUST002",
        "name": "Sarah Johnson",
        "email": "sarah.j@email.com",
        "age": 28,
        "preferences": ["Clothing", "Accessories"],
        "loyalty_points": 850,
        "membership_tier": "Silver",
        "location": "Los Angeles, CA"
    },
    {
        "customer_id": "CUST003",
        "name": "Mike Davis",
        "email": "mike.davis@email.com",
        "age": 45,
        "preferences": ["Footwear", "Outdoor"],
        "loyalty_points": 2100,
        "membership_tier": "Platinum",
        "location": "Chicago, IL"
    },
    {
        "customer_id": "CUST004",
        "name": "Emma Wilson",
        "email": "emma.w@email.com",
        "age": 24,
        "preferences": ["Electronics", "Fitness"],
        "loyalty_points": 450,
        "membership_tier": "Bronze",
        "location": "Miami, FL"
    }
]

orders_collection.insert_many(sample_orders)
products_collection.insert_many(sample_products)
customers_collection.insert_many(sample_customers)

print("✅ MongoDB populated with sample data!")
print(f"Orders: {orders_collection.count_documents({})}")
print(f"Products: {products_collection.count_documents({})}")
print(f"Customers: {customers_collection.count_documents({})}")