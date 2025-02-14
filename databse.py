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
<<<<<<< HEAD
        contact_info TEXT NOT NULL,
        password TEXT NOT NULL
=======
        email VARCHAR(40) UNIQUE,
        password VARCHAR(64) NOT NULL
>>>>>>> 44eb5479139a866b75bd72079dd58b8a7cc74b6f
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Ownership (
        ownership_id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER NOT NULL,
        plant_id INTEGER NOT NULL,
<<<<<<< HEAD
        FOREIGN KEY (owner_id) REFERENCES Owners(owner_id) ON DELETE CASCADE,
        FOREIGN KEY (plant_id) REFERENCES Plants(plant_id) ON DELETE CASCADE
=======
        FOREIGN KEY (owner_id) REFERENCES Owners(owner_id),
        FOREIGN KEY (plant_id) REFERENCES Plants(plant_id)
>>>>>>> 44eb5479139a866b75bd72079dd58b8a7cc74b6f
    )
    """)

    # Commit changes and close connection
    conn.commit()
    conn.close()
<<<<<<< HEAD

def print_database(db_name="plant_management.db"):
    """
    Prints all data from the database tables.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    tables = ["Plants", "Owners", "Changes", "Ownership"]

    for table in tables:
        print(f"\nTABLE: {table}")
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No data found.")

    conn.close()

# --- Example Data Insertion ---
def insert_sample_data(db_name="plant_management.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Add an owner
    cursor.execute("INSERT INTO Owners (owner_name, contact_info, password) VALUES (?, ?, ?)",
                   ("Alice", "alice@example.com", "securepassword"))

    # Add a plant
    cursor.execute("INSERT INTO Plants (plant_name, plant_type_name) VALUES (?, ?)",
                   ("Rose", "Flowering Plant"))

    # Log a change
    cursor.execute("INSERT INTO Changes (plant_id, change_description, value) VALUES (?, ?, ?)",
                   (1, "Watered the plant", "500ml"))

    # Map owner to plant
    cursor.execute("INSERT INTO Ownership (owner_id, plant_id) VALUES (?, ?)",
                   (1, 1))

    # Commit changes
    conn.commit()
    conn.close()

if __name__ == "__main__":
    try:
        initialize_database()  # Ensure the database is initialized
        print_database()
        print("\nDatabase initialized and displayed successfully.")
        insert_sample_data()
        print_database()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

# Uncomment the line below to insert sample data
# insert_sample_data()
=======
        
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
>>>>>>> 44eb5479139a866b75bd72079dd58b8a7cc74b6f
