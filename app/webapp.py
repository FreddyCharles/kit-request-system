from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def get_inventory():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM inventory')
    items = c.fetchall()
    conn.close()
    return items

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inventory')
def inventory():
    items = get_inventory()
    return jsonify(items)

@app.route('/request_item', methods=['POST'])
def request_item():
    data = request.json
    item_id = data.get('item_id')
    requester_name = data.get('requester_name')
    
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    
    # Increment the requests value by 1
    c.execute('SELECT requests, requesters FROM inventory WHERE id = ?', (item_id,))
    item = c.fetchone()

    if item is None:
        conn.close()
        return jsonify({'message': 'Item not found.'}), 404

    current_requests = item[0]
    current_requesters = item[1] if item[1] else ""

    # Increment the number of requests and update the requester list
    new_requests = current_requests + 1
    new_requesters = current_requesters + f"{requester_name}, "

    # Update the database with the new requests count and requester name
    c.execute('UPDATE inventory SET requests = ?, requesters = ? WHERE id = ?', (new_requests, new_requesters, item_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Request added successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
