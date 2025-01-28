import sqlite3

# Connect to the database
def connect_db():
    return sqlite3.connect("plant_management.db")

# Function to add a new user
def add_user(owner_name, contact_info):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Owners (owner_name, contact_info) VALUES (?, ?)", (owner_name, contact_info))
    conn.commit()
    conn.close()

    print(f"User {owner_name} added successfully.")

# Function to register a new plant for a user
def register_plant_for_user(owner_name, change_description):
    conn = connect_db()
    cursor = conn.cursor()

    # Find the owner_id based on owner_name
    cursor.execute("SELECT owner_id FROM Owners WHERE owner_name = ?", (owner_name,))
    owner = cursor.fetchone()

    if not owner:
        print(f"Owner {owner_name} does not exist.")
        conn.close()
        return

    owner_id = owner[0]

    # Insert new plant change
    cursor.execute("INSERT INTO Changes (plant_id, change_description) VALUES (NULL, ?)", (change_description,))
    conn.commit()

    # Get the plant_id of the newly inserted plant change
    cursor.execute("SELECT plant_id FROM Changes WHERE change_description = ? ORDER BY time DESC LIMIT 1", (change_description,))
    plant = cursor.fetchone()

    plant_id = plant[0]

    # Register the ownership of the plant
    cursor.execute("INSERT INTO Ownership (owner_id, plant_id) VALUES (?, ?)", (owner_id, plant_id))
    conn.commit()
    conn.close()

    print(f"Plant registered for {owner_name} successfully.")

# Function to query the database for a specific plant by its ID
def query_plant_by_id(plant_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Query plant change details
    cursor.execute("SELECT * FROM Changes WHERE plant_id = ?", (plant_id,))
    plant_changes = cursor.fetchall()

    if not plant_changes:
        print(f"No changes found for plant ID {plant_id}.")
        conn.close()
        return

    print(f"Details of plant ID {plant_id}:")
    for change in plant_changes:
        print(f"Change ID: {change[0]}, Time: {change[1]}, Description: {change[3]}")

    # Query ownership information
    cursor.execute("SELECT o.owner_name, o.contact_info FROM Owners o JOIN Ownership ow ON o.owner_id = ow.owner_id WHERE ow.plant_id = ?", (plant_id,))
    owner_info = cursor.fetchone()

    if owner_info:
        print(f"Owner: {owner_info[0]}, Contact: {owner_info[1]}")
    else:
        print("No owner found for this plant.")

    conn.close()

# Example usage
if __name__ == "__main__":
    # Add a new user
    add_user("Bob", "bob@example.com")

    # Register a new plant for Bob
    register_plant_for_user("Bob", "Planted a new flower")

    # Query plant details by plant ID (assuming plant_id is 1)
    query_plant_by_id(1)
