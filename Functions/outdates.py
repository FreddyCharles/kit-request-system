from app.webapp import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

@app.route('/inventory', methods=['GET'])
def get_inventory():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM inventory')
    items = c.fetchall()
    conn.close()
    
    # Convert items to a list of dictionaries
    inventory = [dict(item) for item in items]

    return jsonify(inventory)

@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM inventory WHERE ID = ?', (item_id,))
    item = c.fetchone()
    conn.close()
    
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    
    return jsonify(dict(item))

@app.route('/inventory', methods=['POST'])
def add_item():
    new_item = request.json
    if not all(key in new_item for key in ['Description', 'Location', 'Size', 'Quantity', 'Requests']):
        return jsonify({'error': 'Missing fields'}), 400

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO inventory (Description, Location, Size, Quantity, Requests) VALUES (?, ?, ?, ?, ?)',
              (new_item['Description'], new_item['Location'], new_item['Size'], new_item['Quantity'], new_item['Requests']))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Item added successfully'}), 201

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM inventory WHERE ID = ?', (item_id,))
    conn.commit()
    conn.close()
    
    if c.rowcount == 0:
        return jsonify({'error': 'Item not found'}), 404
    
    return jsonify({'message': 'Item deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Listen on all interfaces
