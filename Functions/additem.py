import sqlite3
from viewinventory import view_inventory

def add_item(description, storage_location, size, quantity, requests=0, requester=None):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO inventory (description, storage_location, size, quantity, requests, requester)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (description, storage_location, size, quantity, requests, requester))
    conn.commit()
    conn.close()
    print('Item added successfully!')

def main():
    view_inventory()
    print("Enter details for the new item:")
    description = input("Description: ")
    storage_location = input("Storage Location: ")
    size = input("Size: ")
    quantity = int(input("Quantity: "))
    requests = int(input("Number of Requests (default is 0): ") or 0)
    requester = input("Any requesters?: ") or None  # Set default as None if no requesters

    add_item(description, storage_location, size, quantity, requests, requester)

if __name__ == '__main__':
    main()
