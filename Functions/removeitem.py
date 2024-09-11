import sqlite3
from viewinventory import view_inventory

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

def main():
    view_inventory()
    print("Enter the ID of the item to remove:")
    item_id = int(input("Item ID: "))

    remove_item(item_id)

if __name__ == '__main__':
    main()
