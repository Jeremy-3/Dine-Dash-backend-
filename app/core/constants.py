from datetime import datetime, timedelta
import bcrypt
from app.core.config import settings

# =============================================================================
# ROLES & PERMISSIONS
# =============================================================================

ROLE_SUPERADMIN_ID = 1
ROLE_ADMIN_ID      = 2
ROLE_MANAGER_ID    = 3
ROLE_DRIVER_ID     = 4
ROLE_CUSTOMER_ID   = 5

DEFAULT_ROLES = [
    {"id": ROLE_SUPERADMIN_ID, "name": "superadmin"},
    {"id": ROLE_ADMIN_ID,      "name": "admin"},
    {"id": ROLE_MANAGER_ID,    "name": "manager"},
    {"id": ROLE_DRIVER_ID,     "name": "driver"},
    {"id": ROLE_CUSTOMER_ID,   "name": "customer"},
]

DEFAULT_PERMISSIONS = [
    # Users
    {"id": 1,  "name": "users.view_all",         "description": "View all users",                  "category": "users"},
    {"id": 2,  "name": "users.create",            "description": "Create new users",                "category": "users"},
    {"id": 3,  "name": "users.edit",              "description": "Edit user details",               "category": "users"},
    {"id": 4,  "name": "users.delete",            "description": "Delete users",                    "category": "users"},
    {"id": 5,  "name": "users.view_own",          "description": "View own profile",                "category": "users"},
    {"id": 6,  "name": "users.edit_own",          "description": "Edit own profile",                "category": "users"},
    # Roles
    {"id": 7,  "name": "roles.view",              "description": "View roles",                      "category": "roles"},
    {"id": 8,  "name": "roles.create",            "description": "Create roles",                    "category": "roles"},
    {"id": 9,  "name": "roles.edit",              "description": "Edit roles",                      "category": "roles"},
    {"id": 10, "name": "roles.delete",            "description": "Delete roles",                    "category": "roles"},
    {"id": 11, "name": "permissions.manage",      "description": "Manage permissions",              "category": "roles"},
    # Foods
    {"id": 12, "name": "foods.view",              "description": "View food menu",                  "category": "foods"},
    {"id": 13, "name": "foods.create",            "description": "Add new food items",              "category": "foods"},
    {"id": 14, "name": "foods.edit",              "description": "Edit food items",                 "category": "foods"},
    {"id": 15, "name": "foods.delete",            "description": "Delete food items",               "category": "foods"},
    {"id": 16, "name": "foods.toggle_availability","description": "Toggle food availability",       "category": "foods"},
    {"id": 17, "name": "foods.manage_categories", "description": "Manage food categories",          "category": "foods"},
    # Orders
    {"id": 18, "name": "orders.view_all",         "description": "View all orders",                 "category": "orders"},
    {"id": 19, "name": "orders.view_own",         "description": "View own orders",                 "category": "orders"},
    {"id": 20, "name": "orders.create",           "description": "Create new orders",               "category": "orders"},
    {"id": 21, "name": "orders.edit",             "description": "Edit order details",              "category": "orders"},
    {"id": 22, "name": "orders.cancel",           "description": "Cancel orders",                   "category": "orders"},
    {"id": 23, "name": "orders.confirm",          "description": "Confirm pending orders",          "category": "orders"},
    {"id": 24, "name": "orders.update_status",    "description": "Update order status",             "category": "orders"},
    {"id": 25, "name": "orders.view_history",     "description": "View order history",              "category": "orders"},
    # Drivers
    {"id": 26, "name": "drivers.view_all",        "description": "View all drivers",                "category": "drivers"},
    {"id": 27, "name": "drivers.create",          "description": "Create driver accounts",          "category": "drivers"},
    {"id": 28, "name": "drivers.edit",            "description": "Edit driver details",             "category": "drivers"},
    {"id": 29, "name": "drivers.delete",          "description": "Delete drivers",                  "category": "drivers"},
    {"id": 30, "name": "drivers.update_status",   "description": "Update any driver status",        "category": "drivers"},
    {"id": 31, "name": "drivers.update_own_status","description": "Update own driver status",       "category": "drivers"},
    {"id": 32, "name": "drivers.view_performance","description": "View driver performance metrics", "category": "drivers"},
    # Deliveries
    {"id": 33, "name": "deliveries.view_all",     "description": "View all deliveries",             "category": "deliveries"},
    {"id": 34, "name": "deliveries.view_own",     "description": "View own deliveries",             "category": "deliveries"},
    {"id": 35, "name": "deliveries.assign",       "description": "Assign deliveries to drivers",    "category": "deliveries"},
    {"id": 36, "name": "deliveries.reassign",     "description": "Reassign deliveries",             "category": "deliveries"},
    {"id": 37, "name": "deliveries.update_status","description": "Update delivery status",          "category": "deliveries"},
    # Restaurants
    {"id": 38, "name": "restaurants.view",        "description": "View restaurants",                "category": "restaurants"},
    {"id": 39, "name": "restaurants.create",      "description": "Add new restaurants",             "category": "restaurants"},
    {"id": 40, "name": "restaurants.edit",        "description": "Edit restaurant details",         "category": "restaurants"},
    {"id": 41, "name": "restaurants.delete",      "description": "Delete restaurants",              "category": "restaurants"},
    # Payments
    {"id": 42, "name": "payments.view_all",       "description": "View all payments",               "category": "payments"},
    {"id": 43, "name": "payments.view_own",       "description": "View own payments",               "category": "payments"},
    {"id": 44, "name": "payments.process",        "description": "Process payments",                "category": "payments"},
    {"id": 45, "name": "payments.refund",         "description": "Process refunds",                 "category": "payments"},
    {"id": 46, "name": "payments.view_details",   "description": "View payment details",            "category": "payments"},
    # Offers & Combos
    {"id": 47, "name": "offers.view",             "description": "View daily offers",               "category": "offers"},
    {"id": 48, "name": "offers.create",           "description": "Create daily offers",             "category": "offers"},
    {"id": 49, "name": "offers.edit",             "description": "Edit daily offers",               "category": "offers"},
    {"id": 50, "name": "offers.delete",           "description": "Delete daily offers",             "category": "offers"},
    {"id": 51, "name": "offers.toggle_active",    "description": "Activate/deactivate offers",      "category": "offers"},
    {"id": 52, "name": "combos.view",             "description": "View combo deals",                "category": "combos"},
    {"id": 53, "name": "combos.create",           "description": "Create combo deals",              "category": "combos"},
    {"id": 54, "name": "combos.edit",             "description": "Edit combo deals",                "category": "combos"},
    {"id": 55, "name": "combos.delete",           "description": "Delete combo deals",              "category": "combos"},
    # Analytics
    {"id": 56, "name": "analytics.view",          "description": "View analytics dashboard",        "category": "analytics"},
    {"id": 57, "name": "analytics.export",        "description": "Export analytics data",           "category": "analytics"},
    {"id": 58, "name": "reports.sales",           "description": "View sales reports",              "category": "analytics"},
    {"id": 59, "name": "reports.orders",          "description": "View order reports",              "category": "analytics"},
    {"id": 60, "name": "reports.drivers",         "description": "View driver reports",             "category": "analytics"},
    {"id": 61, "name": "reports.customers",       "description": "View customer reports",           "category": "analytics"},
    # Dashboard
    {"id": 62, "name": "dashboard.admin",         "description": "Access admin dashboard",          "category": "dashboard"},
    {"id": 63, "name": "dashboard.manager",       "description": "Access manager dashboard",        "category": "dashboard"},
    {"id": 64, "name": "dashboard.driver",        "description": "Access driver dashboard",         "category": "dashboard"},
    {"id": 65, "name": "dashboard.customer",      "description": "Access customer dashboard",       "category": "dashboard"},
    # Addresses
    {"id": 66, "name": "addresses.view_own",      "description": "View own addresses",              "category": "addresses"},
    {"id": 67, "name": "addresses.create",        "description": "Create addresses",                "category": "addresses"},
    {"id": 68, "name": "addresses.edit_own",      "description": "Edit own addresses",              "category": "addresses"},
    {"id": 69, "name": "addresses.delete_own",    "description": "Delete own addresses",            "category": "addresses"},
]

DEFAULT_ROLE_PERMISSIONS = {
    ROLE_SUPERADMIN_ID: [p["id"] for p in DEFAULT_PERMISSIONS],

    ROLE_ADMIN_ID: [
        1, 2, 3, 4, 5, 6,           # users
        12, 13, 14, 15, 16, 17,     # foods
        18, 20, 21, 22, 23, 24, 25, # orders
        26, 27, 28, 29, 30, 32,     # drivers
        33, 35, 36, 37,             # deliveries
        38, 39, 40, 41,             # restaurants
        42, 44, 45, 46,             # payments
        47, 48, 49, 50, 51,         # offers
        52, 53, 54, 55,             # combos
        56, 57, 58, 59, 60, 61,     # analytics
        62,                         # dashboard
        7,8,9,10,11,                # roles and permissions
    ],

    ROLE_MANAGER_ID: [
        1, 5, 6,                    # users (view only)
        12, 13, 14, 15, 16, 17,     # foods
        18, 20, 21, 22, 23, 24, 25, # orders
        26, 30, 32,                 # drivers
        33, 35, 36, 37,             # deliveries
        38, 40,                     # restaurants
        42, 46,                     # payments
        47, 48, 49, 50, 51,         # offers
        52, 53, 54, 55,             # combos
        56, 58, 59, 60,             # analytics
        63,                         # dashboard
    ],

    ROLE_DRIVER_ID: [
        5, 6,                       # own profile
        12,                         # view foods
        19, 25,                     # own orders
        31,                         # own driver status
        34, 37,                     # own deliveries
        43,                         # own payments
        47, 52,                     # view offers/combos
        64,                         # dashboard
    ],

    ROLE_CUSTOMER_ID: [
        5, 6,                       # own profile
        12,                         # view foods
        19, 20, 22, 25,             # own orders
        43, 44, 46,                 # payments (44=process needed for order creation)
        47, 52,                     # view offers/combos
        66, 67, 68, 69,             # addresses
        65,                         # dashboard
    ],
}

# =============================================================================
# USERS
# =============================================================================

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

DEFAULT_USERS = [
    {
        "id": 1,
        "name": settings.SUPERADMIN_NAME,
        "email": settings.SUPERADMIN_EMAIL,
        "phone": settings.SUPERADMIN_PHONE,
        "password_hash": hash_password(settings.SUPERADMIN_PASSWORD),
        "role_id": ROLE_SUPERADMIN_ID,
        "is_active": True,
    },
    {
        "id": 2,
        "name": "Admin User",
        "email": "admin@demo.com",
        "phone": "+254700100001",
        "password_hash": hash_password("demo123"),
        "role_id": ROLE_ADMIN_ID,
        "is_active": True,
    },
    {
        "id": 3,
        "name": "Sarah Manager",
        "email": "manager@demo.com",
        "phone": "+254700100002",
        "password_hash": hash_password("demo123"),
        "role_id": ROLE_MANAGER_ID,
        "is_active": True,
    },
    # ── Drivers ───────────────────────────────────────────────────────────────
    {
        "id": 4,
        "name": "Mike Kamau",
        "email": "driver@demo.com",
        "phone": "+254712345001",
        "password_hash": hash_password("demo123"),
        "role_id": ROLE_DRIVER_ID,
        "is_active": True,
    },
    {
        "id": 5,
        "name": "Tom Otieno",
        "email": "driver2@demo.com",
        "phone": "+254722345002",
        "password_hash": hash_password("demo123"),
        "role_id": ROLE_DRIVER_ID,
        "is_active": True,
    },
    {
        "id": 6,
        "name": "Lisa Wanjiru",
        "email": "driver3@demo.com",
        "phone": "+254733345003",
        "password_hash": hash_password("demo123"),
        "role_id": ROLE_DRIVER_ID,
        "is_active": True,
    },
    # ── Customers ─────────────────────────────────────────────────────────────
    {
        "id": 7,
        "name": "John Kariuki",
        "email": "customer@demo.com",
        "phone": "+254711000001",
        "password_hash": hash_password("demo123"),
        "role_id": ROLE_CUSTOMER_ID,
        "is_active": True,
    },
    {
        "id": 8,
        "name": "Jane Muthoni",
        "email": "customer2@demo.com",
        "phone": "+254722000002",
        "password_hash": hash_password("demo123"),
        "role_id": ROLE_CUSTOMER_ID,
        "is_active": True,
    },
    {
        "id": 9,
        "name": "Bob Odhiambo",
        "email": "customer3@demo.com",
        "phone": "+254733000003",
        "password_hash": hash_password("demo123"),
        "role_id": ROLE_CUSTOMER_ID,
        "is_active": True,
    },
]

# =============================================================================
# DRIVERS
# =============================================================================

DEFAULT_DRIVERS = [
    {"id": 1, "user_id": 4, "status": "available", "created_at": datetime.now() - timedelta(days=100)},
    {"id": 2, "user_id": 5, "status": "available", "created_at": datetime.now() - timedelta(days=95)},
    {"id": 3, "user_id": 6, "status": "available", "created_at": datetime.now() - timedelta(days=90)},
]

# =============================================================================
# RESTAURANTS — Nairobi locations
# =============================================================================

DEFAULT_RESTAURANTS = [
    {"id": 1, "name": "Burger Palace",     "street": "Kimathi Street",      "city": "Nairobi", "state": "Nairobi County", "zip_code": "00100", "phone": "+254720100001"},
    {"id": 2, "name": "Pizza Paradise",    "street": "Kenyatta Avenue",     "city": "Nairobi", "state": "Nairobi County", "zip_code": "00100", "phone": "+254720100002"},
    {"id": 3, "name": "Sushi Sensation",   "street": "Westlands Road",      "city": "Nairobi", "state": "Nairobi County", "zip_code": "00800", "phone": "+254720100003"},
    {"id": 4, "name": "Taco Town",         "street": "Ngong Road",          "city": "Nairobi", "state": "Nairobi County", "zip_code": "00200", "phone": "+254720100004"},
    {"id": 5, "name": "Asian Express",     "street": "Moi Avenue",          "city": "Nairobi", "state": "Nairobi County", "zip_code": "00100", "phone": "+254720100005"},
]

# =============================================================================
# FOODS — matches your backend seed exactly (IDs matter for combos)
# =============================================================================

DEFAULT_FOODS = [
    # Burgers
    {"id": 1,  "name": "Classic Cheeseburger",      "description": "Juicy beef patty with melted cheddar, lettuce, tomato, and our secret sauce",      "category": "burgers",  "price": 12.99, "available": True},
    {"id": 2,  "name": "Double Bacon Burger",        "description": "Two beef patties with crispy bacon, cheese, pickles, and BBQ sauce",               "category": "burgers",  "price": 16.99, "available": True},
    {"id": 3,  "name": "Veggie Burger",              "description": "Plant-based patty with avocado, sprouts, and herb mayo",                           "category": "burgers",  "price": 13.99, "available": True},
    {"id": 4,  "name": "Spicy Jalapeño Burger",      "description": "Beef patty with pepper jack cheese, jalapeños, and chipotle aioli",                "category": "burgers",  "price": 14.99, "available": True},
    # Pizza
    {"id": 5,  "name": "Margherita Pizza",           "description": "Fresh mozzarella, tomato sauce, and basil on thin crust",                          "category": "pizza",    "price": 18.99, "available": True},
    {"id": 6,  "name": "Pepperoni Supreme",          "description": "Loaded with pepperoni, mozzarella, and our signature tomato sauce",                "category": "pizza",    "price": 21.99, "available": True},
    {"id": 7,  "name": "BBQ Chicken Pizza",          "description": "Grilled chicken, red onions, cilantro with tangy BBQ sauce",                       "category": "pizza",    "price": 23.99, "available": True},
    {"id": 8,  "name": "Four Cheese Pizza",          "description": "Mozzarella, parmesan, gorgonzola, and ricotta blend",                              "category": "pizza",    "price": 22.99, "available": True},
    # Sushi
    {"id": 9,  "name": "California Roll (8pc)",      "description": "Crab, avocado, and cucumber with sesame seeds",                                    "category": "sushi",    "price": 12.99, "available": True},
    {"id": 10, "name": "Salmon Nigiri (4pc)",         "description": "Fresh Atlantic salmon over pressed sushi rice",                                    "category": "sushi",    "price": 14.99, "available": True},
    {"id": 11, "name": "Dragon Roll (8pc)",           "description": "Eel, cucumber topped with avocado and unagi sauce",                               "category": "sushi",    "price": 18.99, "available": True},
    {"id": 12, "name": "Sashimi Platter",             "description": "Chef's selection of 12 pieces of premium fresh fish",                             "category": "sushi",    "price": 32.99, "available": True},
    # Tacos
    {"id": 13, "name": "Street Tacos (3pc)",          "description": "Authentic corn tortillas with carne asada, onions, and cilantro",                 "category": "tacos",    "price": 11.99, "available": True},
    {"id": 14, "name": "Fish Tacos (3pc)",             "description": "Crispy battered fish with cabbage slaw and lime crema",                          "category": "tacos",    "price": 13.99, "available": True},
    {"id": 15, "name": "Carnitas Tacos (3pc)",         "description": "Slow-cooked pork with salsa verde and pickled onions",                           "category": "tacos",    "price": 12.99, "available": True},
    # Asian
    {"id": 16, "name": "Pad Thai",                    "description": "Rice noodles with shrimp, tofu, peanuts, and tamarind sauce",                     "category": "asian",    "price": 15.99, "available": True},
    {"id": 17, "name": "Kung Pao Chicken",            "description": "Wok-fired chicken with peanuts, vegetables, and spicy sauce",                     "category": "asian",    "price": 14.99, "available": True},
    {"id": 18, "name": "Beef Teriyaki Bowl",          "description": "Grilled beef with teriyaki glaze over steamed rice and vegetables",               "category": "asian",    "price": 16.99, "available": True},
    # Desserts
    {"id": 19, "name": "Chocolate Lava Cake",         "description": "Warm chocolate cake with molten center and vanilla ice cream",                    "category": "desserts", "price": 8.99,  "available": True},
    {"id": 20, "name": "New York Cheesecake",          "description": "Creamy cheesecake with graham cracker crust and berry compote",                  "category": "desserts", "price": 7.99,  "available": True},
    {"id": 21, "name": "Churros (6pc)",                "description": "Crispy cinnamon sugar churros with chocolate dipping sauce",                     "category": "desserts", "price": 6.99,  "available": True},
    # Drinks
    {"id": 22, "name": "Fresh Lemonade",              "description": "House-made lemonade with fresh mint",                                             "category": "drinks",   "price": 4.99,  "available": True},
    {"id": 23, "name": "Mango Smoothie",              "description": "Blended mango with yogurt and honey",                                             "category": "drinks",   "price": 6.99,  "available": True},
    {"id": 24, "name": "Iced Coffee",                 "description": "Cold brew coffee with your choice of milk",                                        "category": "drinks",   "price": 4.49,  "available": True},
    {"id": 25, "name": "Bubble Tea",                  "description": "Taiwanese milk tea with tapioca pearls",                                          "category": "drinks",   "price": 5.99,  "available": True},
]

# =============================================================================
# COMBOS — matches the 8 combos you created via admin UI
# Note: food IDs reference DEFAULT_FOODS above
# =============================================================================

DEFAULT_COMBOS = [
    {
        "id": 1, "name": "Burger Feast",
        "description": "Classic Cheeseburger + Fries + Drink",
        "combo_price": 15.99, "is_available": True,
        "items": [{"food_id": 1, "quantity": 1}],
    },
    {
        "id": 2, "name": "Pizza Party Pack",
        "description": "Any large pizza + Garlic bread + 2 drinks",
        "combo_price": 27.99, "is_available": True,
        "items": [{"food_id": 6, "quantity": 1}],
    },
    {
        "id": 3, "name": "Sushi Date Night",
        "description": "Dragon Roll + California Roll + Miso soup for 2",
        "combo_price": 29.99, "is_available": True,
        "items": [{"food_id": 11, "quantity": 1}, {"food_id": 9, "quantity": 1}],
    },
    {
        "id": 4, "name": "Taco Fiesta",
        "description": "Any 2 taco orders + Churros + 2 drinks",
        "combo_price": 28.99, "is_available": True,
        "items": [{"food_id": 13, "quantity": 1}, {"food_id": 15, "quantity": 1}, {"food_id": 21, "quantity": 1}],
    },
    {
        "id": 5, "name": "Asian Express",
        "description": "Pad Thai + Spring Rolls + Bubble Tea",
        "combo_price": 21.99, "is_available": True,
        "items": [{"food_id": 16, "quantity": 1}, {"food_id": 25, "quantity": 1}],
    },
    {
        "id": 6, "name": "Family Meal Deal",
        "description": "2 Pizzas + 4 Drinks + Chocolate Lava Cake",
        "combo_price": 49.99, "is_available": True,
        "items": [{"food_id": 6, "quantity": 1}, {"food_id": 7, "quantity": 1}, {"food_id": 19, "quantity": 1}],
    },
    {
        "id": 7, "name": "Healthy Lunch",
        "description": "Veggie Burger + Fresh Lemonade + Fruit Salad",
        "combo_price": 17.99, "is_available": True,
        "items": [{"food_id": 3, "quantity": 1}, {"food_id": 22, "quantity": 1}],
    },
    {
        "id": 8, "name": "Sweet Tooth Bundle",
        "description": "Chocolate Lava Cake + Churros + Mango Smoothie",
        "combo_price": 16.99, "is_available": True,
        "items": [{"food_id": 19, "quantity": 1}, {"food_id": 21, "quantity": 1}, {"food_id": 23, "quantity": 1}],
    },
]

# =============================================================================
# ORDERS — updated with Nairobi addresses + driver/restaurant FKs
# =============================================================================

DEFAULT_ORDERS = [
    {
        "id": 1, "customer_id": 7, "driver_id": 4, "restaurant_id": 4,
        "status": "delivered",
        "subtotal": 28.98, "delivery_fee": 3.99, "total": 32.97,
        "created_at": datetime.now() - timedelta(days=2, hours=5),
    },
    {
        "id": 2, "customer_id": 8, "driver_id": 4, "restaurant_id": 1,
        "status": "in_transit",
        "subtotal": 37.97, "delivery_fee": 4.99, "total": 42.96,
        "created_at": datetime.now() - timedelta(hours=2),
    },
    {
        "id": 3, "customer_id": 9, "driver_id": 5, "restaurant_id": 3,
        "status": "picked_up",
        "subtotal": 51.98, "delivery_fee": 5.99, "total": 57.97,
        "created_at": datetime.now() - timedelta(hours=1),
    },
    {
        "id": 4, "customer_id": 7, "driver_id": None, "restaurant_id": None,
        "status": "confirmed",
        "subtotal": 18.99, "delivery_fee": 3.99, "total": 22.98,
        "created_at": datetime.now() - timedelta(minutes=30),
    },
    {
        "id": 5, "customer_id": 8, "driver_id": None, "restaurant_id": None,
        "status": "pending",
        "subtotal": 25.98, "delivery_fee": 4.49, "total": 30.47,
        "created_at": datetime.now() - timedelta(minutes=10),
    },
]

DEFAULT_ORDER_ITEMS = [
    # Order 1
    {"id": 1, "order_id": 1, "food_id": 13, "name": "Street Tacos (3pc)",  "quantity": 2, "price_at_order": 11.99},
    {"id": 2, "order_id": 1, "food_id": 21, "name": "Churros (6pc)",       "quantity": 1, "price_at_order": 6.99},
    # Order 2
    {"id": 3, "order_id": 2, "food_id": 1,  "name": "Classic Cheeseburger","quantity": 2, "price_at_order": 12.99},
    {"id": 4, "order_id": 2, "food_id": 22, "name": "Fresh Lemonade",      "quantity": 2, "price_at_order": 4.99},
    # Order 3
    {"id": 5, "order_id": 3, "food_id": 12, "name": "Sashimi Platter",     "quantity": 1, "price_at_order": 32.99},
    {"id": 6, "order_id": 3, "food_id": 11, "name": "Dragon Roll (8pc)",   "quantity": 1, "price_at_order": 18.99},
    # Order 4
    {"id": 7, "order_id": 4, "food_id": 5,  "name": "Margherita Pizza",    "quantity": 1, "price_at_order": 18.99},
    # Order 5
    {"id": 8, "order_id": 5, "food_id": 16, "name": "Pad Thai",            "quantity": 1, "price_at_order": 15.99},
    {"id": 9, "order_id": 5, "food_id": 25, "name": "Bubble Tea",          "quantity": 2, "price_at_order": 5.99},
]

# =============================================================================
# ADDRESSES — Nairobi locations
# =============================================================================

DEFAULT_ADDRESSES = [
    {"id": 1,  "order_id": 1, "street": "Ngong Road",         "city": "Nairobi", "state": "Nairobi County", "zip_code": "00200", "notes": "Ring the gate"},
    {"id": 2,  "order_id": 2, "street": "Kileleshwa Estate",  "city": "Nairobi", "state": "Nairobi County", "zip_code": "00800", "notes": "Apt 4A, call on arrival"},
    {"id": 3,  "order_id": 3, "street": "Karen Hardy",        "city": "Nairobi", "state": "Nairobi County", "zip_code": "00502", "notes": "Leave with security"},
    {"id": 4,  "order_id": 4, "street": "Lavington Green",    "city": "Nairobi", "state": "Nairobi County", "zip_code": "00603", "notes": "House no. 12"},
    {"id": 5,  "order_id": 5, "street": "South B Estate",     "city": "Nairobi", "state": "Nairobi County", "zip_code": "00100", "notes": "Near the shops"},
]

# =============================================================================
# PAYMENTS
# =============================================================================

DEFAULT_PAYMENTS = [
    {"id": 1, "order_id": 1, "amount": 32.97, "method": "debit_card", "status": "success", "paid_at": datetime.now() - timedelta(days=2, hours=5)},
    {"id": 2, "order_id": 2, "amount": 42.96, "method": "debit_card", "status": "success", "paid_at": datetime.now() - timedelta(hours=2)},
    {"id": 3, "order_id": 3, "amount": 57.97, "method": "debit_card", "status": "success", "paid_at": datetime.now() - timedelta(hours=1)},
    {"id": 4, "order_id": 4, "amount": 22.98, "method": "debit_card", "status": "pending", "paid_at": None},
    {"id": 5, "order_id": 5, "amount": 30.47, "method": "debit_card", "status": "pending", "paid_at": None},
]

# =============================================================================
# DELIVERIES
# =============================================================================

DEFAULT_DELIVERIES = [
    {
        "id": 1, "order_id": 1, "driver_id": 1, "restaurant_id": 4, "assigned_by": 3,
        "status": "delivered",
        "assigned_at":  datetime.now() - timedelta(days=2, hours=5),
        "delivered_at": datetime.now() - timedelta(days=2, hours=4, minutes=30),
    },
    {
        "id": 2, "order_id": 2, "driver_id": 1, "restaurant_id": 1, "assigned_by": 3,
        "status": "in_transit",
        "assigned_at":  datetime.now() - timedelta(hours=2),
        "delivered_at": None,
    },
    {
        "id": 3, "order_id": 3, "driver_id": 2, "restaurant_id": 3, "assigned_by": 3,
        "status": "picked_up",
        "assigned_at":  datetime.now() - timedelta(hours=1),
        "delivered_at": None,
    },
]

# =============================================================================
# ORDER STATUS HISTORY
# =============================================================================

DEFAULT_ORDER_STATUS_HISTORY = [
    # Order 1 — delivered
    {"id": 1,  "order_id": 1, "status": "pending",     "changed_at": datetime.now() - timedelta(days=2, hours=5)},
    {"id": 2,  "order_id": 1, "status": "confirmed",   "changed_at": datetime.now() - timedelta(days=2, hours=4, minutes=55)},
    {"id": 3,  "order_id": 1, "status": "assigned",    "changed_at": datetime.now() - timedelta(days=2, hours=4, minutes=50)},
    {"id": 4,  "order_id": 1, "status": "picked_up",   "changed_at": datetime.now() - timedelta(days=2, hours=4, minutes=40)},
    {"id": 5,  "order_id": 1, "status": "in_transit",  "changed_at": datetime.now() - timedelta(days=2, hours=4, minutes=35)},
    {"id": 6,  "order_id": 1, "status": "delivered",   "changed_at": datetime.now() - timedelta(days=2, hours=4, minutes=30)},
    # Order 2 — in_transit
    {"id": 7,  "order_id": 2, "status": "pending",     "changed_at": datetime.now() - timedelta(hours=2)},
    {"id": 8,  "order_id": 2, "status": "confirmed",   "changed_at": datetime.now() - timedelta(hours=1, minutes=55)},
    {"id": 9,  "order_id": 2, "status": "assigned",    "changed_at": datetime.now() - timedelta(hours=1, minutes=50)},
    {"id": 10, "order_id": 2, "status": "picked_up",   "changed_at": datetime.now() - timedelta(hours=1, minutes=30)},
    {"id": 11, "order_id": 2, "status": "in_transit",  "changed_at": datetime.now() - timedelta(hours=1, minutes=20)},
    # Order 3 — picked_up
    {"id": 12, "order_id": 3, "status": "pending",     "changed_at": datetime.now() - timedelta(hours=1)},
    {"id": 13, "order_id": 3, "status": "confirmed",   "changed_at": datetime.now() - timedelta(minutes=55)},
    {"id": 14, "order_id": 3, "status": "assigned",    "changed_at": datetime.now() - timedelta(minutes=50)},
    {"id": 15, "order_id": 3, "status": "picked_up",   "changed_at": datetime.now() - timedelta(minutes=30)},
    # Order 4 — confirmed
    {"id": 16, "order_id": 4, "status": "pending",     "changed_at": datetime.now() - timedelta(minutes=30)},
    {"id": 17, "order_id": 4, "status": "confirmed",   "changed_at": datetime.now() - timedelta(minutes=25)},
    # Order 5 — pending
    {"id": 18, "order_id": 5, "status": "pending",     "changed_at": datetime.now() - timedelta(minutes=10)},
]

# =============================================================================
# HELPER
# =============================================================================

def get_all_seed_data():
    return {
        "roles":                DEFAULT_ROLES,
        "permissions":          DEFAULT_PERMISSIONS,
        "role_permissions":     DEFAULT_ROLE_PERMISSIONS,
        "users":                DEFAULT_USERS,
        "drivers":              DEFAULT_DRIVERS,
        "restaurants":          DEFAULT_RESTAURANTS,
        "foods":                DEFAULT_FOODS,
        "combos":               DEFAULT_COMBOS,
        "orders":               DEFAULT_ORDERS,
        "order_items":          DEFAULT_ORDER_ITEMS,
        "addresses":            DEFAULT_ADDRESSES,
        "payments":             DEFAULT_PAYMENTS,
        "deliveries":           DEFAULT_DELIVERIES,
        "order_status_history": DEFAULT_ORDER_STATUS_HISTORY,
    }