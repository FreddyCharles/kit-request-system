import sqlite3
from viewinventory import view_inventory

def edit_item(item_id, description=None, storage_location=None, size=None, quantity=None, requests=None, requester=None):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Create a list of updates to be made
    updates = []
    parameters = []

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
    if requester is not None:
        parameters.append(requester)

    if not updates:
        print("No fields to update.")
        return

    # Join the update fields with commas
    update_str = ", ".join(updates)
    parameters.append(item_id)

    c.execute(f'UPDATE inventory SET {update_str} WHERE id = ?', parameters)
    conn.commit()
    conn.close()

    if c.rowcount > 0:
        print('Item updated successfully!')
    else:
        print('Item not found.')

def main():
    view_inventory()
    print("Enter the ID of the item to edit:")
    item_id = int(input("Item ID: "))

    print("Enter new details for the item (leave blank to keep current value):")
    description = input("Description: ") or None
    storage_location = input("Storage Location: ") or None
    size = input("Size: ") or None
    quantity = input("Quantity: ")
    quantity = int(quantity) if quantity else None
    requests = input("Number of Requests: ")
    requests = int(requests) if requests else None

    edit_item(item_id, description, storage_location, size, quantity, requests)

if __name__ == '__main__':
    main()
