from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM inventory').fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/manage')
def manage():
    return render_template('manage.html')

@app.route('/sort', methods=['POST'])
def sort_inventory():
    column_name = request.form['column_name']
    valid_columns = ["id", "description", "type", "storage_location", "size", "quantity", "requests", "requesters"]
    if column_name.lower() not in valid_columns:
        return "Invalid column name. Valid columns are: " + ", ".join(valid_columns)
    
    conn = get_db_connection()
    items = conn.execute(f'SELECT * FROM inventory ORDER BY {column_name}').fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        description = request.form['description']
        type = request.form['type']
        storage_location = request.form['storage_location']
        size = request.form['size']
        quantity = int(request.form['quantity'])
        requests = int(request.form['requests'])
        requesters = request.form['requesters']

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO inventory (description, type, storage_location, size, quantity, requests, requesters)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (description, type, storage_location, size, quantity, requests, requesters))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_item.html')

@app.route('/remove_item', methods=['POST'])
def remove_item():
    item_id = request.form['item_id']
    conn = get_db_connection()
    conn.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit_item', methods=['GET', 'POST'])
def edit_item():
    if request.method == 'POST':
        item_id = request.form['item_id']
        type = request.form.get('type')
        description = request.form.get('description')
        storage_location = request.form.get('storage_location')
        size = request.form.get('size')
        quantity = request.form.get('quantity')
        requests = request.form.get('requests')
        requesters = request.form.get('requesters')

        conn = get_db_connection()
        updates = []
        parameters = []
        
        if type:
            updates.append("type = ?")
            parameters.append(type)
        if description:
            updates.append("description = ?")
            parameters.append(description)
        if storage_location:
            updates.append("storage_location = ?")
            parameters.append(storage_location)
        if size:
            updates.append("size = ?")
            parameters.append(size)
        if quantity:
            updates.append("quantity = ?")
            parameters.append(quantity)
        if requests:
            updates.append("requests = ?")
            parameters.append(requests)
        if requesters:
            updates.append("requesters = ?")
            parameters.append(requesters)

        if updates:
            update_str = ", ".join(updates)
            parameters.append(item_id)
            conn.execute(f'UPDATE inventory SET {update_str} WHERE id = ?', parameters)
            conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('edit_item.html')

@app.route('/request_item', methods=['POST'])
def request_item():
    item_id = request.form['item_id']
    requester_name = request.form['requester_name']

    conn = get_db_connection()
    item = conn.execute('SELECT requests, requesters FROM inventory WHERE id = ?', (item_id,)).fetchone()
    
    if item:
        current_requests = item['requests']
        current_requesters = item['requesters'] or ""
        if requester_name not in current_requesters.split(', '):
            new_requests = current_requests + 1
            new_requesters = current_requesters + f"{requester_name}, "
            conn.execute('UPDATE inventory SET requests = ?, requesters = ? WHERE id = ?', (new_requests, new_requesters, item_id))
            conn.commit()
    conn.close()
    return redirect(url_for('members_requests'))

@app.route('/clear_requests', methods=['POST'])
def clear_requests():
    conn = get_db_connection()
    conn.execute('UPDATE inventory SET requests = 0, requesters = ""')
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/members_requests')
def members_requests():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM inventory')
    items = c.fetchall()
    conn.close()

    # Convert fetched data to a list of dictionaries
    items_list = [
        {
            'id': item[0],
            'description': item[1],
            'type': item[2],
            'storage_location': item[3],
            'size': item[4],
            'quantity': item[5],
            'requests': item[6],
            'requesters': item[7]
        } for item in items
    ]
    
    return render_template('members_requests.html', items=items_list)


if __name__ == "__main__":
    app.run(debug=True)
