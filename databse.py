import sqlite3
import hashlib

# databse.py
def initialize_database(db_name="plant_management.db"):
    """
    Creates and initializes the SQLite database with necessary tables.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create tables if they do not exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Changes (
        change_id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    
        plant_id INTEGER NOT NULL,
        change_description TEXT NOT NULL,
        value TEXT NOT NULL,
        FOREIGN KEY (plant_id) REFERENCES Plants(plant_id) ON DELETE CASCADE
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Plants (
        plant_id INTEGER PRIMARY KEY AUTOINCREMENT,
        plant_name TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Owners (
        owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_name TEXT NOT NULL,
        email VARCHAR(40) UNIQUE,
        password VARCHAR(64) NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Ownership (
        ownership_id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER NOT NULL,
        plant_id INTEGER NOT NULL,
        FOREIGN KEY (owner_id) REFERENCES Owners(owner_id) ON DELETE CASCADE,
        FOREIGN KEY (plant_id) REFERENCES Plants(plant_id) ON DELETE CASCADE
    )
    """)

    # Commit changes and close connection
    conn.commit()
    conn.close()
        
    # Example: Insert data into tables
    # Add an owner
    conn = sqlite3.connect("plant_management.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Owners (owner_name,email,password) VALUES (?, ?,?)",
                ("Alice", "alice@example.com", hashlib.sha256("Password".encode()).hexdigest()))

    # Log a change
    cursor.execute("INSERT INTO Changes (plant_id, change_description,value) VALUES (?, ?,?)",
                (1, "moisture","94"))
    cursor.execute("INSERT INTO Changes (plant_id, change_description,value) VALUES (?, ?,?)",
                (1, "temperature","29"))
    cursor.execute("INSERT INTO Changes (plant_id, change_description,value) VALUES (?, ?,?)",
                (1, "light","7"))
    cursor.execute("INSERT INTO Changes (plant_id, change_description,value) VALUES (?, ?,?)",
                (1, "humidity","60"))

    # Map owner to plant
    cursor.execute("INSERT INTO Ownership (owner_id, plant_id) VALUES (?, ?)",
                (1, 1))

    # Commit changes
    conn.commit()

    # # Query and display data
    # print("Changes:")
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
