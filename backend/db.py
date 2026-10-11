import sqlite3
import os

# Path to the SQLite database file in the same folder as this script
DB_FILE = os.path.join(os.path.dirname(__file__), "cold_storage.db")


def get_connection():
    """
    Establishes and returns a connection to the SQLite database.
    sqlite3.Row allows accessing columns by name like a dictionary.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    DDL (Data Definition Language) step:
    Creates the 'cold_storage_items' table if it does not already exist,
    and inserts initial sample records.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # DDL: CREATE TABLE with PRIMARY KEY constraint
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cold_storage_items (
            item_id TEXT PRIMARY KEY,
            item_name TEXT NOT NULL,
            category TEXT NOT NULL,
            temperature TEXT NOT NULL
        )
    """)

    # Check if table is empty; if so, populate initial sample items
    cursor.execute("SELECT COUNT(*) FROM cold_storage_items")
    count = cursor.fetchone()[0]

    if count == 0:
        sample_items = [
            ("CS-101", "Fresh Apples", "Fruits", "4°C"),
            ("CS-102", "Frozen Fish", "Seafood", "-18°C"),
            ("CS-103", "Dairy Butter", "Dairy", "-5°C"),
            ("CS-104", "Vaccines", "Pharmaceuticals", "2°C")
        ]
        # DML: INSERT initial records
        cursor.executemany(
            "INSERT INTO cold_storage_items (item_id, item_name, category, temperature) VALUES (?, ?, ?, ?)",
            sample_items
        )
        conn.commit()
        print("Cold storage database initialized with sample inventory.")

    conn.close()


def get_all_items():
    """
    DQL (Data Query Language):
    Fetches all inventory records from the cold storage database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT item_id, item_name, category, temperature FROM cold_storage_items ORDER BY item_id ASC")
    rows = cursor.fetchall()
    conn.close()

    # Convert rows to a list of standard Python dictionaries
    return [
        {
            "item_id": row["item_id"],
            "item_name": row["item_name"],
            "category": row["category"],
            "temperature": row["temperature"]
        }
        for row in rows
    ]


def add_item(item_id, item_name, category, temperature):
    """
    DML (Data Manipulation Language):
    Inserts a new cold storage item into the database.
    Uses parameterized queries (?) to prevent SQL injection.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO cold_storage_items (item_id, item_name, category, temperature) VALUES (?, ?, ?, ?)",
            (item_id.strip(), item_name.strip(), category.strip(), temperature.strip())
        )
        conn.commit()
        return True, "Item added to cold storage successfully."
    except sqlite3.IntegrityError:
        # Handles duplicate Primary Key error
        return False, f"Error: Item with ID '{item_id}' already exists."
    except Exception as e:
        return False, f"Database error: {str(e)}"
    finally:
        conn.close()


def update_item(item_id, item_name, category, temperature):
    """
    DML:
    Updates an existing item's name, category, and temperature by Primary Key (item_id).
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE cold_storage_items SET item_name = ?, category = ?, temperature = ? WHERE item_id = ?",
            (item_name.strip(), category.strip(), temperature.strip(), item_id.strip())
        )
        conn.commit()
        if cursor.rowcount == 0:
            return False, f"No item found with ID '{item_id}'."
        return True, "Cold storage item updated successfully."
    except Exception as e:
        return False, f"Database error: {str(e)}"
    finally:
        conn.close()


def delete_item(item_id):
    """
    DML:
    Deletes an item record from cold storage using its Primary Key (item_id).
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM cold_storage_items WHERE item_id = ?",
            (item_id.strip(),)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return False, f"No item found with ID '{item_id}'."
        return True, "Item removed from cold storage successfully."
    except Exception as e:
        return False, f"Database error: {str(e)}"
    finally:
        conn.close()
