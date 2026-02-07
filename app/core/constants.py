from datetime import datetime, timedelta
import bcrypt
from app.core.config import settings
# from app.core.security import hash_password

# =============================================================================
# ROLES & PERMISSIONS
# =============================================================================

ROLE_SUPERADMIN_ID = 1
ROLE_ADMIN_ID = 2
ROLE_MANAGER_ID = 3
ROLE_DRIVER_ID = 4
ROLE_CUSTOMER_ID = 5

DEFAULT_ROLES = [
    {"id": ROLE_SUPERADMIN_ID, "name": "Superadmin"},
    {"id": ROLE_ADMIN_ID, "name": "Admin"},
    {"id": ROLE_MANAGER_ID, "name": "Manager"},
    {"id": ROLE_DRIVER_ID, "name": "Driver"},
    {"id": ROLE_CUSTOMER_ID, "name": "Customer"},
]

DEFAULT_PERMISSIONS = [
    # =========================================================================
    # USER MANAGEMENT
    # =========================================================================
    {"id": 1, "name": "users.view_all", "description": "View all users", "category": "users"},
    {"id": 2, "name": "users.create", "description": "Create new users", "category": "users"},
    {"id": 3, "name": "users.edit", "description": "Edit user details", "category": "users"},
    {"id": 4, "name": "users.delete", "description": "Delete users", "category": "users"},
    {"id": 5, "name": "users.view_own", "description": "View own profile", "category": "users"},
    {"id": 6, "name": "users.edit_own", "description": "Edit own profile", "category": "users"},
    
    # =========================================================================
    # ROLE & PERMISSION MANAGEMENT
    # =========================================================================
    {"id": 7, "name": "roles.view", "description": "View roles", "category": "roles"},
    {"id": 8, "name": "roles.create", "description": "Create roles", "category": "roles"},
    {"id": 9, "name": "roles.edit", "description": "Edit roles", "category": "roles"},
    {"id": 10, "name": "roles.delete", "description": "Delete roles", "category": "roles"},
    {"id": 11, "name": "permissions.manage", "description": "Manage permissions", "category": "roles"},
    
    # =========================================================================
    # FOOD MENU MANAGEMENT
    # =========================================================================
    {"id": 12, "name": "foods.view", "description": "View food menu", "category": "foods"},
    {"id": 13, "name": "foods.create", "description": "Add new food items", "category": "foods"},
    {"id": 14, "name": "foods.edit", "description": "Edit food items", "category": "foods"},
    {"id": 15, "name": "foods.delete", "description": "Delete food items", "category": "foods"},
    {"id": 16, "name": "foods.toggle_availability", "description": "Toggle food availability", "category": "foods"},
    {"id": 17, "name": "foods.manage_categories", "description": "Manage food categories", "category": "foods"},
    
    # =========================================================================
    # ORDER MANAGEMENT
    # =========================================================================
    {"id": 18, "name": "orders.view_all", "description": "View all orders", "category": "orders"},
    {"id": 19, "name": "orders.view_own", "description": "View own orders", "category": "orders"},
    {"id": 20, "name": "orders.create", "description": "Create new orders", "category": "orders"},
    {"id": 21, "name": "orders.edit", "description": "Edit order details", "category": "orders"},
    {"id": 22, "name": "orders.cancel", "description": "Cancel orders", "category": "orders"},
    {"id": 23, "name": "orders.confirm", "description": "Confirm pending orders", "category": "orders"},
    {"id": 24, "name": "orders.update_status", "description": "Update order status", "category": "orders"},
    {"id": 25, "name": "orders.view_history", "description": "View order history", "category": "orders"},
    
    # =========================================================================
    # DRIVER MANAGEMENT
    # =========================================================================
    {"id": 26, "name": "drivers.view_all", "description": "View all drivers", "category": "drivers"},
    {"id": 27, "name": "drivers.create", "description": "Create driver accounts", "category": "drivers"},
    {"id": 28, "name": "drivers.edit", "description": "Edit driver details", "category": "drivers"},
    {"id": 29, "name": "drivers.delete", "description": "Delete drivers", "category": "drivers"},
    {"id": 30, "name": "drivers.update_status", "description": "Update any driver status", "category": "drivers"},
    {"id": 31, "name": "drivers.update_own_status", "description": "Update own driver status", "category": "drivers"},
    {"id": 32, "name": "drivers.view_performance", "description": "View driver performance metrics", "category": "drivers"},
    
    # =========================================================================
    # DELIVERY MANAGEMENT
    # =========================================================================
    {"id": 33, "name": "deliveries.view_all", "description": "View all deliveries", "category": "deliveries"},
    {"id": 34, "name": "deliveries.view_own", "description": "View own deliveries", "category": "deliveries"},
    {"id": 35, "name": "deliveries.assign", "description": "Assign deliveries to drivers", "category": "deliveries"},
    {"id": 36, "name": "deliveries.reassign", "description": "Reassign deliveries", "category": "deliveries"},
    {"id": 37, "name": "deliveries.update_status", "description": "Update delivery status", "category": "deliveries"},
    
    # =========================================================================
    # RESTAURANT MANAGEMENT
    # =========================================================================
    {"id": 38, "name": "restaurants.view", "description": "View restaurants", "category": "restaurants"},
    {"id": 39, "name": "restaurants.create", "description": "Add new restaurants", "category": "restaurants"},
    {"id": 40, "name": "restaurants.edit", "description": "Edit restaurant details", "category": "restaurants"},
    {"id": 41, "name": "restaurants.delete", "description": "Delete restaurants", "category": "restaurants"},
    
    # =========================================================================
    # PAYMENT MANAGEMENT
    # =========================================================================
    {"id": 42, "name": "payments.view_all", "description": "View all payments", "category": "payments"},
    {"id": 43, "name": "payments.view_own", "description": "View own payments", "category": "payments"},
    {"id": 44, "name": "payments.process", "description": "Process payments", "category": "payments"},
    {"id": 45, "name": "payments.refund", "description": "Process refunds", "category": "payments"},
    {"id": 46, "name": "payments.view_details", "description": "View payment details", "category": "payments"},
    
    # =========================================================================
    # OFFERS & COMBOS MANAGEMENT
    # =========================================================================
    {"id": 47, "name": "offers.view", "description": "View daily offers", "category": "offers"},
    {"id": 48, "name": "offers.create", "description": "Create daily offers", "category": "offers"},
    {"id": 49, "name": "offers.edit", "description": "Edit daily offers", "category": "offers"},
    {"id": 50, "name": "offers.delete", "description": "Delete daily offers", "category": "offers"},
    {"id": 51, "name": "offers.toggle_active", "description": "Activate/deactivate offers", "category": "offers"},
    
    {"id": 52, "name": "combos.view", "description": "View combo deals", "category": "combos"},
    {"id": 53, "name": "combos.create", "description": "Create combo deals", "category": "combos"},
    {"id": 54, "name": "combos.edit", "description": "Edit combo deals", "category": "combos"},
    {"id": 55, "name": "combos.delete", "description": "Delete combo deals", "category": "combos"},
    
    # =========================================================================
    # ANALYTICS & REPORTS
    # =========================================================================
    {"id": 56, "name": "analytics.view", "description": "View analytics dashboard", "category": "analytics"},
    {"id": 57, "name": "analytics.export", "description": "Export analytics data", "category": "analytics"},
    {"id": 58, "name": "reports.sales", "description": "View sales reports", "category": "analytics"},
    {"id": 59, "name": "reports.orders", "description": "View order reports", "category": "analytics"},
    {"id": 60, "name": "reports.drivers", "description": "View driver reports", "category": "analytics"},
    {"id": 61, "name": "reports.customers", "description": "View customer reports", "category": "analytics"},
    
    # =========================================================================
    # DASHBOARD ACCESS
    # =========================================================================
    {"id": 62, "name": "dashboard.admin", "description": "Access admin dashboard", "category": "dashboard"},
    {"id": 63, "name": "dashboard.manager", "description": "Access manager dashboard", "category": "dashboard"},
    {"id": 64, "name": "dashboard.driver", "description": "Access driver dashboard", "category": "dashboard"},
    {"id": 65, "name": "dashboard.customer", "description": "Access customer dashboard", "category": "dashboard"},
    
    # =========================================================================
    # ADDRESS MANAGEMENT
    # =========================================================================
    {"id": 66, "name": "addresses.view_own", "description": "View own addresses", "category": "addresses"},
    {"id": 67, "name": "addresses.create", "description": "Create addresses", "category": "addresses"},
    {"id": 68, "name": "addresses.edit_own", "description": "Edit own addresses", "category": "addresses"},
    {"id": 69, "name": "addresses.delete_own", "description": "Delete own addresses", "category": "addresses"},
]

# Role-Permission mappings based on frontend routes and features
DEFAULT_ROLE_PERMISSIONS = {
    # =========================================================================
    # SUPERADMIN - Full system access
    # =========================================================================
    ROLE_SUPERADMIN_ID: [p["id"] for p in DEFAULT_PERMISSIONS],
    
    # =========================================================================
    # ADMIN - System management (no role/permission management)
    # Route: /admin
    # Features: All management except roles/permissions
    # =========================================================================
    ROLE_ADMIN_ID: [
        # Users
        1, 2, 3, 4, 5, 6,
        # Foods
        12, 13, 14, 15, 16, 17,
        # Orders
        18, 20, 21, 22, 23, 24, 25,
        # Drivers
        26, 27, 28, 29, 30, 32,
        # Deliveries
        33, 35, 36, 37,
        # Restaurants
        38, 39, 40, 41,
        # Payments
        42, 44, 45, 46,
        # Offers & Combos
        47, 48, 49, 50, 51, 52, 53, 54, 55,
        # Analytics
        56, 57, 58, 59, 60, 61,
        # Dashboard
        62,
    ],
    
    # =========================================================================
    # MANAGER - Operations management
    # Route: /manager
    # Features: Orders, deliveries, food menu, daily operations
    # =========================================================================
    ROLE_MANAGER_ID: [
        # Users (view only)
        1, 5, 6,
        # Foods (full management)
        12, 13, 14, 15, 16, 17,
        # Orders (full management)
        18, 20, 21, 22, 23, 24, 25,
        # Drivers (view and assign)
        26, 30, 32,
        # Deliveries (full management)
        33, 35, 36, 37,
        # Restaurants (view and edit)
        38, 40,
        # Payments (view all)
        42, 46,
        # Offers & Combos (full management)
        47, 48, 49, 50, 51, 52, 53, 54, 55,
        # Analytics (view only)
        56, 58, 59, 60,
        # Dashboard
        63,
    ],
    
    # =========================================================================
    # DRIVER - Delivery operations
    # Route: /driver
    # Features: View assigned deliveries, update status, view own orders
    # =========================================================================
    ROLE_DRIVER_ID: [
        # Users (own profile only)
        5, 6,
        # Foods (view menu)
        12,
        # Orders (view assigned)
        19, 25,
        # Drivers (update own status)
        31,
        # Deliveries (own deliveries)
        34, 37,
        # Payments (own payments)
        43,
        # Offers (view only)
        47, 52,
        # Dashboard
        64,
    ],
    
    # =========================================================================
    # CUSTOMER - Ordering and tracking
    # Route: /customer
    # Features: Browse menu, place orders, track deliveries, manage profile
    # =========================================================================
    ROLE_CUSTOMER_ID: [
        # Users (own profile only)
        5, 6,
        # Foods (view menu)
        12,
        # Orders (own orders)
        19, 20, 22, 25,
        # Payments (own payments)
        43, 46,
        # Offers (view)
        47, 52,
        # Addresses (own addresses)
        66, 67, 68, 69,
        # Dashboard
        65,
    ],
}

# =============================================================================
# DEFAULT USERS
# =============================================================================

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

DEFAULT_USERS = [
    {
        "id": 1,
        "name": settings.SUPERADMIN_NAME,
        "email": settings.SUPERADMIN_EMAIL,
        "phone": settings.SUPERADMIN_PHONE,
        "password_hash": hash_password(settings.SUPERADMIN_PASSWORD),
        "role_id": ROLE_SUPERADMIN_ID
    },
    {
        "id": 2,
        "name": "Admin User",
        "email": "admin@demo.com",
        "phone": "+1555000100",
        "password_hash": hash_password("demo123"),
        "role_id": ROLE_ADMIN_ID,
    },
    {
        "id": 3,
        "name": "Sarah Manager",
        "email": "manager@demo.com",
        "phone": "+1555000102",
        "password_hash": hash_password("demo123"),
        "role_id": ROLE_MANAGER_ID,
    },
    {
        "id": 4,
        "name": "Mike Driver",
        "email": "driver@demo.com",
        "phone": "+1555000103",
        "password_hash": hash_password("demo123"),
        "role_id": ROLE_DRIVER_ID,
    },
    {
        "id": 5,
        "name": "Tom Rider",
        "email": "driver2@demo.com",
        "phone": "+1555000203",
        "password_hash": hash_password("demo123"),
        "role_id": ROLE_DRIVER_ID,
    },
    {
        "id": 6,
        "name": "Lisa Speed",
        "email": "driver3@demo.com",
        "phone": "+1555000303",
        "password_hash": hash_password("demo123"),
        "role_id": ROLE_DRIVER_ID,
    },
    {
        "id": 7,
        "name": "John Customer",
        "email": "customer@demo.com",
        "phone": "+1555000101",
        "password_hash": hash_password("demo123"),
        "role_id": ROLE_CUSTOMER_ID,
    },
    {
        "id": 8,
        "name": "Jane Smith",
        "email": "customer2@demo.com",
        "phone": "+1555000201",
        "password_hash": hash_password("demo123"),
        "role_id": ROLE_CUSTOMER_ID,
    },
    {
        "id": 9,
        "name": "Bob Wilson",
        "email": "customer3@demo.com",
        "phone": "+1555000301",
        "password_hash": hash_password("demo123"),
        "role_id": ROLE_CUSTOMER_ID,
    },
]

# =============================================================================
# DEFAULT DRIVERS
# =============================================================================

DEFAULT_DRIVERS = [
    {
        "id": 1,
        "user_id": 4,  # Mike Driver
        "status": "available",
        "created_at": datetime.now() - timedelta(days=100),
    },
    {
        "id": 2,
        "user_id": 5,  # Tom Rider
        "status": "available",
        "created_at": datetime.now() - timedelta(days=95),
    },
    {
        "id": 3,
        "user_id": 6,  # Lisa Speed
        "status": "available",
        "created_at": datetime.now() - timedelta(days=90),
    },
]

# =============================================================================
# DEFAULT RESTAURANTS
# =============================================================================

DEFAULT_RESTAURANTS = [
    {
        "id": 1,
        "name": "Burger Palace",
        "street": "123 Restaurant Ave",
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94102",
        "phone": "+1555100100",
    },
    {
        "id": 2,
        "name": "Pizza Paradise",
        "street": "789 Pizza Lane",
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94104",
        "phone": "+1555100200",
    },
    {
        "id": 3,
        "name": "Sushi Sensation",
        "street": "555 Sushi Street",
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94106",
        "phone": "+1555100300",
    },
    {
        "id": 4,
        "name": "Taco Town",
        "street": "888 Taco Court",
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94108",
        "phone": "+1555100400",
    },
    {
        "id": 5,
        "name": "Asian Express",
        "street": "999 Thai Avenue",
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94109",
        "phone": "+1555100500",
    },
]

# =============================================================================
# DEFAULT FOOD ITEMS
# =============================================================================

DEFAULT_FOODS = [
    # Burgers
    {"id": 1, "name": "Classic Cheeseburger", "description": "Juicy beef patty with melted cheddar, lettuce, tomato, and our secret sauce", "category": "burgers", "price": 12.99, "available": True},
    {"id": 2, "name": "Double Bacon Burger", "description": "Two beef patties with crispy bacon, cheese, pickles, and BBQ sauce", "category": "burgers", "price": 16.99, "available": True},
    {"id": 3, "name": "Veggie Burger", "description": "Plant-based patty with avocado, sprouts, and herb mayo", "category": "burgers", "price": 13.99, "available": True},
    {"id": 4, "name": "Spicy Jalapeño Burger", "description": "Beef patty with pepper jack cheese, jalapeños, and chipotle aioli", "category": "burgers", "price": 14.99, "available": True},
    
    # Pizza
    {"id": 5, "name": "Margherita Pizza", "description": "Fresh mozzarella, tomato sauce, and basil on thin crust", "category": "pizza", "price": 18.99, "available": True},
    {"id": 6, "name": "Pepperoni Supreme", "description": "Loaded with pepperoni, mozzarella, and our signature tomato sauce", "category": "pizza", "price": 21.99, "available": True},
    {"id": 7, "name": "BBQ Chicken Pizza", "description": "Grilled chicken, red onions, cilantro with tangy BBQ sauce", "category": "pizza", "price": 23.99, "available": True},
    {"id": 8, "name": "Four Cheese Pizza", "description": "Mozzarella, parmesan, gorgonzola, and ricotta blend", "category": "pizza", "price": 22.99, "available": True},
    
    # Sushi
    {"id": 9, "name": "California Roll (8pc)", "description": "Crab, avocado, and cucumber with sesame seeds", "category": "sushi", "price": 12.99, "available": True},
    {"id": 10, "name": "Salmon Nigiri (4pc)", "description": "Fresh Atlantic salmon over pressed sushi rice", "category": "sushi", "price": 14.99, "available": True},
    {"id": 11, "name": "Dragon Roll (8pc)", "description": "Eel, cucumber topped with avocado and unagi sauce", "category": "sushi", "price": 18.99, "available": True},
    {"id": 12, "name": "Sashimi Platter", "description": "Chef's selection of 12 pieces of premium fresh fish", "category": "sushi", "price": 32.99, "available": True},
    
    # Tacos
    {"id": 13, "name": "Street Tacos (3pc)", "description": "Authentic corn tortillas with carne asada, onions, and cilantro", "category": "tacos", "price": 11.99, "available": True},
    {"id": 14, "name": "Fish Tacos (3pc)", "description": "Crispy battered fish with cabbage slaw and lime crema", "category": "tacos", "price": 13.99, "available": True},
    {"id": 15, "name": "Carnitas Tacos (3pc)", "description": "Slow-cooked pork with salsa verde and pickled onions", "category": "tacos", "price": 12.99, "available": True},
    
    # Asian
    {"id": 16, "name": "Pad Thai", "description": "Rice noodles with shrimp, tofu, peanuts, and tamarind sauce", "category": "asian", "price": 15.99, "available": True},
    {"id": 17, "name": "Kung Pao Chicken", "description": "Wok-fired chicken with peanuts, vegetables, and spicy sauce", "category": "asian", "price": 14.99, "available": True},
    {"id": 18, "name": "Beef Teriyaki Bowl", "description": "Grilled beef with teriyaki glaze over steamed rice and vegetables", "category": "asian", "price": 16.99, "available": True},
    
    # Desserts
    {"id": 19, "name": "Chocolate Lava Cake", "description": "Warm chocolate cake with molten center and vanilla ice cream", "category": "desserts", "price": 8.99, "available": True},
    {"id": 20, "name": "New York Cheesecake", "description": "Creamy cheesecake with graham cracker crust and berry compote", "category": "desserts", "price": 7.99, "available": True},
    {"id": 21, "name": "Churros (6pc)", "description": "Crispy cinnamon sugar churros with chocolate dipping sauce", "category": "desserts", "price": 6.99, "available": True},
    
    # Drinks
    {"id": 22, "name": "Fresh Lemonade", "description": "House-made lemonade with fresh mint", "category": "drinks", "price": 4.99, "available": True},
    {"id": 23, "name": "Mango Smoothie", "description": "Blended mango with yogurt and honey", "category": "drinks", "price": 6.99, "available": True},
    {"id": 24, "name": "Iced Coffee", "description": "Cold brew coffee with your choice of milk", "category": "drinks", "price": 4.49, "available": True},
    {"id": 25, "name": "Bubble Tea", "description": "Taiwanese milk tea with tapioca pearls", "category": "drinks", "price": 5.99, "available": True},
]

# =============================================================================
# DEFAULT ORDERS
# =============================================================================

DEFAULT_ORDERS = [
    {
        "id": 1,
        "customer_id": 7,  # John Customer
        "status": "delivered",
        "subtotal": 28.98,
        "delivery_fee": 3.99,
        "total": 32.97,
        "created_at": datetime.now() - timedelta(days=2, hours=5),
    },
    {
        "id": 2,
        "customer_id": 8,  # Jane Smith
        "status": "in_transit",
        "subtotal": 37.97,
        "delivery_fee": 4.99,
        "total": 42.96,
        "created_at": datetime.now() - timedelta(hours=2),
    },
    {
        "id": 3,
        "customer_id": 9,  # Bob Wilson
        "status": "picked_up",
        "subtotal": 51.98,
        "delivery_fee": 5.99,
        "total": 57.97,
        "created_at": datetime.now() - timedelta(hours=1),
    },
    {
        "id": 4,
        "customer_id": 7,  # John Customer
        "status": "confirmed",
        "subtotal": 18.98,
        "delivery_fee": 3.99,
        "total": 22.97,
        "created_at": datetime.now() - timedelta(minutes=30),
    },
    {
        "id": 5,
        "customer_id": 8,  # Jane Smith
        "status": "pending",
        "subtotal": 25.98,
        "delivery_fee": 4.49,
        "total": 30.47,
        "created_at": datetime.now() - timedelta(minutes=10),
    },
]

# =============================================================================
# DEFAULT ORDER ITEMS
# =============================================================================

DEFAULT_ORDER_ITEMS = [
    # Order 1 items
    {"id": 1, "order_id": 1, "food_id": 13, "name": "Street Tacos (3pc)", "quantity": 2, "price_at_order": 11.99},
    {"id": 2, "order_id": 1, "food_id": 21, "name": "Churros (6pc)", "quantity": 1, "price_at_order": 6.99},
    
    # Order 2 items
    {"id": 3, "order_id": 2, "food_id": 1, "name": "Classic Cheeseburger", "quantity": 2, "price_at_order": 12.99},
    {"id": 4, "order_id": 2, "food_id": 22, "name": "Fresh Lemonade", "quantity": 2, "price_at_order": 4.99},
    
    # Order 3 items
    {"id": 5, "order_id": 3, "food_id": 12, "name": "Sashimi Platter", "quantity": 1, "price_at_order": 32.99},
    {"id": 6, "order_id": 3, "food_id": 11, "name": "Dragon Roll (8pc)", "quantity": 1, "price_at_order": 18.99},
    
    # Order 4 items
    {"id": 7, "order_id": 4, "food_id": 5, "name": "Margherita Pizza", "quantity": 1, "price_at_order": 18.99},
    
    # Order 5 items
    {"id": 8, "order_id": 5, "food_id": 16, "name": "Pad Thai", "quantity": 1, "price_at_order": 15.99},
    {"id": 9, "order_id": 5, "food_id": 25, "name": "Bubble Tea", "quantity": 2, "price_at_order": 5.99},
]

# =============================================================================
# DEFAULT ADDRESSES
# =============================================================================

DEFAULT_ADDRESSES = [
    {"id": 1, "order_id": 1, "street": "888 Taco Court", "city": "San Francisco", "state": "CA", "zip_code": "94108", "notes": "Pickup address"},
    {"id": 2, "order_id": 1, "street": "456 Customer Blvd", "city": "San Francisco", "state": "CA", "zip_code": "94103", "notes": "Ring doorbell"},
    
    {"id": 3, "order_id": 2, "street": "123 Restaurant Ave", "city": "San Francisco", "state": "CA", "zip_code": "94102", "notes": "Pickup address"},
    {"id": 4, "order_id": 2, "street": "456 Customer Blvd", "city": "San Francisco", "state": "CA", "zip_code": "94103", "notes": "Leave at door"},
    
    {"id": 5, "order_id": 3, "street": "555 Sushi Street", "city": "San Francisco", "state": "CA", "zip_code": "94106", "notes": "Pickup address"},
    {"id": 6, "order_id": 3, "street": "777 Office Park", "city": "San Francisco", "state": "CA", "zip_code": "94107", "notes": "Call on arrival"},
    
    {"id": 7, "order_id": 4, "street": "789 Pizza Lane", "city": "San Francisco", "state": "CA", "zip_code": "94104", "notes": "Pickup address"},
    {"id": 8, "order_id": 4, "street": "321 Home Street", "city": "San Francisco", "state": "CA", "zip_code": "94105", "notes": "Apt 5B"},
    
    {"id": 9, "order_id": 5, "street": "999 Thai Avenue", "city": "San Francisco", "state": "CA", "zip_code": "94109", "notes": "Pickup address"},
    {"id": 10, "order_id": 5, "street": "111 Apartment Complex", "city": "San Francisco", "state": "CA", "zip_code": "94110", "notes": "Unit 12"},
]

# =============================================================================
# DEFAULT PAYMENTS
# =============================================================================

DEFAULT_PAYMENTS = [
    {"id": 1, "order_id": 1, "amount": 32.97, "method": "debit_card", "status": "success", "paid_at": datetime.now() - timedelta(days=2, hours=5)},
    {"id": 2, "order_id": 2, "amount": 42.96, "method": "debit_card", "status": "success", "paid_at": datetime.now() - timedelta(hours=2)},
    {"id": 3, "order_id": 3, "amount": 57.97, "method": "debit_card", "status": "success", "paid_at": datetime.now() - timedelta(hours=1)},
    {"id": 4, "order_id": 4, "amount": 22.97, "method": "debit_card", "status": "pending", "paid_at": None},
    {"id": 5, "order_id": 5, "amount": 30.47, "method": "debit_card", "status": "pending", "paid_at": None},
]

# =============================================================================
# DEFAULT DELIVERIES
# =============================================================================

DEFAULT_DELIVERIES = [
    {
        "id": 1,
        "order_id": 1,
        "driver_id": 1,  # Mike Driver
        "restaurant_id": 4,  # Taco Town
        "assigned_by": 3,  # Sarah Manager
        "status": "delivered",
        "assigned_at": datetime.now() - timedelta(days=2, hours=5),
        "delivered_at": datetime.now() - timedelta(days=2, hours=4, minutes=30),
    },
    {
        "id": 2,
        "order_id": 2,
        "driver_id": 1,  # Mike Driver
        "restaurant_id": 1,  # Burger Palace
        "assigned_by": 3,  # Sarah Manager
        "status": "in_transit",
        "assigned_at": datetime.now() - timedelta(hours=2),
        "delivered_at": None,
    },
    {
        "id": 3,
        "order_id": 3,
        "driver_id": 2,  # Tom Rider
        "restaurant_id": 3,  # Sushi Sensation
        "assigned_by": 3,  # Sarah Manager
        "status": "picked_up",
        "assigned_at": datetime.now() - timedelta(hours=1),
        "delivered_at": None,
    },
]

# =============================================================================
# DEFAULT ORDER STATUS HISTORY
# =============================================================================

DEFAULT_ORDER_STATUS_HISTORY = [
    # Order 1 history (delivered)
    {"id": 1, "order_id": 1, "status": "pending", "changed_at": datetime.now() - timedelta(days=2, hours=5)},
    {"id": 2, "order_id": 1, "status": "confirmed", "changed_at": datetime.now() - timedelta(days=2, hours=4, minutes=55)},
    {"id": 3, "order_id": 1, "status": "assigned", "changed_at": datetime.now() - timedelta(days=2, hours=4, minutes=50)},
    {"id": 4, "order_id": 1, "status": "picked_up", "changed_at": datetime.now() - timedelta(days=2, hours=4, minutes=40)},
    {"id": 5, "order_id": 1, "status": "in_transit", "changed_at": datetime.now() - timedelta(days=2, hours=4, minutes=35)},
    {"id": 6, "order_id": 1, "status": "delivered", "changed_at": datetime.now() - timedelta(days=2, hours=4, minutes=30)},
    
    # Order 2 history (in_transit)
    {"id": 7, "order_id": 2, "status": "pending", "changed_at": datetime.now() - timedelta(hours=2)},
    {"id": 8, "order_id": 2, "status": "confirmed", "changed_at": datetime.now() - timedelta(hours=1, minutes=55)},
    {"id": 9, "order_id": 2, "status": "assigned", "changed_at": datetime.now() - timedelta(hours=1, minutes=50)},
    {"id": 10, "order_id": 2, "status": "picked_up", "changed_at": datetime.now() - timedelta(hours=1, minutes=30)},
    {"id": 11, "order_id": 2, "status": "in_transit", "changed_at": datetime.now() - timedelta(hours=1, minutes=20)},
    
    # Order 3 history (picked_up)
    {"id": 12, "order_id": 3, "status": "pending", "changed_at": datetime.now() - timedelta(hours=1)},
    {"id": 13, "order_id": 3, "status": "confirmed", "changed_at": datetime.now() - timedelta(minutes=55)},
    {"id": 14, "order_id": 3, "status": "assigned", "changed_at": datetime.now() - timedelta(minutes=50)},
    {"id": 15, "order_id": 3, "status": "picked_up", "changed_at": datetime.now() - timedelta(minutes=30)},
    
    # Order 4 history (confirmed)
    {"id": 16, "order_id": 4, "status": "pending", "changed_at": datetime.now() - timedelta(minutes=30)},
    {"id": 17, "order_id": 4, "status": "confirmed", "changed_at": datetime.now() - timedelta(minutes=25)},
    
    # Order 5 history (pending)
    {"id": 18, "order_id": 5, "status": "pending", "changed_at": datetime.now() - timedelta(minutes=10)},
]

# =============================================================================
# HELPER FUNCTION TO GET ALL SEED DATA
# =============================================================================

def get_all_seed_data():
    """Returns a dictionary containing all seed data"""
    return {
        "roles": DEFAULT_ROLES,
        "permissions": DEFAULT_PERMISSIONS,
        "role_permissions": DEFAULT_ROLE_PERMISSIONS,
        "users": DEFAULT_USERS,
        "drivers": DEFAULT_DRIVERS,
        "restaurants": DEFAULT_RESTAURANTS,
        "foods": DEFAULT_FOODS,
        "orders": DEFAULT_ORDERS,
        "order_items": DEFAULT_ORDER_ITEMS,
        "addresses": DEFAULT_ADDRESSES,
        "payments": DEFAULT_PAYMENTS,
        "deliveries": DEFAULT_DELIVERIES,
        "order_status_history": DEFAULT_ORDER_STATUS_HISTORY,
    }