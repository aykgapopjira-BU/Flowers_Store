from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database path using os.path for cross-platform compatibility
DB_PATH = os.path.join(os.path.dirname(__file__), 'flowers_store.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    flowers = conn.execute('''
        SELECT f.*, c.name as category_name
        FROM Flowers f
        LEFT JOIN Categories c ON f.category_id = c.id
        ORDER BY f.id DESC
    ''').fetchall()
    conn.close()
    return render_template('index.html', flowers=flowers)

@app.route('/flowers')
def flowers():
    conn = get_db_connection()
    flowers = conn.execute('''
        SELECT f.*, c.name as category_name
        FROM Flowers f
        LEFT JOIN Categories c ON f.category_id = c.id
        ORDER BY f.id DESC
    ''').fetchall()
    conn.close()
    return render_template('flowers.html', flowers=flowers)

@app.route('/flowers/add', methods=['GET', 'POST'])
def add_flower():
    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category_id']
        price = request.form['price']
        description = request.form['description']

        conn = get_db_connection()
        conn.execute('INSERT INTO Flowers (name, category_id, price, description) VALUES (?, ?, ?, ?)',
                     (name, category_id, price, description))
        conn.commit()
        conn.close()
        flash('Flower added successfully!')
        return redirect(url_for('flowers'))

    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM Categories').fetchall()
    conn.close()
    return render_template('add_flower.html', categories=categories)

@app.route('/flowers/edit/<int:id>', methods=['GET', 'POST'])
def edit_flower(id):
    conn = get_db_connection()
    flower = conn.execute('SELECT * FROM Flowers WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category_id']
        price = request.form['price']
        description = request.form['description']

        conn.execute('UPDATE Flowers SET name = ?, category_id = ?, price = ?, description = ? WHERE id = ?',
                     (name, category_id, price, description, id))
        conn.commit()
        conn.close()
        flash('Flower updated successfully!')
        return redirect(url_for('flowers'))

    categories = conn.execute('SELECT * FROM Categories').fetchall()
    conn.close()
    return render_template('edit_flower.html', flower=flower, categories=categories)

@app.route('/flowers/delete/<int:id>', methods=['POST'])
def delete_flower(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Flowers WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Flower deleted successfully!')
    return redirect(url_for('flowers'))

@app.route('/categories')
def categories():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM Categories ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('categories.html', categories=categories)

@app.route('/categories/add', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form['name']

        conn = get_db_connection()
        conn.execute('INSERT INTO Categories (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
        flash('Category added successfully!')
        return redirect(url_for('categories'))

    return render_template('add_category.html')

@app.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    conn = get_db_connection()
    category = conn.execute('SELECT * FROM Categories WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']

        conn.execute('UPDATE Categories SET name = ? WHERE id = ?', (name, id))
        conn.commit()
        conn.close()
        flash('Category updated successfully!')
        return redirect(url_for('categories'))

    conn.close()
    return render_template('edit_category.html', category=category)

@app.route('/categories/delete/<int:id>', methods=['POST'])
def delete_category(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Categories WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Category deleted successfully!')
    return redirect(url_for('categories'))

if __name__ == '__main__':
    app.run(debug=True)
