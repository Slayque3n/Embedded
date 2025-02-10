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