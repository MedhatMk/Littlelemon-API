import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')  # Replace 'your_database_name' with your database name or path

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Define the menu items as a list of dictionaries
menu_items = [

        {
            "id": 1,
            "title": "Mozzarella Sticks",
            "price": 7.99,
            "featured":False,
            "category_id": 1,
        },
        {"id": 2, "title": "Chicken Wings", "price": 9.99, "featured": True, "category_id": 1},
        {
            "id": 3,
            "title": "Spaghetti Bolognese",
            "price": 12.99,
            "featured":False,
            "category_id": 2,
        },
        {
            "id": 4,
            "title": "Margherita Pizza",
            "price": 10.99,
            "featured": True,
            "category_id": 2,
        },
        {
            "id": 5,
            "title": "Chocolate Cake",
            "price": 6.99,
            "featured":False,
            "category_id": 3,
        },
        {
            "id": 6,
            "title": "Vanilla Ice Cream",
            "price": 4.99,
            "featured": True,
            "category_id": 3,
        },
        {"id": 7, "title": "Soda", "price": 1.99, "featured":False, "category_id": 4},
        {"id": 8, "title": "Iced Tea", "price": 2.49, "featured": True, "category_id": 4},
        {"id": 9, "title": "Caesar Salad", "price": 8.49, "featured":False, "category_id": 5},
        {"id": 10, "title": "Greek Salad", "price": 7.99, "featured":False, "category_id": 5},
        {"id": 11, "title": "Tomato Soup", "price": 5.99, "featured":False, "category_id": 6},
        {
            "id": 12,
            "title": "Chicken Noodle Soup",
            "price": 6.49,
            "featured":False,
            "category_id": 6,
        },
        {"id": 13, "title": "Garlic Bread", "price": 3.99, "featured":False, "category_id": 1},
        {"id": 14, "title": "Steak", "price": 18.99, "featured": True, "category_id": 2},
        {"id": 15, "title": "Cheesecake", "price": 7.49, "featured": True, "category_id": 3},
        {"id": 16, "title": "Cappuccino", "price": 4.99, "featured": True, "category_id": 4},
        {
            "id": 17,
            "title": "Greek Gyro Salad",
            "price": 9.99,
            "featured":False,
            "category_id": 5,
        },
        {
            "id": 18,
            "title": "Minestrone Soup",
            "price": 6.99,
            "featured":False,
            "category_id": 6,
        },
        {"id": 19,
         "title": "Onion Rings",
         "price": 5.49,
         "featured":False,
         "category_id": 1
         },

        {"id": 20,
         "title": "Salmon",
         "price": 16.99,
         "featured": True,
         "category_id": 2}

]
    # Add the remaining menu items here

# Insert menu items into the 'app_menuitem' table
for item in menu_items:
    cursor.execute("""
        INSERT INTO app_menuitem (id, title, price, featured, category_id)
        VALUES (?, ?, ?, ?, ?)
    """, (
        item["id"],
        item["title"],
        item["price"],
        item["featured"],
        item["category_id"]
    ))

# Commit the changes and close the database connection
conn.commit()
conn.close()
