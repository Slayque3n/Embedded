# funcforweb.py
import sqlite3

def get_moisture_changes(plant_id, db_name="plant_management.db"):
    """
    Fetch all rows where change_description is 'moisture' for a specific plant_id.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Changes WHERE change_description = 'moisture' AND plant_id = ? ORDER BY time DESC LIMIT 1
    """, (plant_id,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_temperature_changes(plant_id, db_name="plant_management.db"):
    """
    Fetch all rows where change_description is 'temperature' for a specific plant_id.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Changes WHERE change_description = 'temperature' AND plant_id = ? ORDER BY time DESC LIMIT 1
    """, (plant_id,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_light_changes(plant_id, db_name="plant_management.db"):
    """
    Fetch all rows where change_description is 'light' for a specific plant_id.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Changes WHERE change_description = 'light' AND plant_id = ? ORDER BY time DESC LIMIT 1
    """, (plant_id,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_humidity_changes(plant_id, db_name="plant_management.db"):
    """
    Fetch all rows where change_description is 'humidity' for a specific plant_id.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Changes WHERE change_description = 'humidity' AND plant_id = ? ORDER BY time DESC LIMIT 1
    """, (plant_id,))
    results = cursor.fetchall()
    conn.close()
    return results

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

def add_plant_for_owner(owner_id, plant_name, plant_type, db_name="plant_management.db"):
    """
    Adds a new plant to the database and links it to an owner.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Insert the new plant with plant_type directly
    cursor.execute("""
    INSERT INTO Plants (plant_name, plant_type) VALUES (?, ?)
    """, (plant_name, plant_type))

    plant_id = cursor.lastrowid  # Get the newly inserted plant's ID

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

def update_email(owner_id, new_email, db_name="plant_management.db"):
    """
    Updates the contact information of an existing owner.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Update the contact info for the given owner_id
    cursor.execute("""
    UPDATE Owners SET email = ? WHERE owner_id = ?
    """, (new_email, owner_id))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def remove_plant(plant_id, db_name="plant_management.db"):
    """
    Removes a plant from the database, including its ownership records.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Step 1: Remove plant from Ownership table first (to maintain foreign key constraints)
    cursor.execute("DELETE FROM Ownership WHERE plant_id = ?", (plant_id,))

    # Step 2: Remove plant from Plants table
    cursor.execute("DELETE FROM Plants WHERE plant_id = ?", (plant_id,))

    # Commit changes and close the connection
    conn.commit()
    conn.close()