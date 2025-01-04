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

    cursor.execute('SELECT * FROM tblMain')
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

if __name__ == '__main__':
    app.run(debug=True)
