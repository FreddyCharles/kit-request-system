import sqlite3

def create_inventory_table():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Create the inventory table with an additional 'requester' column
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            storage_location TEXT NOT NULL,
            size TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            requests INTEGER DEFAULT 0,
            requester TEXT DEFAULT ''
        )
    ''')

    conn.commit()
    conn.close()
    print('Inventory table created successfully!')

def main():
    create_inventory_table()

if __name__ == '__main__':
    main()
