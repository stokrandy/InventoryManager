from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection helper
def db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

# Route to display and add locations
@app.route('/locations', methods=['GET', 'POST'])
def locations():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        main_location = request.form['main_location']
        sublocation = request.form['sublocation']
        cursor.execute('INSERT INTO tblLocations (MainLocation, Sublocation) VALUES (?, ?)',
                       (main_location, sublocation))
        conn.commit()
        return redirect(url_for('locations'))

    cursor.execute('SELECT * FROM tblLocations')
    locations = cursor.fetchall()
    conn.close()
    return render_template('locations.html', locations=locations)

@app.route('/delete_location/<int:id>', methods=['POST'])
def delete_location(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tblLocations WHERE LocationID = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('locations'))

# Route to display and add categories
@app.route('/categories', methods=['GET', 'POST'])
def categories():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        category_name = request.form['category_name']
        cursor.execute('INSERT INTO tblCategories (CategoryName) VALUES (?)', (category_name,))
        conn.commit()
        return redirect(url_for('categories'))

    cursor.execute('SELECT * FROM tblCategories')
    categories = cursor.fetchall()
    conn.close()
    return render_template('categories.html', categories=categories)

@app.route('/delete_category/<int:id>', methods=['POST'])
def delete_category(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tblCategories WHERE CategoryID = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('categories'))

# Route to display and add main inventory
@app.route('/main', methods=['GET', 'POST'])
def main():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        location_id = request.form['location_id']
        category_id = request.form['category_id']
        description = request.form['description']
        notes = request.form['notes']
        parent_id = request.form.get('parent_id') or None

        cursor.execute('INSERT INTO tblMain (LocationID, CategoryID, Description, Notes, ParentID) VALUES (?, ?, ?, ?, ?)',
                       (location_id, category_id, description, notes, parent_id))
        conn.commit()
        return redirect(url_for('main'))

    cursor.execute('''
        SELECT
            tblMain.ID,
            tblMain.Description,
            tblMain.Notes,
            tblLocations.MainLocation || ' (' || tblLocations.Sublocation || ')' AS Location,
            tblCategories.CategoryName
        FROM tblMain
        LEFT JOIN tblLocations ON tblMain.LocationID = tblLocations.LocationID
        LEFT JOIN tblCategories ON tblMain.CategoryID = tblCategories.CategoryID
    ''')
    main_items = cursor.fetchall()

    cursor.execute('SELECT * FROM tblLocations')
    locations = cursor.fetchall()

    cursor.execute('SELECT * FROM tblCategories')
    categories = cursor.fetchall()

    conn.close()
    return render_template('main.html', main_items=main_items, locations=locations, categories=categories)

@app.route('/delete_main/<int:id>', methods=['POST'])
def delete_main(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tblMain WHERE ID = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('main'))

@app.route('/add_item_details/<int:main_id>', methods=['GET', 'POST'])
def add_item_details(main_id):
    conn = db_connection()
    cursor = conn.cursor()

    # Fetch the description for the item being edited
    cursor.execute('SELECT Description FROM tblMain WHERE ID = ?', (main_id,))
    item = cursor.fetchone()

    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        sn = request.form['sn']
        cost = request.form['cost']
        quantity = request.form['quantity']
        condition = request.form['condition']

        cursor.execute('''
            INSERT INTO tblDetail (tblMainID, Make, Model, SN, Cost, Quantity, Condition)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (main_id, make, model, sn, cost, quantity, condition))
        conn.commit()
        conn.close()
        return redirect(url_for('main'))

    conn.close()
    return render_template('add_item_details.html', main_id=main_id, description=item['Description'] if item else None)

@app.route('/scan_qr', methods=['GET', 'POST'])
def scan_qr():
    if request.method == 'POST':
        file = request.files['qr_image']
        img = Image.open(file)
        qr_data = decode(img)
        if qr_data:
            data = qr_data[0].data.decode('utf-8')
            item_id = data.split(",")[0].split(":")[1].strip()
            return redirect(f'/view_item/{item_id}')
        else:
            return "Invalid QR Code", 400
    return render_template('scan_qr.html')

@app.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        category_name = request.form['category_name']
        cursor.execute('''
            UPDATE tblCategories
            SET CategoryName = ?
            WHERE CategoryID = ?
        ''', (category_name, category_id))
        conn.commit()
        conn.close()
        return redirect(url_for('categories'))

    cursor.execute('SELECT * FROM tblCategories WHERE CategoryID = ?', (category_id,))
    category = cursor.fetchone()
    conn.close()
    return render_template('edit_category.html', category=category)

@app.route('/edit_main/<int:item_id>', methods=['GET', 'POST'])
def edit_main(item_id):
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        location_id = request.form['location_id']
        category_id = request.form['category_id']
        description = request.form['description']
        notes = request.form['notes']
        parent_id = request.form.get('parent_id') or None
        cursor.execute('''
            UPDATE tblMain
            SET LocationID = ?, CategoryID = ?, Description = ?, Notes = ?, ParentID = ?
            WHERE ID = ?
        ''', (location_id, category_id, description, notes, parent_id, item_id))
        conn.commit()
        conn.close()
        return redirect(url_for('main'))

    cursor.execute('SELECT * FROM tblMain WHERE ID = ?', (item_id,))
    item = cursor.fetchone()

    cursor.execute('SELECT * FROM tblLocations')
    locations = cursor.fetchall()

    cursor.execute('SELECT * FROM tblCategories')
    categories = cursor.fetchall()

    conn.close()
    return render_template('edit_main.html', item=item, locations=locations, categories=categories)

if __name__ == '__main__':
    app.run(debug=True)
