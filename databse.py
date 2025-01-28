import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("plant_management.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS Changes (
    change_id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    plant_id INTEGER NOT NULL,
    change_description TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Owners (
    owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_name TEXT NOT NULL,
    contact_info TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Ownership (
    ownership_id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    plant_id INTEGER NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES Owners(owner_id),
    FOREIGN KEY (plant_id) REFERENCES Changes(plant_id)
)
""")

# Commit changes and close connection
conn.commit()

# Example: Insert data into tables
# Add an owner
cursor.execute("INSERT INTO Owners (owner_name, contact_info) VALUES (?, ?)",
               ("Alice", "alice@example.com"))

# Log a change
cursor.execute("INSERT INTO Changes (plant_id, change_description) VALUES (?, ?)",
               (1, "Watered the plant"))

# Map owner to plant
cursor.execute("INSERT INTO Ownership (owner_id, plant_id) VALUES (?, ?)",
               (1, 1))

# Commit changes
conn.commit()

# Query and display data
print("Changes:")
for row in cursor.execute("SELECT * FROM Changes"):
    print(row)

print("\nOwners:")
for row in cursor.execute("SELECT * FROM Owners"):
    print(row)

print("\nOwnership:")
for row in cursor.execute("SELECT * FROM Ownership"):
    print(row)

# Close the connection
conn.close()
