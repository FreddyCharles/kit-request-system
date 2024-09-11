import sqlite3
from prettytable import PrettyTable

def view_inventory():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM inventory')
    items = c.fetchall()
    
    # Create a PrettyTable object and set the column names
    table = PrettyTable()
    table.field_names = ["ID", "Description", "Location", "Size", "Quantity", "Requests", "Requesters"]
    
    # Add rows to the table
    for item in items:
        table.add_row(item)
    
    # Print the table
    print(table)
    
    conn.close()

if __name__ == '__main__':
    view_inventory()
