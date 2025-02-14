# funcforweb.py
import sqlite3
import hashlib


def get_most_recent_change(plant_id, change_description, db_name="plant_management.db"):
    """
    Fetch the most recent value for a specific change description (e.g., moisture, light, etc.) for a plant.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT value FROM Changes 
        WHERE plant_id = ? AND change_description = ? 
        ORDER BY time DESC 
        LIMIT 1
    """, (plant_id, change_description))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_plants_for_owner(owner_id, db_name="plant_management.db"):
    """
    Retrieves all plant IDs associated with a given owner.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT plant_id FROM Ownership WHERE owner_id = ?
    """, (owner_id,))
    plant_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return plant_ids

def add_plant_for_owner(owner_id, plant_name, db_name="plant_management.db"):
    """
    Adds a new plant to the database and links it to an owner.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Insert the new plant
    cursor.execute("""
    INSERT INTO Plants (plant_name) VALUES (?)
    """, (plant_name,))

    plant_id = cursor.lastrowid  

    # Assign the plant to the owner in the Ownership table
    cursor.execute("""
    INSERT INTO Ownership (owner_id, plant_id) VALUES (?, ?)
    """, (owner_id, plant_id))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def add_owner(owner_name, email, password, db_name="plant_management.db"):
    """
    Adds a new owner to the database.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Hash the password before storing it
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Insert the new owner into the Owners table
    cursor.execute("""
    INSERT INTO Owners (owner_name, email, password) VALUES (?, ?, ?)
    """, (owner_name, email, hashed_password))
    
    # Get the newly inserted owner's ID
    owner_id = cursor.lastrowid

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    return owner_id

def verify_login(email, password):
    conn = sqlite3.connect("plant_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT owner_id, password FROM Owners WHERE email = ?", (email,))  # Add a comma after email
    user = cursor.fetchone()
    conn.close()

    if user:
        owner_id, hashed_password = user
        if hashlib.sha256(password.encode()).hexdigest() == hashed_password:
            return owner_id
    return None