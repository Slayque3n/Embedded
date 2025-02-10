import sqlite3

def get_moisture_changes(plant_id, db_name="plant_management.db"):
    """
    Fetch all rows where change_description is 'moisture' for a specific plant_id.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Changes WHERE change_description = 'moisture' AND plant_id = ?
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
        SELECT * FROM Changes WHERE change_description = 'temperature' AND plant_id = ?
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
        SELECT * FROM Changes WHERE change_description = 'light' AND plant_id = ?
    """, (plant_id,))
    results = cursor.fetchall()
    conn.close()
    return results
def get_plants_for_owner(owner_id, db_name="plant_management.db"):
    """
    Retrieves all plant IDs associated with a given owner.
    
    :param owner_id: The ID of the owner whose plants we want to retrieve.
    :param db_name: The SQLite database file name.
    :return: A list of plant IDs owned by the specified owner.
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
    Adds a new plant to the database, assigns it a plant type, and links it to an owner.

    :param owner_id: The ID of the owner.
    :param plant_name: The name of the plant.
    :param plant_type: The type of the plant (e.g., "Succulent", "Fern").
    :param db_name: The SQLite database file name.
    :return: The new plant's ID.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Step 1: Check if the plant type exists
    cursor.execute("SELECT plant_type_id FROM PlantTypes WHERE plant_type_name = ?", (plant_type,))
    result = cursor.fetchone()

    if result:
        plant_type_id = result[0]  # Get existing plant_type_id
    else:
        # Step 2: Insert the new plant type if not found
        cursor.execute("INSERT INTO PlantTypes (plant_type_name) VALUES (?)", (plant_type,))
        plant_type_id = cursor.lastrowid  # Get the new plant_type_id

    # Step 3: Insert the new plant with plant_type_id
    cursor.execute("""
    INSERT INTO Plants (plant_name, plant_type_id) VALUES (?, ?)
    """, (plant_name, plant_type_id))

    plant_id = cursor.lastrowid  # Get the newly inserted plant's ID

    # Step 4: Assign the plant to the owner in the Ownership table
    cursor.execute("""
    INSERT INTO Ownership (owner_id, plant_id) VALUES (?, ?)
    """, (owner_id, plant_id))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def add_owner(owner_name, contact_info, db_name="plant_management.db"):
    """
    Adds a new owner to the database.

    :param owner_name: The name of the owner.
    :param contact_info: Contact information of the owner (email, phone, etc.).
    :param db_name: The SQLite database file name.
    :return: The new owner's ID.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Insert the new owner into the Owners table
    cursor.execute("""
    INSERT INTO Owners (owner_name, contact_info) VALUES (?, ?)
    """, (owner_name, contact_info))
    
    # Get the newly inserted owner's ID
    owner_id = cursor.lastrowid

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    return owner_id

def update_contact_info(owner_id, new_contact_info, db_name="plant_management.db"):
    """
    Updates the contact information of an existing owner.

    :param owner_id: The ID of the owner whose contact info needs to be updated.
    :param new_contact_info: The new contact information (email, phone, etc.).
    :param db_name: The SQLite database file name.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Update the contact info for the given owner_id
    cursor.execute("""
    UPDATE Owners SET contact_info = ? WHERE owner_id = ?
    """, (new_contact_info, owner_id))

    # Commit changes and close the connection
    conn.commit()
    conn.close()



def remove_plant(plant_id, db_name="plant_management.db"):
    """
    Removes a plant from the database, including its ownership records.

    :param plant_id: The ID of the plant to be removed.
    :param db_name: The SQLite database file name.
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