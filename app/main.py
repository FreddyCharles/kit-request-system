import sqlite3
from prettytable import PrettyTable

def create_inventory_table():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT DEFAULT '',
            type TEXT DEFAULT '',
            storage_location TEXT DEFAULT '',
            size TEXT DEFAULT '',
            quantity INTEGER DEFAULT 0,
            requests INTEGER DEFAULT 0,
            requesters TEXT DEFAULT ''
        )
    ''')

    conn.commit()
    conn.close()
    print('Inventory table created successfully!')

def view_inventory():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM inventory')
    items = c.fetchall()

    table = PrettyTable()
    table.field_names = ["ID", "Description", "Type", "Location", "Size", "Quantity", "Requests", "Requesters"]

    for item in items:
        table.add_row(item)

    print(table)

    conn.close()

def add_item(description=None, type=None, storage_location=None, size=None, quantity=0, requests=0, requesters=None):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO inventory (description, type, storage_location, size, quantity, requests, requesters)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (description, type, storage_location, size, quantity, requests, requesters))
    conn.commit()
    conn.close()
    print('Item added successfully!')

def add_item_request():
    print("Enter details for the new item:")
    description = input("Description: ")
    type = input('Type: ')
    storage_location = input("Storage Location: ")
    size = input("Size: ")
    quantity = int(input("Quantity: "))
    requests = int(input("Number of Requests (default is 0): ") or 0)
    requesters = input("Any requesters?: ") or ""  # Set default as empty string if no requesters

    try:
        add_item(description, type, storage_location, size, quantity, requests, requesters)
    except ValueError:
        print('Error!')

def remove_item(item_id):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

    if c.rowcount > 0:
        print('Item removed successfully!')
    else:
        print('Item not found.')

def remove_item_request():
    print("Enter the ID of the item to remove:")
    item_id = int(input("Item ID: "))

    remove_item(item_id)

def edit_item(item_id, type=None, description=None, storage_location=None, size=None, quantity=None, requests=None, requesters=None):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    updates = []
    parameters = []

    if type is not None:
        updates.append("type = ?")
        parameters.append(type)
    if description is not None:
        updates.append("description = ?")
        parameters.append(description)
    if storage_location is not None:
        updates.append("storage_location = ?")
        parameters.append(storage_location)
    if size is not None:
        updates.append("size = ?")
        parameters.append(size)
    if quantity is not None:
        updates.append("quantity = ?")
        parameters.append(quantity)
    if requests is not None:
        updates.append("requests = ?")
        parameters.append(requests)
    if requesters is not None:
        updates.append("requesters = ?")
        parameters.append(requesters)

    if not updates:
        print("No fields to update.")
        return

    update_str = ", ".join(updates)
    parameters.append(item_id)

    c.execute(f'UPDATE inventory SET {update_str} WHERE id = ?', parameters)
    conn.commit()
    conn.close()

    if c.rowcount > 0:
        print('Item updated successfully!')
    else:
        print('Item not found.')

def edit_item_request():
    print("Enter the ID of the item to edit:")
    item_id = int(input("Item ID: "))
    print("Enter new details for the item (leave blank to keep current value):")
    type = input("Type: ") or None
    description = input("Description: ") or None
    storage_location = input("Storage Location: ") or None
    size = input("Size: ") or None
    quantity = input("Quantity: ")
    quantity = int(quantity) if quantity else None
    requests = input("Number of Requests: ")
    requests = int(requests) if requests else None
    requesters = input("Requesters: ") or None

    edit_item(item_id, type, description, storage_location, size, quantity, requests, requesters)

def request_item(item_id, requester_name):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Increment the requests value by 1
    c.execute('SELECT requests, requesters FROM inventory WHERE id = ?', (item_id,))
    item = c.fetchone()

    if item is None:
        print('Item not found.')
        return

    current_requests = item[0]
    current_requesters = item[1] if item[1] else ""

    # Increment the number of requests and update the requesters list
    new_requests = current_requests + 1
    new_requesters = current_requesters + f"{requester_name}, "

    # Update the database with the new requests count and requesters list
    c.execute('UPDATE inventory SET requests = ?, requesters = ? WHERE id = ?', (new_requests, new_requesters, item_id))
    conn.commit()
    conn.close()

    print('Request added successfully!')

def request_item_request():
    print("Enter the ID of the item to request:")
    item_id = int(input("Item ID: "))

    print("Enter your name (FIRST AND LAST NAME):")
    requester_name = input("Name: ")

    request_item(item_id, requester_name)

def clear_requesters():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    c.execute('UPDATE inventory SET requests = 0, requesters = ""')

    conn.commit()
    conn.close()

    if c.rowcount > 0:
        print(f'{c.rowcount} items updated successfully! Requests and requesters cleared.')
    else:
        print('No items to update.')

def reset_ids():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Create a new table with the updated schema
    c.execute('''
        CREATE TABLE IF NOT EXISTS temp_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT DEFAULT '',
            description TEXT DEFAULT '',
            storage_location TEXT DEFAULT '',
            size TEXT DEFAULT '',
            quantity INTEGER DEFAULT 0,
            requests INTEGER DEFAULT 0,
            requesters TEXT DEFAULT ''
        )
    ''')

    # Copy data from the old table to the new one
    c.execute('''
        INSERT INTO temp_inventory (type, description, storage_location, size, quantity, requests, requesters)
        SELECT type, description, storage_location, size, quantity, requests, requesters FROM inventory
    ''')

    # Drop the old table and rename the new one
    c.execute('DROP TABLE inventory')
    c.execute('ALTER TABLE temp_inventory RENAME TO inventory')

    conn.commit()
    conn.close()

    print("IDs reset successfully!")

def manage_inventory():
    while True:
        reset_ids()
        print("\nCurrent Inventory:")
        view_inventory()

        print("\nWhat would you like to do?")
        print("1. Add a new item")
        print("2. Remove an item")
        print("3. Edit an item")
        print("4. Request an item")
        print('5. Clear requests?')
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_item_request()
        elif choice == '2':
            remove_item_request()
        elif choice == '3':
            edit_item_request()
        elif choice == '4':
            request_item_request()
        elif choice == '5':
            confirmation = input('Are you sure? (y/n) ')
            if confirmation == 'y':
                clear_requesters()
            else:
                pass
        elif choice == '6':
            print("Exiting the inventory manager.")
            break
        else:
            print("Invalid choice. Please select 1-6.")

def sort_inventory(column_name):
    valid_columns = ["id", "description", "type", "storage_location", "size", "quantity", "requests", "requesters"]

    if column_name.lower() not in valid_columns:
        print(f"Invalid column name. Valid columns are: {', '.join(valid_columns)}")
        return

    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    c.execute(f'''
        SELECT * FROM inventory
        ORDER BY {column_name}
    ''')

    items = c.fetchall()
    conn.close()

    if not items:
        print(f'No items to display.')
        return

    table = PrettyTable()
    table.field_names = ["ID", "Description", "Type", "Location", "Size", "Quantity", "Requests", "Requesters"]

    for item in items:
        table.add_row(item)

    print(table)


if __name__ == '__main__':
    create_inventory_table()

    while True:
        print("\nCurrent Inventory:")
        view_inventory()

        print("\nWhat would you like to do?")
        print("1. Manage inventory")
        print("2. Sort table")
        print("3. -")
        print("4. -")
        print('5. -')
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            manage_inventory()
        elif choice == '2':
            column = input('What column would you like to sort by? ')
            sort_inventory(column)
        elif choice == '6':
            print("Exiting the inventory manager.")
            break
        else:
            print("Invalid choice. Please select 1-6.")

