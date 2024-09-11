import sqlite3
from viewinventory import view_inventory

def request_item(item_id, requester_name):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Increment the requests value by 1
    c.execute('SELECT requests, requester FROM inventory WHERE id = ?', (item_id,))
    item = c.fetchone()

    if item is None:
        print('Item not found.')
        return

    current_requests = item[0]
    current_requesters = item[1] if item[1] else ""

    # Increment the number of requests and update the requester list
    new_requests = current_requests + 1
    new_requesters = current_requesters + f"{requester_name}, "

    # Update the database with the new requests count and requester name
    c.execute('UPDATE inventory SET requests = ?, requester = ? WHERE id = ?', (new_requests, new_requesters, item_id))
    conn.commit()
    conn.close()

    print('Request added successfully!')

def main():
    view_inventory()
    print("Enter the ID of the item to request:")
    item_id = int(input("Item ID: "))

    print("Enter your name:")
    requester_name = input("Name: ")

    request_item(item_id, requester_name)

if __name__ == '__main__':
    main()
