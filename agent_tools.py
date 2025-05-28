import requests
import pymongo
from datetime import datetime
from langchain.tools import tool
from typing import Optional, List, Dict, Any


client = pymongo.MongoClient("")
db = client["ecommerce_system"]


@tool
def check_order_status(order_id: str) -> str:
    """Check the status of an order by order ID."""
    try:
        order = db.orders.find_one({"order_id": order_id})
        if not order:
            return f"Order {order_id} not found."
        
        return f"""
Order ID: {order['order_id']}
Status: {order['status'].upper()}
Customer: {order['customer_id']}
Total Amount: ${order['total_amount']}
Order Date: {order['order_date'].strftime('%Y-%m-%d')}
Items: {len(order['items'])} item(s)
Shipping Address: {order['shipping_address']}
Can Cancel: {'Yes' if order['can_cancel'] else 'No'}
Can Return: {'Yes' if order['can_return'] else 'No'}
        """.strip()
    except Exception as e:
        return f"Error checking order status: {str(e)}"

@tool
def cancel_order(order_id: str) -> str:
    """Cancel an order if it meets business rules (can_cancel = True)."""
    try:
        order = db.orders.find_one({"order_id": order_id})
        if not order:
            return f"Order {order_id} not found."
        
        if not order['can_cancel']:
            return f"Order {order_id} cannot be cancelled. Status: {order['status']}"
        
        result = db.orders.update_one(
            {"order_id": order_id},
            {"$set": {"status": "cancelled", "cancelled_date": datetime.now()}}
        )
        
        if result.modified_count > 0:
            return f"Order {order_id} has been successfully cancelled."
        else:
            return f"Failed to cancel order {order_id}."
            
    except Exception as e:
        return f"Error cancelling order: {str(e)}"

@tool
def process_return(order_id: str, reason: str = "Customer request") -> str:
    """Process a return/refund for an order if eligible."""
    try:
        order = db.orders.find_one({"order_id": order_id})
        if not order:
            return f"Order {order_id} not found."
        
        if not order['can_return']:
            return f"Order {order_id} is not eligible for return. Status: {order['status']}"
        
        result = db.orders.update_one(
            {"order_id": order_id},
            {"$set": {
                "status": "returned", 
                "return_date": datetime.now(),
                "return_reason": reason
            }}
        )
        
        if result.modified_count > 0:
            return f"Return processed for order {order_id}. Refund of ${order['total_amount']} will be processed within 3-5 business days. Reason: {reason}"
        else:
            return f"Failed to process return for order {order_id}."
            
    except Exception as e:
        return f"Error processing return: {str(e)}"

@tool
def search_products(query: str, category: Optional[str] = None) -> str:
    """Search products by name or category."""
    try:
        search_filter = {}
        
        if query:
            search_filter["$or"] = [
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}}
            ]
        
        if category:
            search_filter["category"] = {"$regex": category, "$options": "i"}
        
        products = list(db.products.find(search_filter, {"_id": 0}).limit(10))
        
        if not products:
            return f"No products found for query: {query}"
        
        result = f"Found {len(products)} products:\n\n"
        for product in products:
            result += f"• {product['name']} ({product['product_id']})\n"
            result += f"  Category: {product['category']} | Price: ${product['price']} | Available: {product['availability']}\n"
            result += f"  Description: {product['description']}\n\n"
        
        return result.strip()
        
    except Exception as e:
        return f"Error searching products: {str(e)}"

@tool
def get_product_details(product_id: str) -> str:
    """Get detailed information about a specific product."""
    try:
        product = db.products.find_one({"product_id": product_id}, {"_id": 0})
        if not product:
            return f"Product {product_id} not found."
        
        return f"""
Product ID: {product['product_id']}
Name: {product['name']}
Category: {product['category']}
Price: ${product['price']}
Availability: {product['availability']} units in stock
Description: {product['description']}
Weather Suitable: {', '.join(product['weather_suitable'])}
        """.strip()
        
    except Exception as e:
        return f"Error getting product details: {str(e)}"

@tool
def get_product_recommendations(product_id: str) -> str:
    """Get product recommendations based on a given product."""
    try:
        product = db.products.find_one({"product_id": product_id})
        if not product:
            return f"Product {product_id} not found."
        
        recommended_ids = product.get('recommendations', [])
        if not recommended_ids:
            return f"No recommendations available for {product['name']}"
        
        recommended_products = list(db.products.find(
            {"product_id": {"$in": recommended_ids}}, 
            {"_id": 0}
        ))
        
        result = f"Recommendations for {product['name']}:\n\n"
        for rec_product in recommended_products:
            result += f"• {rec_product['name']} ({rec_product['product_id']})\n"
            result += f"  Price: ${rec_product['price']} | Available: {rec_product['availability']}\n"
            result += f"  {rec_product['description']}\n\n"
        
        return result.strip()
        
    except Exception as e:
        return f"Error getting recommendations: {str(e)}"


@tool
def get_customer_info(customer_id: str) -> str:
    """Retrieve customer information by customer ID."""
    try:
        customer = db.customers.find_one({"customer_id": customer_id}, {"_id": 0})
        if not customer:
            return f"Customer {customer_id} not found."
        
        return f"""
Customer ID: {customer['customer_id']}
Name: {customer['name']}
Email: {customer['email']}
Age: {customer['age']}
Location: {customer['location']}
Preferences: {', '.join(customer['preferences'])}
Loyalty Points: {customer['loyalty_points']} points
Membership Tier: {customer['membership_tier']}
        """.strip()
        
    except Exception as e:
        return f"Error getting customer info: {str(e)}"

@tool
def update_customer_preferences(customer_id: str, new_preferences: str) -> str:
    """Update customer preferences (comma-separated list)."""
    try:
        customer = db.customers.find_one({"customer_id": customer_id})
        if not customer:
            return f"Customer {customer_id} not found."
        
        preferences_list = [pref.strip() for pref in new_preferences.split(',')]
        
        result = db.customers.update_one(
            {"customer_id": customer_id},
            {"$set": {"preferences": preferences_list}}
        )
        
        if result.modified_count > 0:
            return f"Successfully updated preferences for {customer['name']} to: {', '.join(preferences_list)}"
        else:
            return f"Failed to update preferences for customer {customer_id}"
            
    except Exception as e:
        return f"Error updating customer preferences: {str(e)}"

@tool
def check_loyalty_points(customer_id: str) -> str:
    """Check customer's loyalty points and rewards."""
    try:
        customer = db.customers.find_one({"customer_id": customer_id})
        if not customer:
            return f"Customer {customer_id} not found."
        
        points = customer['loyalty_points']
        tier = customer['membership_tier']
        
        # Calculate available rewards based on points
        available_rewards = []
        if points >= 500:
            available_rewards.append("$5 discount coupon (500 points)")
        if points >= 1000:
            available_rewards.append("$10 discount coupon (1000 points)")
        if points >= 2000:
            available_rewards.append("Free shipping for 1 month (2000 points)")
        
        result = f"""
Customer: {customer['name']}
Current Loyalty Points: {points}
Membership Tier: {tier}
        """
        
        if available_rewards:
            result += f"\nAvailable Rewards:\n" + "\n".join([f"• {reward}" for reward in available_rewards])
        else:
            result += f"\nNo rewards available yet. Earn {500 - points} more points for first reward!"
        
        return result.strip()
        
    except Exception as e:
        return f"Error checking loyalty points: {str(e)}"

@tool
def get_current_weather(location: str) -> str:
    """Get current weather for shipping estimates and recommendations."""
    try:
        #simulated data here in this api for demo purposes
        # api_key = "your_openweather_api_key"
        # url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        
        weather_conditions = {
            "New York, NY": {"temp": 22, "condition": "rainy", "humidity": 78},
            "Los Angeles, CA": {"temp": 28, "condition": "sunny", "humidity": 45},
            "Chicago, IL": {"temp": 15, "condition": "cold", "humidity": 65},
            "Miami, FL": {"temp": 32, "condition": "sunny", "humidity": 82}
        }
        
        weather = weather_conditions.get(location, {"temp": 20, "condition": "mild", "humidity": 60})
        
        shipping_impact = "Normal delivery times expected"
        if weather["condition"] == "rainy":
            shipping_impact = "Possible 1-2 day delay due to weather"
        elif weather["condition"] == "snowy":
            shipping_impact = "Possible 2-3 day delay due to snow"
        
        return f"""
Weather in {location}:
Temperature: {weather['temp']}°C
Condition: {weather['condition'].title()}
Humidity: {weather['humidity']}%
Shipping Impact: {shipping_impact}
        """.strip()
        
    except Exception as e:
        return f"Error getting weather info: {str(e)}"

@tool
def get_weather_based_recommendations(location: str) -> str:
    """Get product recommendations based on current weather."""
    try:
        weather_conditions = {
            "New York, NY": "rainy",
            "Los Angeles, CA": "sunny", 
            "Chicago, IL": "cold",
            "Miami, FL": "sunny"
        }
        
        condition = weather_conditions.get(location, "mild")
        
        suitable_products = list(db.products.find(
            {"weather_suitable": {"$in": [condition, "all_weather"]}},
            {"_id": 0}
        ).limit(5))
        
        if not suitable_products:
            return f"No specific weather-based recommendations for {location}"
        
        result = f"Weather-based recommendations for {location} ({condition} weather):\n\n"
        for product in suitable_products:
            result += f"• {product['name']} - ${product['price']}\n"
            result += f"  Perfect for {condition} weather! {product['description']}\n\n"
        
        return result.strip()
        
    except Exception as e:
        return f"Error getting weather recommendations: {str(e)}"

order_tools = [check_order_status, cancel_order, process_return]

product_tools = [search_products, get_product_details, get_product_recommendations]

customer_tools = [get_customer_info, update_customer_preferences, check_loyalty_points]

weather_tools = [get_current_weather, get_weather_based_recommendations]
