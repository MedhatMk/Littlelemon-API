import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')  # Replace 'your_database_name' with your database name or path

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Define the menu items as a list of dictionaries
menu_items = [

{
      "id": 1,
      "slug": "appetizers",
      "title": "Appetizers"
    },
    {
      "id": 2,
      "slug": "main-courses",
      "title": "Main Courses"
    },
    {
      "id": 3,
      "slug": "desserts",
      "title": "Desserts"
    },
    {
      "id": 4,
      "slug": "beverages",
      "title": "Beverages"
    },
    {
      "id": 5,
      "slug": "salads",
      "title": "Salads"
    },
    {
      "id": 6,
      "slug": "soups",
      "title": "Soups"
    }

]
    # Add the remaining menu items here

# Insert menu items into the 'app_menuitem' table
for item in menu_items:
    cursor.execute("""
        INSERT INTO app_category (id, slug, title)
        VALUES (?, ?, ?)
    """, (
        item["id"],
        item["slug"],
        item["title"],

    ))

# Commit the changes and close the database connection
conn.commit()
conn.close()
